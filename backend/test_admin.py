<<<<<<< HEAD
﻿import pytest
from datetime import date, time

from flask import Flask
from flask_jwt_extended import JWTManager, create_access_token

from extensions import db
from models import User, Resource, Booking, Incident
from routes.admin import admin_bp


@pytest.fixture
def admin_setup():
    test_app = Flask(__name__)
=======

import pytest
from flask import Flask
from extensions import db, jwt
from models import User, Resource
from routes.admin import admin_bp
from flask_jwt_extended import create_access_token


@pytest.fixture
def admin_client():
    test_app = Flask(__name__)

>>>>>>> 6fbb0e6 (Add project planning architecture and test documentation)
    test_app.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI="sqlite:///:memory:",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
<<<<<<< HEAD
        JWT_SECRET_KEY="test-secret-key-for-admin-tests-2026"
    )

    db.init_app(test_app)
    jwt = JWTManager(test_app)

    test_app.register_blueprint(admin_bp, url_prefix="/api/admin")
=======
        JWT_SECRET_KEY="test-admin-secret-for-pytest-2026"
    )

    db.init_app(test_app)
    jwt.init_app(test_app)

    test_app.register_blueprint(
        admin_bp,
        url_prefix="/api/admin"
    )
>>>>>>> 6fbb0e6 (Add project planning architecture and test documentation)

    with test_app.app_context():
        db.create_all()

        admin = User(
            name="Test Admin",
<<<<<<< HEAD
            email="admin@test.com",
=======
            email="admin@example.com",
>>>>>>> 6fbb0e6 (Add project planning architecture and test documentation)
            password_hash="test-hash",
            role="admin"
        )

        student = User(
            name="Test Student",
<<<<<<< HEAD
            email="student@test.com",
=======
            email="student@example.com",
>>>>>>> 6fbb0e6 (Add project planning architecture and test documentation)
            password_hash="test-hash",
            role="student"
        )

<<<<<<< HEAD
        db.session.add_all([admin, student])
        db.session.commit()

        resource = Resource(
            resource_name="Computer Lab",
            resource_type="Laboratory",
            location="Block A",
            description="Testing lab",
            is_active=True
        )

        db.session.add(resource)
        db.session.commit()

        booking = Booking(
            user_id=student.user_id,
            resource_id=resource.resource_id,
            booking_date=date(2026, 12, 1),
            start_time=time(10, 0),
            end_time=time(11, 0),
            status="pending"
        )

        incident = Incident(
            user_id=student.user_id,
            resource_id=resource.resource_id,
            title="Projector issue",
            description="Projector is not working",
            status="reported"
        )

        db.session.add_all([booking, incident])
=======
        resource = Resource(
            resource_name="Computer Lab 1",
            resource_type="Laboratory",
            location="Block A",
            description="Testing resource",
            is_active=True
        )

        db.session.add_all([admin, student, resource])
>>>>>>> 6fbb0e6 (Add project planning architecture and test documentation)
        db.session.commit()

        admin_token = create_access_token(
            identity=str(admin.user_id)
        )
<<<<<<< HEAD
=======

>>>>>>> 6fbb0e6 (Add project planning architecture and test documentation)
        student_token = create_access_token(
            identity=str(student.user_id)
        )

        yield (
            test_app.test_client(),
            admin_token,
<<<<<<< HEAD
            student_token,
            resource.resource_id,
            booking.booking_id,
            incident.incident_id
=======
            student_token
>>>>>>> 6fbb0e6 (Add project planning architecture and test documentation)
        )

        db.session.remove()
        db.drop_all()


<<<<<<< HEAD
def test_admin_dashboard(admin_setup):
    client, admin_token, _, _, _, _ = admin_setup

    response = client.get(
        "/api/admin/dashboard",
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    assert response.status_code == 200
    assert response.json["total_users"] == 2
    assert response.json["total_resources"] == 1
    assert response.json["total_bookings"] == 1
    assert response.json["total_incidents"] == 1


def test_student_cannot_access_admin_dashboard(admin_setup):
    client, _, student_token, _, _, _ = admin_setup

    response = client.get(
        "/api/admin/dashboard",
        headers={"Authorization": f"Bearer {student_token}"}
    )

    assert response.status_code == 403


def test_admin_can_view_resources(admin_setup):
    client, admin_token, _, _, _, _ = admin_setup
=======
def test_admin_view_resources(admin_client):
    client, admin_token, _ = admin_client
>>>>>>> 6fbb0e6 (Add project planning architecture and test documentation)

    response = client.get(
        "/api/admin/resources",
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    assert response.status_code == 200
    assert len(response.json) == 1


<<<<<<< HEAD
def test_admin_can_create_resource(admin_setup):
    client, admin_token, _, _, _, _ = admin_setup

    response = client.post(
        "/api/admin/resources",
        headers={"Authorization": f"Bearer {admin_token}"},
=======
def test_admin_add_resource(admin_client):
    client, admin_token, _ = admin_client

    response = client.post(
        "/api/admin/resources",
>>>>>>> 6fbb0e6 (Add project planning architecture and test documentation)
        json={
            "resource_name": "Seminar Hall",
            "resource_type": "Hall",
            "location": "Block B",
            "description": "Main seminar hall"
<<<<<<< HEAD
        }
    )

    assert response.status_code == 201
    assert response.json["resource"]["resource_name"] == "Seminar Hall"


def test_admin_can_update_resource(admin_setup):
    client, admin_token, _, resource_id, _, _ = admin_setup

    response = client.put(
        f"/api/admin/resources/{resource_id}",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={"resource_name": "Updated Computer Lab"}
    )

    assert response.status_code == 200
    assert response.json["resource"]["resource_name"] == "Updated Computer Lab"


def test_admin_can_deactivate_resource(admin_setup):
    client, admin_token, _, resource_id, _, _ = admin_setup

    response = client.patch(
        f"/api/admin/resources/{resource_id}/status",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={"is_active": False}
    )

    assert response.status_code == 200
    assert response.json["resource"]["is_active"] is False


def test_admin_can_approve_booking(admin_setup):
    client, admin_token, _, _, booking_id, _ = admin_setup

    response = client.patch(
        f"/api/admin/bookings/{booking_id}/approve",
=======
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    assert response.status_code == 201
    assert response.json["message"] == "Resource created successfully"


def test_admin_update_resource(admin_client):
    client, admin_token, _ = admin_client

    response = client.patch(
        "/api/admin/resources/1",
        json={"resource_name": "Updated Computer Lab"},
>>>>>>> 6fbb0e6 (Add project planning architecture and test documentation)
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    assert response.status_code == 200
<<<<<<< HEAD
    assert response.json["booking"]["status"] == "approved"


def test_admin_can_update_incident_status(admin_setup):
    client, admin_token, _, _, _, incident_id = admin_setup

    response = client.patch(
        f"/api/admin/incidents/{incident_id}/status",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={"status": "in_progress"}
    )

    assert response.status_code == 200
    assert response.json["incident"]["status"] == "in_progress"
=======


def test_admin_deactivate_resource(admin_client):
    client, admin_token, _ = admin_client

    response = client.delete(
        "/api/admin/resources/1",
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    assert response.status_code == 200
    assert response.json["message"] == "Resource deactivated successfully"


def test_student_cannot_access_admin_resources(admin_client):
    client, _, student_token = admin_client

    response = client.get(
        "/api/admin/resources",
        headers={"Authorization": f"Bearer {student_token}"}
    )

    assert response.status_code == 403
>>>>>>> 6fbb0e6 (Add project planning architecture and test documentation)
