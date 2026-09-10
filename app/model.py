from datetime import datetime, timezone
from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    date_of_birth = db.Column(
        db.Date,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc)
    )

    spins = db.relationship(
        "Spin",
        backref="user",
        lazy=True
    )


class Spin(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )

    number = db.Column(
        db.Integer,
        nullable=False
    )

    quote = db.Column(
        db.String(500),
        nullable=False
    )

    spun_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc)
    )
