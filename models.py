from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

db = SQLAlchemy()

user_orchestra_association = db.Table(
    "user_orchestra_association",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
    db.Column("orchestra_id", db.Integer, db.ForeignKey("orchestra.id")),
)


class User(db.Model):
    id = db.Column(Integer, primary_key=True)
    full_name = db.Column(String)
    username = db.Column(String)
    email = db.Column(String, unique=True)
    password_hash = db.Column(String)
    profile_picture = db.Column(String)  # URL or File Path

    twofa_enabled = db.Column(db.Boolean, default=False)
    twofa_secret = db.Column(db.String(120))
    reset_tokens = db.relationship("PasswordResetToken", backref="user", lazy=True)

    verification_tokens = db.relationship(
        "VerificationToken", backref="user", lazy=True
    )

    orchestra_memberships = relationship(
        "Orchestra", secondary=user_orchestra_association, back_populates="members"
    )


class Orchestra(db.Model):
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String, nullable=False)

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
