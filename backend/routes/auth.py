
"""Authentication and user profile API routes."""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity
)
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash

from extensions import db
from models import User

auth_bp = Blueprint("auth", __name__)


# USER REGISTRATION
# pylint: disable=too-many-return-statements
@auth_bp.route("/register", methods=["POST"])
def register():
    """Register a new student or faculty account."""

    data = request.get_json()

    if not isinstance(data, dict):
        return jsonify({"error": "Invalid request data"}), 400

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    role = data.get("role", "student")

    if not all(isinstance(value, str) for value in [name, email, password, role]):
        return jsonify({"error": "Invalid field values"}), 400

    name = name.strip()
    email = email.strip().lower()
    role = role.strip().lower()

    if not name or not email or not password:
        return jsonify({"error": "All fields are required"}), 400

    if len(password) < 8:
        return jsonify({
            "error": "Password must contain at least 8 characters"
        }), 400

    if role not in ["student", "faculty"]:
        return jsonify({"error": "Invalid role"}), 400

    new_user = User(
        name=name,
        email=email,
        password_hash=generate_password_hash(password),
        role=role
    )

    try:
        db.session.add(new_user)
        db.session.commit()

        return jsonify({
            "message": "Registration successful",
            "user_id": new_user.user_id,
            "name": new_user.name,
            "email": new_user.email,
            "role": new_user.role
        }), 201

    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Email already registered"}), 409


# USER LOGIN
@auth_bp.route("/login", methods=["POST"])
def login():
    """Authenticate a user and return an access token."""

    data = request.get_json()

    if not isinstance(data, dict):
        return jsonify({"error": "Invalid request data"}), 400

    email = data.get("email")
    password = data.get("password")

    if not isinstance(email, str) or not isinstance(password, str):
        return jsonify({
            "error": "Email and password are required"
        }), 400

    email = email.strip().lower()

    if not email or not password:
        return jsonify({
            "error": "Email and password are required"
        }), 400

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({"error": "Invalid email or password"}), 401

    access_token = create_access_token(
        identity=str(user.user_id)
    )

    return jsonify({
        "message": "Login successful",
        "access_token": access_token,
        "user": {
            "user_id": user.user_id,
            "name": user.name,
            "email": user.email,
            "role": user.role
        }
    }), 200


# VIEW USER PROFILE
@auth_bp.route("/profile", methods=["GET"])
@jwt_required()
def profile():
    """Return the profile of the authenticated user."""

    user_id = get_jwt_identity()
    user = db.session.get(User, int(user_id))

    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "user_id": user.user_id,
        "name": user.name,
        "email": user.email,
        "role": user.role
    }), 200
