
import pytest
from datetime import date, time

from flask import Flask
from flask_jwt_extended import create_access_token

from extensions import db, jwt
from models import User, Resource, Booking
from routes.admin import admin_bp


@pytest.fixture
def booking_admin_client():
    app = Flask(__name__)

    app.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI="sqlite:///:memory:",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        JWT_SECRET_KEY="test-booking-admin-secret-for-tests-2026"
    )

    db.init_app(app)
    jwt.init_app(app)

    app.register_blueprint(admin_bp, url_prefix="/api/admin")

    with app.app_context():
        db.create_all()

        admin = User(
            name="Admin",
            email="admin_booking@example.com",
            password_hash="test-hash",
            role="admin"
        )

        student = User(
            name="Student",
            email="student_booking@example.com",
            password_hash="test-hash",
            role="student"
        )

        resource = Resource(
            resource_name="Computer Lab",
            resource_type="Laboratory",
            location="Block A",
            description="Test lab",
            is_active=True
        )

        db.session.add_all([admin, student, resource])
        db.session.commit()

        booking1 = Booking(
            user_id=student.user_id,
            resource_id=resource.resource_id,
            booking_date=date(2026, 11, 20),
            start_time=time(10, 0),
            end_time=time(11, 0),
            status="pending"
        )

        booking2 = Booking(
            user_id=student.user_id,
            resource_id=resource.resource_id,
            booking_date=date(2026, 11, 20),
            start_time=time(10, 30),
            end_time=time(11, 30),
            status="pending"
        )

        db.session.add_all([booking1, booking2])
        db.session.commit()

        admin_token = create_access_token(
            identity=str(admin.user_id)
        )

        student_token = create_access_token(
            identity=str(student.user_id)
        )

        yield (
            app.test_client(),
            admin_token,
            student_token,
            booking1.booking_id,
            booking2.booking_id
        )

        db.session.remove()
        db.drop_all()


def test_admin_view_bookings(booking_admin_client):
    client, admin_token, _, _, _ = booking_admin_client

    response = client.get(
        "/api/admin/bookings",
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    assert response.status_code == 200
    assert len(response.json) == 2


def test_admin_approve_booking(booking_admin_client):
    client, admin_token, _, booking_id, _ = booking_admin_client

    response = client.patch(
        f"/api/admin/bookings/{booking_id}/approve",
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    assert response.status_code == 200
    assert response.json["status"] == "approved"


def test_admin_reject_booking(booking_admin_client):
    client, admin_token, _, _, booking_id = booking_admin_client

    response = client.patch(
        f"/api/admin/bookings/{booking_id}/reject",
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    assert response.status_code == 200
    assert response.json["status"] == "rejected"


def test_cannot_approve_already_processed_booking(booking_admin_client):
    client, admin_token, _, booking_id, _ = booking_admin_client

    headers = {"Authorization": f"Bearer {admin_token}"}

    first = client.patch(
        f"/api/admin/bookings/{booking_id}/approve",
        headers=headers
    )

    second = client.patch(
        f"/api/admin/bookings/{booking_id}/approve",
        headers=headers
    )

    assert first.status_code == 200
    assert second.status_code == 409


def test_prevent_overlapping_approved_bookings(booking_admin_client):
    client, admin_token, _, booking1_id, booking2_id = booking_admin_client

    headers = {"Authorization": f"Bearer {admin_token}"}

    first = client.patch(
        f"/api/admin/bookings/{booking1_id}/approve",
        headers=headers
    )

    second = client.patch(
        f"/api/admin/bookings/{booking2_id}/approve",
        headers=headers
    )

    assert first.status_code == 200
    assert second.status_code == 409


def test_student_cannot_manage_bookings(booking_admin_client):
    client, _, student_token, booking_id, _ = booking_admin_client

    response = client.patch(
        f"/api/admin/bookings/{booking_id}/approve",
        headers={"Authorization": f"Bearer {student_token}"}
    )

    assert response.status_code == 403
