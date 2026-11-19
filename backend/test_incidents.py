<<<<<<< HEAD
﻿import pytest

from flask import Flask
from flask_jwt_extended import JWTManager, create_access_token

from extensions import db
=======

import pytest

from flask import Flask
from flask_jwt_extended import create_access_token

from extensions import db, jwt
>>>>>>> 6fbb0e6 (Add project planning architecture and test documentation)
from models import User, Resource, Incident
from routes.incidents import incidents_bp


@pytest.fixture
<<<<<<< HEAD
def incident_setup():
    test_app = Flask(__name__)
    test_app.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI="sqlite:///:memory:",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        JWT_SECRET_KEY="test-secret-key-for-incident-tests-2026"
    )

    db.init_app(test_app)
    jwt = JWTManager(test_app)

    test_app.register_blueprint(
        incidents_bp,
        url_prefix="/api/incidents"
    )

    with test_app.app_context():
        db.create_all()

        student = User(
            name="Test Student",
            email="student@test.com",
            password_hash="test-hash",
            role="student"
        )

        another_student = User(
            name="Another Student",
            email="another@test.com",
            password_hash="test-hash",
            role="student"
        )

        admin = User(
            name="Test Admin",
            email="admin@test.com",
=======
def incident_client():
    app = Flask(__name__)

    app.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI="sqlite:///:memory:",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        JWT_SECRET_KEY="incident-testing-secret-key-long-enough-2026"
    )

    db.init_app(app)
    jwt.init_app(app)
    app.register_blueprint(incidents_bp, url_prefix="/api")

    with app.app_context():
        db.create_all()

        admin = User(
            name="Admin",
            email="incident_admin@example.com",
>>>>>>> 6fbb0e6 (Add project planning architecture and test documentation)
            password_hash="test-hash",
            role="admin"
        )

<<<<<<< HEAD
        db.session.add_all([student, another_student, admin])
        db.session.commit()
=======
        student1 = User(
            name="Student One",
            email="incident_student1@example.com",
            password_hash="test-hash",
            role="student"
        )

        student2 = User(
            name="Student Two",
            email="incident_student2@example.com",
            password_hash="test-hash",
            role="student"
        )
>>>>>>> 6fbb0e6 (Add project planning architecture and test documentation)

        resource = Resource(
            resource_name="Computer Lab",
            resource_type="Laboratory",
            location="Block A",
<<<<<<< HEAD
            description="Testing lab",
            is_active=True
        )

        inactive_resource = Resource(
            resource_name="Old Laboratory",
            resource_type="Laboratory",
            location="Block B",
            description="Inactive lab",
            is_active=False
        )

        db.session.add_all([resource, inactive_resource])
        db.session.commit()

        incident = Incident(
            user_id=student.user_id,
            resource_id=resource.resource_id,
            title="Projector issue",
            description="Projector is not working",
            status="reported"
        )

        db.session.add(incident)
        db.session.commit()

        student_token = create_access_token(
            identity=str(student.user_id)
        )
        another_student_token = create_access_token(
            identity=str(another_student.user_id)
        )
        admin_token = create_access_token(
            identity=str(admin.user_id)
        )

        yield (
            test_app.test_client(),
            student_token,
            another_student_token,
            admin_token,
            resource.resource_id,
            inactive_resource.resource_id,
            incident.incident_id
=======
            description="Test resource",
            is_active=True
        )

        db.session.add_all([admin, student1, student2, resource])
        db.session.commit()

        incident1 = Incident(
            user_id=student1.user_id,
            resource_id=resource.resource_id,
            title="Projector not working",
            description="The projector is not displaying anything.",
            status="reported"
        )

        incident2 = Incident(
            user_id=student2.user_id,
            resource_id=resource.resource_id,
            title="Computer issue",
            description="One computer is not starting.",
            status="in_progress"
        )

        db.session.add_all([incident1, incident2])
        db.session.commit()

        admin_token = create_access_token(identity=str(admin.user_id))
        student1_token = create_access_token(identity=str(student1.user_id))
        student2_token = create_access_token(identity=str(student2.user_id))

        yield (
            app.test_client(),
            admin_token,
            student1_token,
            student2_token,
            incident1.incident_id
>>>>>>> 6fbb0e6 (Add project planning architecture and test documentation)
        )

        db.session.remove()
        db.drop_all()


<<<<<<< HEAD
def test_report_incident(incident_setup):
    client, student_token, _, _, resource_id, _, _ = incident_setup

    response = client.post(
        "/api/incidents/",
        headers={"Authorization": f"Bearer {student_token}"},
        json={
            "resource_id": resource_id,
            "title": "Broken chair",
            "description": "One chair is damaged"
=======
def test_student_can_report_incident(incident_client):
    client, _, student_token, _, _ = incident_client

    response = client.post(
        "/api/incidents",
        headers={"Authorization": f"Bearer {student_token}"},
        json={
            "resource_id": 1,
            "title": "Air conditioner issue",
            "description": "The air conditioner is not working."
>>>>>>> 6fbb0e6 (Add project planning architecture and test documentation)
        }
    )

    assert response.status_code == 201
<<<<<<< HEAD
    assert response.json["incident"]["title"] == "Broken chair"
    assert response.json["incident"]["status"] == "reported"


def test_report_incident_without_required_fields(incident_setup):
    client, student_token, _, _, _, _, _ = incident_setup

    response = client.post(
        "/api/incidents/",
        headers={"Authorization": f"Bearer {student_token}"},
        json={"title": "Missing details"}
    )

    assert response.status_code == 400


def test_report_incident_for_invalid_resource(incident_setup):
    client, student_token, _, _, _, _, _ = incident_setup

    response = client.post(
        "/api/incidents/",
        headers={"Authorization": f"Bearer {student_token}"},
        json={
            "resource_id": 9999,
            "title": "Test issue",
            "description": "Testing invalid resource"
        }
    )

    assert response.status_code == 404


def test_report_incident_for_inactive_resource(incident_setup):
    client, student_token, _, _, _, inactive_id, _ = incident_setup

    response = client.post(
        "/api/incidents/",
        headers={"Authorization": f"Bearer {student_token}"},
        json={
            "resource_id": inactive_id,
            "title": "Test issue",
            "description": "Testing inactive resource"
=======
    assert response.json["incident"]["title"] == "Air conditioner issue"
    assert response.json["incident"]["status"] == "reported"


def test_student_cannot_submit_incident_without_title(incident_client):
    client, _, student_token, _, _ = incident_client

    response = client.post(
        "/api/incidents",
        headers={"Authorization": f"Bearer {student_token}"},
        json={
            "resource_id": 1,
            "description": "There is a problem with the resource."
>>>>>>> 6fbb0e6 (Add project planning architecture and test documentation)
        }
    )

    assert response.status_code == 400


<<<<<<< HEAD
def test_view_my_incidents(incident_setup):
    client, student_token, _, _, _, _, _ = incident_setup

    response = client.get(
        "/api/incidents/my",
        headers={"Authorization": f"Bearer {student_token}"}
=======
def test_student_can_view_only_own_incidents(incident_client):
    client, _, student1_token, _, _ = incident_client

    response = client.get(
        "/api/incidents/my",
        headers={"Authorization": f"Bearer {student1_token}"}
>>>>>>> 6fbb0e6 (Add project planning architecture and test documentation)
    )

    assert response.status_code == 200
    assert len(response.json) == 1
<<<<<<< HEAD
    assert response.json[0]["title"] == "Projector issue"


def test_view_own_incident(incident_setup):
    client, student_token, _, _, _, _, incident_id = incident_setup

    response = client.get(
        f"/api/incidents/{incident_id}",
        headers={"Authorization": f"Bearer {student_token}"}
    )

    assert response.status_code == 200
    assert response.json["incident_id"] == incident_id


def test_student_cannot_view_another_students_incident(incident_setup):
    client, _, another_token, _, _, _, incident_id = incident_setup

    response = client.get(
        f"/api/incidents/{incident_id}",
        headers={"Authorization": f"Bearer {another_token}"}
=======
    assert response.json[0]["title"] == "Projector not working"


def test_admin_can_view_all_incidents(incident_client):
    client, admin_token, _, _, _ = incident_client

    response = client.get(
        "/api/admin/incidents",
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    assert response.status_code == 200
    assert len(response.json) == 2


def test_admin_can_update_incident_status(incident_client):
    client, admin_token, _, _, incident_id = incident_client

    response = client.patch(
        f"/api/admin/incidents/{incident_id}/status",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={"status": "in_progress"}
    )

    assert response.status_code == 200
    assert response.json["status"] == "in_progress"


def test_admin_cannot_set_invalid_incident_status(incident_client):
    client, admin_token, _, _, incident_id = incident_client

    response = client.patch(
        f"/api/admin/incidents/{incident_id}/status",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={"status": "random_status"}
    )

    assert response.status_code == 400


def test_student_cannot_view_all_admin_incidents(incident_client):
    client, _, student_token, _, _ = incident_client

    response = client.get(
        "/api/admin/incidents",
        headers={"Authorization": f"Bearer {student_token}"}
>>>>>>> 6fbb0e6 (Add project planning architecture and test documentation)
    )

    assert response.status_code == 403


<<<<<<< HEAD
def test_admin_can_view_another_students_incident(incident_setup):
    client, _, _, admin_token, _, _, incident_id = incident_setup

    response = client.get(
        f"/api/incidents/{incident_id}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    assert response.status_code == 200


def test_incident_not_found(incident_setup):
    client, student_token, _, _, _, _, _ = incident_setup

    response = client.get(
        "/api/incidents/9999",
        headers={"Authorization": f"Bearer {student_token}"}
    )

    assert response.status_code == 404
=======
def test_student_cannot_update_incident_status(incident_client):
    client, _, student_token, _, incident_id = incident_client

    response = client.patch(
        f"/api/admin/incidents/{incident_id}/status",
        headers={"Authorization": f"Bearer {student_token}"},
        json={"status": "resolved"}
    )

    assert response.status_code == 403


def test_admin_cannot_use_student_incident_endpoint(incident_client):
    client, admin_token, _, _, _ = incident_client

    response = client.get(
        "/api/incidents/my",
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    assert response.status_code == 403
>>>>>>> 6fbb0e6 (Add project planning architecture and test documentation)
