import pytest
from flask import Flask
from extensions import db, jwt
from models import User
from routes.auth import auth_bp


@pytest.fixture
def client():
    test_app = Flask(__name__)

    test_app.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI="sqlite:///:memory:",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        JWT_SECRET_KEY="test-secret-key-for-pytest-2026-extra"
    )

    db.init_app(test_app)
    jwt.init_app(test_app)

    test_app.register_blueprint(
        auth_bp,
        url_prefix="/api/auth"
    )

    with test_app.app_context():
        db.create_all()

        yield test_app.test_client()

        db.session.remove()
        db.drop_all()


def test_user_registration(client):
    response = client.post(
        "/api/auth/register",
        json={
            "name": "Test Student",
            "email": "test@example.com",
            "password": "Student@123",
            "role": "student"
        }
    )

    assert response.status_code == 201
    assert response.json["message"] == "Registration successful"


def test_user_login(client):
    client.post(
        "/api/auth/register",
        json={
            "name": "Test Student",
            "email": "test@example.com",
            "password": "Student@123",
            "role": "student"
        }
    )

    response = client.post(
        "/api/auth/login",
        json={
            "email": "test@example.com",
            "password": "Student@123"
        }
    )

    assert response.status_code == 200
    assert "access_token" in response.json


def test_login_with_wrong_password(client):
    client.post(
        "/api/auth/register",
        json={
            "name": "Test Student",
            "email": "test@example.com",
            "password": "Student@123",
            "role": "student"
        }
    )

    response = client.post(
        "/api/auth/login",
        json={
            "email": "test@example.com",
            "password": "WrongPassword123"
        }
    )

    assert response.status_code == 401