import os
import uuid

import dotenv
import fitz
import flask
import flask_login
from flask import request, send_file, url_for, flash, redirect
from flask_bcrypt import Bcrypt
from flask_login import current_user
from flask_migrate import Migrate
from werkzeug.utils import secure_filename

import tools.file_orchestrator
from tools.models import User, TemporaryDirectory, TemporaryLocation
from tools.models import db  # Import the SQLAlchemy db object
from tools.verification_mail import EmailVerificator

dotenv.load_dotenv()

app = flask.Flask(__name__)
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = r"sqlite:///C:\Users\Flinn\OneDrive\Dokumente\MusicStore\database.db"
# = "sqlite:////workspaces/MusicStore/database.db"


app.config["MAIL_SERVER"] = os.getenv("MAIL_SERVER")
app.config["MAIL_PORT"] = os.getenv("MAIL_PORT")
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
app.config["MAIL_USE_TLS"] = os.getenv("MAIL_USE_TLS")
app.config["MAIL_USE_SSL"] = os.getenv("MAIL_USE_SSL")

app.config["STORAGE_PATH"] = os.getenv("STORAGE_PATH")

login_manager = flask_login.LoginManager()

app.secret_key = os.getenv("APP_SECRET_KEY")

verificator = EmailVerificator(app)
login_manager.init_app(app)
db.init_app(app)
bcrypt = Bcrypt(app)


migrate = Migrate(app, db)

orchestrator = tools.file_orchestrator.FileOrchestrator(database=db)


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@app.route("/")
def index():
    return flask.render_template(
        "index.html", ids=orchestrator.get_user_pieces(user=current_user)
    )


def allowed_file(filename: str):
    print(filename)
    return True


@app.route("/upload_file", methods=["POST", "Get"])
def upload_file():
    if request.method == "POST":
        # check if the post request has the file part
        if "file" not in request.files:
            flash("No file part")
            return redirect(request.url)

        files = request.files.to_dict(flat=False)
        piece_id = str(
            request.form.get("piece_id")
            if request.form.get("piece_id")
            else orchestrator.get_automatic_next_id()
        )
        # TODO: This is an AI Feature for name detection. You need to be able to disable this. But this is a very cool feature.
        # song_name = tools.ai_functionality.get_song_name_from_content(
        #     files.get("file")[0].stream.read()
        # )
        song_name = files.get("file")[0].filename
        # os.mkdir(os.path.join(app.config["STORAGE_PATH"], piece_id))

        # TODO: Add temporary storage for the files. The files should be saved in the right directory on submit in the
        # init song.html form
        print("Starting tempdir")
        with TemporaryDirectory(delete=False) as tmpdir:
            print("created temporary directory", tmpdir.path)
            print(tmpdir.id)

            location = TemporaryLocation(id=tmpdir.id, path=tmpdir.path)
            print(location)
            db.session.add(location)
            db.session.commit()

            for file in files.get("file"):
                if file:
                    filename = secure_filename(file.filename)
                    filename = f"{uuid.uuid4()}.{filename}"
                    file.save(os.path.join(tmpdir.path, filename))
                    print("-------")
                    print(tmpdir.id)
                    print(type(tmpdir.id))
                    print(tmpdir.path)
                    print(type(tmpdir.path))
                    print("-------")

                    if filename.endswith(".pdf"):
                        for index, page in enumerate(
                            fitz.open(location.get_filepath(filename))  # noqa
                        ):
                            print(location.get_filepath(filename))
                            print(filename)
                            pix = page.get_pixmap()
                            pix.save(
                                f"{tmpdir.path}/{filename.split('.')[0]}_page_{index}.png"
                            )
            return flask.render_template(
                "init_song.html",
                song_title=song_name,
                automatic_id=orchestrator.get_automatic_next_id(),
                stored_id=tmpdir.id,
                files=orchestrator.render_files_for_flask(tmpdir),
            )
    elif request.method == "GET":
        return flask.render_template(
            "upload_file.html", automatic_id=orchestrator.get_automatic_next_id()
        )


@app.route("/load_preview", methods=["GET"])
def load_preview():
    folder_id: str = str(flask.request.args.get("folder_id"))
    part_id: str = str(flask.request.args.get("part_id"))

    print(f"Requested {part_id} preview from {folder_id}")
    print(orchestrator.get_filepath(folder_id, part_id, preview=True))
    return send_file(
        orchestrator.get_filepath(folder_id, part_id, preview=True),
        mimetype="image/png",
    )


@app.route("/finish_setup", methods=["POST"])
def finish_setup():
    data = request.json


@app.route("/register", methods=["GET", "POST"])
def register():
    if flask.request.method == "POST":
        full_name = flask.request.form["full_name"]
        username = flask.request.form["username"]
        email = flask.request.form["email"]
        password = flask.request.form["password"]

        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

        # Create a new user
        user = User(
            full_name=full_name,
            username=username,
            email=email,
            password_hash=hashed_password,
        )
        db.session.add(user)
        db.session.commit()

        flask.flash("Registration successful. You can now log in.", "success")
        return flask.redirect(flask.url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if flask.request.method == "POST":
        email = flask.request.form["email"]
        password = flask.request.form["password"]

        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password_hash, password):
            # Log in the user
            flask.flash("Login successful.", "success")
            return flask.redirect(url_for("profile"))
        else:
            flask.flash("Login failed. Please check your email and password.", "error")

    return flask.render_template("login.html")


@app.route("/profile")
def profile():
    # Implement your profile view here
    return "User Profile"


@app.route("/create_table")
def create_table_on_flask():
    db.create_all()
    return "Ok", 202


if __name__ == "__main__":
    app.run()
