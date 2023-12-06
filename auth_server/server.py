from flask import Flask, request, abort
from flask_bcrypt import Bcrypt
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
)
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SECRET_KEY"] = "VerySecretKey"  # You MUST change this secret key
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "sqlite:///users.db"  # You MUST change this db URI
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(60))
    fullname = db.Column(db.String(100))  # New field for storing full name
    email = db.Column(db.String(100), unique=True)  # New field for storing email
    orchestra_id = db.Column(
        db.PickleType()
    )  # New field for storing list of orchestras


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/register", methods=["POST"])
def register():
    data = request.json
    hashed_password = bcrypt.generate_password_hash(data["password"]).decode("utf-8")
    new_user = User(
        username=data["username"],
        password=hashed_password,
        fullname=data["fullname"],
        email=data["email"],
        orchestra_id=[],
    )
    db.session.add(new_user)
    db.session.commit()
    return "User created!", 201


@app.route("/login", methods=["POST"])
def login():
    data = request.json
    user = User.query.filter_by(username=data["username"]).first()
    if user and bcrypt.check_password_hash(user.password, data["password"]):
        login_user(user)
        return "Logged in successfully!", 200
    else:
        abort(401)


if __name__ == "__main__":
    db.create_all(app=app)
    app.run()
