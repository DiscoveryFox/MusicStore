from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

db = SQLAlchemy()


user_orchestra_association = db.Table(
    "user_orchestra_association",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id")),
    db.Column("orchestra_id", db.Integer, db.ForeignKey("orchestra_memberships.id")),
)


class OrchestraMembership(db.Model):
    __tablename__ = "orchestra_memberships"

    id = db.Column(Integer, primary_key=True)
    user_id = db.Column(Integer, ForeignKey("users.id"))
    orchestra_id = db.Column(Integer, ForeignKey("orchestra_memberships.id"))
    role = db.Column(String)
    instruments_played = db.Column(String)  # Comma-separated list or JSON array.
    user = relationship("User", back_populates="orchestra_memberships")
    orchestra = relationship("Orchestra", back_populates="orchestra_memberships")


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(Integer, primary_key=True)
    full_name = db.Column(String)
    username = db.Column(String)
    email = db.Column(String, unique=True)
    password_hash = db.Column(String)
    profile_picture = db.Column(String)  # URL or File Path
    short_description = db.Column(String)
    # ... add other columns as needed.

    # Define a one-to-many relationship with VerificationToken
    verification_tokens = relationship("VerificationToken", back_populates="user")

    orchestra_memberships = relationship(
        "Orchestra", secondary=user_orchestra_association, back_populates="members"
    )


class Orchestra(db.Model):
    __tablename__ = "orchestras"

    id = db.Column(Integer, primary_key=True)
    name = db.Column(String)
    # ... add other columns as needed.

    members = relationship(
        "User",
        secondary=user_orchestra_association,
        back_populates="orchestra_memberships",
    )


class VerificationToken(db.Model):
    __tablename__ = "verification_tokens"

    id = db.Column(Integer, primary_key=True)
    user_id = db.Column(Integer, ForeignKey("users.id"))
    token = db.Column(String, unique=True)
    expiry_timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    # Define a many-to-one relationship with User
    user = relationship("User", back_populates="verification_tokens")


class PasswordResetToken(db.Model):
    __tablename__ = "password_reset_tokens"

    id = db.Column(Integer, primary_key=True)
    user_id = db.Column(Integer, ForeignKey("users.id"))
    token = db.Column(String, unique=True)
    expiry_timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    # Define a many-to-one relationship with User
    user = relationship("User", back_populates="password_reset_tokens")
