
import pytest
from datetime import date, time

from flask import Flask
from flask_jwt_extended import create_access_token

from extensions import db, jwt
from models import User, Resource, Booking, Incident, Notification
from routes.admin import admin_bp
from routes.incidents import incidents_bp
from routes.notifications import notifications_bp


@pytest.fixture
def notification_client():
    """Create an isolated test database and test users."""

    app = Flask(__name__)

    app.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI="sqlite:///:memory:",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        JWT_SECRET_KEY="notification-testing-secret-key-2026"
    )

    db.init_app(app)
    jwt.init_app(app)

    app.register_blueprint(admin_bp, url_prefix="/api/admin")
    app.register_blueprint(incidents_bp, url_prefix="/api")
    app.register_blueprint(
        notifications_bp,
        url_prefix="/api/notifications"
    )

    with app.app_context():
        db.create_all()

        admin = User(
            name="Admin",
            email="notification_admin@example.com",
            password_hash="test-hash",
            role="admin"
        )

        student1 = User(
            name="Student One",
            email="notification_student1@example.com",
            password_hash="test-hash",
            role="student"
        )

        student2 = User(
            name="Student Two",
            email="notification_student2@example.com",
            password_hash="test-hash",
            role="student"
        )

        resource = Resource(
            resource_name="Computer Lab",
            resource_type="Laboratory",
            location="Block A",
            description="Test laboratory",
            is_active=True
        )

        db.session.add_all([
            admin,
            student1,
            student2,
            resource
        ])
        db.session.commit()

        booking1 = Booking(
            user_id=student1.user_id,
            resource_id=resource.resource_id,
            booking_date=date(2026, 11, 20),
            start_time=time(10, 0),
            end_time=time(11, 0),
            status="pending"
        )

        booking2 = Booking(
            user_id=student1.user_id,
            resource_id=resource.resource_id,
            booking_date=date(2026, 11, 20),
            start_time=time(12, 0),
            end_time=time(13, 0),
            status="pending"
        )

        incident = Incident(
            user_id=student1.user_id,
            resource_id=resource.resource_id,
            title="Projector issue",
            description="The projector is not working.",
            status="reported"
        )

        db.session.add_all([
            booking1,
            booking2,
            incident
        ])
        db.session.commit()

        notification1 = Notification(
            user_id=student1.user_id,
            message="Your first test notification.",
            notification_type="booking",
            related_type="booking",
            related_id=booking1.booking_id
        )

        notification2 = Notification(
            user_id=student1.user_id,
            message="Your second test notification.",
            notification_type="incident",
            related_type="incident",
            related_id=incident.incident_id
        )

        other_notification = Notification(
            user_id=student2.user_id,
            message="Another student's notification.",
            notification_type="booking",
            related_type="booking",
            related_id=booking1.booking_id
        )

        db.session.add_all([
            notification1,
            notification2,
            other_notification
        ])
        db.session.commit()

        admin_token = create_access_token(
            identity=str(admin.user_id)
        )

        student1_token = create_access_token(
            identity=str(student1.user_id)
        )

        student2_token = create_access_token(
            identity=str(student2.user_id)
        )

        yield (
            app.test_client(),
            admin_token,
            student1_token,
            student2_token,
            booking1.booking_id,
            booking2.booking_id,
            incident.incident_id,
            notification1.notification_id,
            other_notification.notification_id
        )

        db.session.remove()
        db.drop_all()


def test_student_can_view_own_notifications(notification_client):
    client, _, student_token, _, _, _, _, _, _ = notification_client

    response = client.get(
        "/api/notifications/",
        headers={"Authorization": f"Bearer {student_token}"}
    )

    assert response.status_code == 200
    assert len(response.json["notifications"]) == 2
    assert response.json["unread_count"] == 2


def test_student_can_mark_notification_as_read(notification_client):
    client, _, student_token, _, _, _, _, notification_id, _ = (
        notification_client
    )

    response = client.patch(
        f"/api/notifications/{notification_id}/read",
        headers={"Authorization": f"Bearer {student_token}"}
    )

    assert response.status_code == 200
    assert response.json["is_read"] is True


def test_student_cannot_mark_another_students_notification(
    notification_client
):
    client, _, student_token, _, _, _, _, _, other_notification_id = (
        notification_client
    )

    response = client.patch(
        f"/api/notifications/{other_notification_id}/read",
        headers={"Authorization": f"Bearer {student_token}"}
    )

    assert response.status_code == 404


def test_student_can_mark_all_notifications_as_read(notification_client):
    client, _, student_token, _, _, _, _, _, _ = notification_client

    response = client.patch(
        "/api/notifications/read-all",
        headers={"Authorization": f"Bearer {student_token}"}
    )

    assert response.status_code == 200

    check_response = client.get(
        "/api/notifications/",
        headers={"Authorization": f"Bearer {student_token}"}
    )

    assert check_response.json["unread_count"] == 0


def test_booking_approval_creates_notification(notification_client):
    client, admin_token, student_token, _, booking_id, _, _, _, _ = (
        notification_client
    )

    response = client.patch(
        f"/api/admin/bookings/{booking_id}/approve",
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    assert response.status_code == 200

    notification_response = client.get(
        "/api/notifications/",
        headers={"Authorization": f"Bearer {student_token}"}
    )

    messages = [
        item["message"]
        for item in notification_response.json["notifications"]
    ]

    assert any(
        f"#{booking_id}" in message and "approved" in message
        for message in messages
    )


def test_booking_rejection_creates_notification(notification_client):
    client, admin_token, student_token, _, _, booking_id, _, _, _ = (
        notification_client
    )

    response = client.patch(
        f"/api/admin/bookings/{booking_id}/reject",
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    assert response.status_code == 200

    notification_response = client.get(
        "/api/notifications/",
        headers={"Authorization": f"Bearer {student_token}"}
    )

    messages = [
        item["message"]
        for item in notification_response.json["notifications"]
    ]

    assert any(
        f"#{booking_id}" in message and "rejected" in message
        for message in messages
    )


def test_incident_status_change_creates_notification(notification_client):
    client, admin_token, student_token, _, _, _, incident_id, _, _ = (
        notification_client
    )

    response = client.patch(
        f"/api/admin/incidents/{incident_id}/status",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={"status": "in_progress"}
    )

    assert response.status_code == 200

    notification_response = client.get(
        "/api/notifications/",
        headers={"Authorization": f"Bearer {student_token}"}
    )

    messages = [
        item["message"]
        for item in notification_response.json["notifications"]
    ]

    assert any(
        f"#{incident_id}" in message and "in_progress" in message
        for message in messages
    )


def test_same_incident_status_does_not_create_duplicate_notification(
    notification_client
):
    client, admin_token, student_token, _, _, _, incident_id, _, _ = (
        notification_client
    )

    headers = {"Authorization": f"Bearer {admin_token}"}

    first_response = client.patch(
        f"/api/admin/incidents/{incident_id}/status",
        headers=headers,
        json={"status": "in_progress"}
    )

    assert first_response.status_code == 200

    second_response = client.patch(
        f"/api/admin/incidents/{incident_id}/status",
        headers=headers,
        json={"status": "in_progress"}
    )

    assert second_response.status_code == 200

    notification_response = client.get(
        "/api/notifications/",
        headers={"Authorization": f"Bearer {student_token}"}
    )

    incident_notifications = [
        item for item in notification_response.json["notifications"]
        if item["related_type"] == "incident"
        and item["related_id"] == incident_id
    ]

    assert len(incident_notifications) == 2
    # One original notification plus exactly one status-change notification.
