import flask
from models import db  # Import the SQLAlchemy db object
from models import User, Orchestra, OrchestraMembership
from flask_bcrypt import Bcrypt

app = flask.Flask(__name__)
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = r"sqlite:///C:\Users\Flinn\OneDrive\Dokumente\MusicStore\database.db"

db.init_app(app)
bcrypt = Bcrypt(app)


@app.route("/")
def index():
    return flask.render_template("index.html")


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
        return flask.redirect(url_for("login"))


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


if __name__ == "__main__":
    app.run()
