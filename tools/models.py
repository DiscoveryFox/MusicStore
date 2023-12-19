import os
import shutil
import uuid

import flask_login
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String
from sqlalchemy.orm import relationship

db = SQLAlchemy()

user_orchestra_association = db.Table(
    "user_orchestra_association",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
    db.Column("orchestra_id", db.Integer, db.ForeignKey("orchestra.id")),
)


class User(db.Model, flask_login.UserMixin):
    id = db.Column(Integer, primary_key=True)
    full_name = db.Column(String)
    username = db.Column(String)
    email = db.Column(String, unique=True)
    password_hash = db.Column(String)
    profile_picture = db.Column(String)  # URL or File Path

    twofa_enabled = db.Column(db.Boolean, default=False)
    twofa_secret = db.Column(db.String(120))
    reset_tokens = db.relationship("PasswordResetToken", backref="user", lazy=True)

    email_confirmed = db.Column(db.Boolean, default=False)

    verification_tokens = db.relationship(
        "VerificationToken", backref="user", lazy=True
    )

    orchestra_memberships = relationship(
        "Orchestra", secondary=user_orchestra_association, back_populates="members"
    )


class Orchestra(db.Model):
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String, nullable=False)

    description = db.Column(String)
    profile_picture = db.Column(String)

    members = relationship(
        "User",
        secondary=user_orchestra_association,
        back_populates="orchestra_memberships",
    )


class VerificationToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(80), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    expiration_date = db.Column(db.DateTime, nullable=False)

    def __init__(self, token, user_id, expiration_date):
        self.token = token
        self.user_id = user_id
        self.expiration_date = expiration_date


class PasswordResetToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(80), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    expiration_date = db.Column(db.DateTime, nullable=False)

    def __init__(self, token, user_id, expiration_date):
        self.token = token
        self.user_id = user_id
        self.expiration_date = expiration_date


class MusicalPiece(db.Model):
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String, nullable=False)
    file_path = db.Column(String(100), nullable=False)
    folder_id = db.Column(String(40), nullable=False)
    instrument = db.Column(String(40), nullable=False)


class TemporaryLocation(db.Model):
    id = db.Column(String(40), primary_key=True, nullable=False)
    path = db.Column(String(100), nullable=False)

    def get_filepath(self, filename: str):
        return os.path.join(self.path, filename)

    def __str__(self):
        return f"TemporaryLocation with ID: {self.id} \nPath: {self.path}"


# todo: this code still needs to be reviewed. Generated with ai. Could be wrong.
""" 
def add_piece(name: str, composer: str, genre: str, files: dict):
    \"\"\"
    This function would add the piece to the database and move the individual files to the corresponding folders.

    :param name: The name of the musical piece
    :param composer: The composer of the musical piece
    :param genre: The genre of the musical piece
    :param files: A dict containing the paths of the individual instrument files.
                  The key is the instrument name and the value is the corresponding file path.

    For example:
    files = {
        "trumpet_b": "/path_to_file/1_trumpet_b",
        "tuba_c": "/path_to_file/1_tuba_c"
    }
    \"\"\"
    piece = MusicalPiece(name=name, composer=composer, genre=genre, file_path="")
    db.session.add(piece)
    db.session.commit()  # The piece is now added to the database, and it has been assigned a unique id.

    # The storage directory where the files would be moved to.
    directory_path = f"storage/{piece.id}"

    # Create the directory if it doesn't exist
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

    for instrument_name, file_path in files.items():
        # Move the file to the directory
        shutil.move(
            file_path, os.path.join(directory_path, f"{piece.id}_{instrument_name}")
        )

    # Update the file_path column with the correct directory path.
    piece.file_path = directory_path
    db.session.commit()

"""


def getFilePath(piece_id: int) -> str:
    piece = MusicalPiece.query.get(piece_id)
    if piece:
        return piece.file_path
    else:
        return None


def join_orchestra(user_id: int, group_id: int):
    """

    :param user_id:
    :param group_id:
    :return: Returns True if the user has joined the orchestra, False if user failed to join the
    orchestra. Either the orchestra or the user doesn't exist then.
    """
    user = User.query.get(user_id)
    group = Group.query.get(group_id)

    if user and group:
        user.groups.append(group)
        db.session.commit()
        return True
    else:
        return False


class TemporaryDirectory:
    def __init__(self, delete: bool = True):
        self.delete = delete
        self.folder_name = uuid.uuid4().hex

        self.id = self.folder_name

        self.path = f"/tmp/{self.folder_name}"

        os.mkdir(path=self.path)

    def cleanup(self):
        shutil.rmtree(self.path)

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        if self.delete:
            self.cleanup()
