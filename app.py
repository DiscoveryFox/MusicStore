import os

import dotenv
import flask
from flask_bcrypt import Bcrypt

from tools.models import User
from tools.models import db  # Import the SQLAlchemy db object
from tools.verification_mail import EmailVerificator

dotenv.load_dotenv()

app = flask.Flask(__name__)
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = r"sqlite:///C:\Users\Flinn\OneDrive\Dokumente\MusicStore\database.db"


app.config["MAIL_SERVER"] = os.getenv("MAIL_SERVER")
app.config["MAIL_PORT"] = os.getenv("MAIL_PORT")
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
app.config["MAIL_USE_TLS"] = os.getenv("MAIL_USE_TLS")
app.config["MAIL_USE_SSL"] = os.getenv("MAIL_USE_SSL")


app.secret_key = os.getenv("APP_SECRET_KEY")

verificator = EmailVerificator(app)
db.init_app(app)
bcrypt = Bcrypt(app)


@app.route("/")
def index():
    return flask.render_template("index.html")


# 245 413
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
