import pytest
from flask import Flask
from extensions import db, jwt
from models import User, Resource
from routes.bookings import bookings_bp
from flask_jwt_extended import create_access_token

@pytest.fixture
def client():
    test_app = Flask(__name__)

    test_app.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI="sqlite:///:memory:",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        JWT_SECRET_KEY="test-secret-key-for-pytest-2026-extra"    )

    db.init_app(test_app)
    jwt.init_app(test_app)

    test_app.register_blueprint(
        bookings_bp,
        url_prefix="/api/bookings"
    )

    with test_app.app_context():
        db.create_all()

        user = User(
            name="Test Student",
            email="test@example.com",
            password_hash="test-hash",
            role="student"
        )

        resource = Resource(
            resource_name="Computer Lab 1",
            resource_type="Laboratory",
            location="Block A",
            description="Testing resource",
            is_active=True
        )

        db.session.add_all([user, resource])
        db.session.commit()

        token = create_access_token(
            identity=str(user.user_id)
        )

        yield test_app.test_client(), token

        db.session.remove()
        db.drop_all()

def test_create_booking(client):
    test_client, token = client

    response = test_client.post(
        "/api/bookings/",
        json={
            "resource_id": 1,
            "booking_date": "2026-11-20",
            "start_time": "10:00",
            "end_time": "11:00"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 201
    assert response.json["booking"]["status"] == "pending"


def test_prevent_overlapping_booking(client):
    test_client, token = client

    headers = {"Authorization": f"Bearer {token}"}

    booking = {
        "resource_id": 1,
        "booking_date": "2026-11-20",
        "start_time": "10:00",
        "end_time": "11:00"
    }

    first = test_client.post(
        "/api/bookings/", json=booking, headers=headers
    )

    second = test_client.post(
        "/api/bookings/", json=booking, headers=headers
    )

    assert first.status_code == 201
    assert second.status_code == 409


def test_view_booking_history(client):
    test_client, token = client

    test_client.post(
        "/api/bookings/",
        json={
            "resource_id": 1,
            "booking_date": "2026-11-20",
            "start_time": "10:00",
            "end_time": "11:00"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    response = test_client.get(
        "/api/bookings/my",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert len(response.json) == 1


def test_cancel_booking(client):
    test_client, token = client

    headers = {"Authorization": f"Bearer {token}"}

    response = test_client.post(
        "/api/bookings/",
        json={
            "resource_id": 1,
            "booking_date": "2026-11-20",
            "start_time": "10:00",
            "end_time": "11:00"
        },
        headers=headers
    )

    booking_id = response.json["booking"]["booking_id"]

    cancel = test_client.delete(
        f"/api/bookings/{booking_id}",
        headers=headers
    )

    assert cancel.status_code == 200
    assert cancel.json["status"] == "cancelled"
