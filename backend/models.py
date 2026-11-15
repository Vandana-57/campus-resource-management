"""Database models for users, resources, bookings and incidents."""

# pylint: disable=too-few-public-methods

from datetime import datetime, timezone
from extensions import db


class User(db.Model):
    """Stores student, faculty and admin account details."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.Text, nullable=False)
    role = db.Column(db.String(20), nullable=False)
    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc).replace(tzinfo=None)
    )


class Resource(db.Model):
    """Stores campus resource information."""

    __tablename__ = "resources"

    resource_id = db.Column(db.Integer, primary_key=True)
    resource_name = db.Column(db.String(100), nullable=False)
    resource_type = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(150))
    description = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)


class Booking(db.Model):
    """Stores resource booking requests and their status."""

    __tablename__ = "bookings"

    booking_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.user_id"),
        nullable=False
    )
    resource_id = db.Column(
        db.Integer,
        db.ForeignKey("resources.resource_id"),
        nullable=False
    )
    booking_date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    status = db.Column(db.String(20), default="pending")
    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc).replace(tzinfo=None)
    )


class Incident(db.Model):
    """Stores reported resource issues and their status."""

    __tablename__ = "incidents"

    incident_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.user_id"),
        nullable=False
    )
    resource_id = db.Column(
        db.Integer,
        db.ForeignKey("resources.resource_id"),
        nullable=False
    )
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default="reported")
    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc).replace(tzinfo=None)
    )
