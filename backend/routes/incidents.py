<<<<<<< HEAD
﻿from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from extensions import db
from models import Incident, User, Resource
from utils.serializers import incident_to_dict
=======

"""Student incident reporting and incident management routes."""

from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from extensions import db
from models import Incident, Notification, Resource, User
from routes.admin import admin_required

>>>>>>> 6fbb0e6 (Add project planning architecture and test documentation)

incidents_bp = Blueprint("incidents", __name__)


<<<<<<< HEAD
# REPORT A NEW INCIDENT
@incidents_bp.route("/", methods=["POST"])
@jwt_required()
def report_incident():
    data = request.get_json() or {}
=======
def get_current_user():
    """Return the user associated with the current JWT."""
    user_id = get_jwt_identity()
    return db.session.get(User, int(user_id))


# ---------------- STUDENT INCIDENT REPORTING ----------------


@incidents_bp.route("/incidents", methods=["POST"])
@jwt_required()
def report_incident():
    """Allow a student to report an issue with a campus resource."""

    user = get_current_user()

    if user is None:
        return jsonify({"message": "User not found"}), 404

    if user.role.lower() != "student":
        return jsonify({
            "message": "Only students can report incidents"
        }), 403

    data = request.get_json(silent=True) or {}
>>>>>>> 6fbb0e6 (Add project planning architecture and test documentation)

    title = data.get("title")
    description = data.get("description")
    resource_id = data.get("resource_id")

<<<<<<< HEAD
    if not title or not description or not resource_id:
        return jsonify({
            "message": "title, description and resource_id are required"
=======
    if not isinstance(title, str) or not title.strip():
        return jsonify({
            "message": "A valid title is required"
        }), 400

    if len(title.strip()) > 150:
        return jsonify({
            "message": "Title cannot exceed 150 characters"
        }), 400

    if not isinstance(description, str) or not description.strip():
        return jsonify({
            "message": "A valid description is required"
>>>>>>> 6fbb0e6 (Add project planning architecture and test documentation)
        }), 400

    try:
        resource_id = int(resource_id)
<<<<<<< HEAD
    except (ValueError, TypeError):
        return jsonify({"message": "Invalid resource_id"}), 400

    resource = db.session.get(Resource, resource_id)

    if not resource:
        return jsonify({"message": "Resource not found"}), 404

    if not resource.is_active:
        return jsonify({"message": "Cannot report an incident for an inactive resource"}), 400

    user_id = int(get_jwt_identity())

    incident = Incident(
        user_id=user_id,
        resource_id=resource_id,
        title=title,
        description=description,
        status="reported",
    )

    db.session.add(incident)
    db.session.commit()

    return jsonify({
        "message": "Incident reported successfully",
        "incident": incident_to_dict(incident),
    }), 201


# VIEW MY REPORTED INCIDENTS
@incidents_bp.route("/my", methods=["GET"])
@jwt_required()
def get_my_incidents():
    user_id = int(get_jwt_identity())

    incidents = (
        Incident.query
        .filter_by(user_id=user_id)
=======
    except (TypeError, ValueError):
        return jsonify({
            "message": "A valid resource_id is required"
        }), 400

    resource = db.session.get(Resource, resource_id)

    if resource is None or not resource.is_active:
        return jsonify({
            "message": "Active resource not found"
        }), 404

    incident = Incident(
        user_id=user.user_id,
        resource_id=resource.resource_id,
        title=title.strip(),
        description=description.strip(),
        status="reported"
    )

    try:
        db.session.add(incident)
        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify({
            "message": "Could not report incident"
        }), 500

    return jsonify({
        "message": "Incident reported successfully",
        "incident": {
            "incident_id": incident.incident_id,
            "resource_id": incident.resource_id,
            "resource_name": resource.resource_name,
            "title": incident.title,
            "description": incident.description,
            "status": incident.status,
            "created_at": incident.created_at.isoformat()
        }
    }), 201


# ---------------- STUDENT INCIDENT HISTORY ----------------


@incidents_bp.route("/incidents/my", methods=["GET"])
@jwt_required()
def my_incidents():
    """Show only the signed-in student's incident reports."""

    user = get_current_user()

    if user is None:
        return jsonify({"message": "User not found"}), 404

    if user.role.lower() != "student":
        return jsonify({
            "message": "Only students can view student incidents"
        }), 403

    incidents = (
        db.session.query(Incident, Resource)
        .join(Resource, Incident.resource_id == Resource.resource_id)
        .filter(Incident.user_id == user.user_id)
>>>>>>> 6fbb0e6 (Add project planning architecture and test documentation)
        .order_by(Incident.created_at.desc())
        .all()
    )

<<<<<<< HEAD
    return jsonify([
        incident_to_dict(incident) for incident in incidents
    ]), 200


# VIEW ONE INCIDENT
@incidents_bp.route("/<int:incident_id>", methods=["GET"])
@jwt_required()
def get_incident(incident_id):
    user_id = int(get_jwt_identity())

    incident = db.session.get(Incident, incident_id)

    if not incident:
        return jsonify({"message": "Incident not found"}), 404

    user = db.session.get(User, user_id)

    if not user:
        return jsonify({"message": "User not found"}), 404

    if incident.user_id != user_id and user.role != "admin":
        return jsonify({"message": "Access denied"}), 403

    return jsonify(incident_to_dict(incident)), 200
=======
    result = []

    for incident, resource in incidents:
        result.append({
            "incident_id": incident.incident_id,
            "resource_id": incident.resource_id,
            "resource_name": resource.resource_name,
            "title": incident.title,
            "description": incident.description,
            "status": incident.status,
            "created_at": incident.created_at.isoformat()
        })

    return jsonify(result), 200


# ---------------- ADMIN INCIDENT MANAGEMENT ----------------


@incidents_bp.route("/admin/incidents", methods=["GET"])
@admin_required
def admin_view_incidents():
    """Allow admins to view all reported incidents."""

    incidents = (
        db.session.query(Incident, User, Resource)
        .join(User, Incident.user_id == User.user_id)
        .join(Resource, Incident.resource_id == Resource.resource_id)
        .order_by(Incident.created_at.desc())
        .all()
    )

    result = []

    for incident, student, resource in incidents:
        result.append({
            "incident_id": incident.incident_id,
            "student_id": student.user_id,
            "student_name": student.name,
            "student_email": student.email,
            "resource_id": resource.resource_id,
            "resource_name": resource.resource_name,
            "title": incident.title,
            "description": incident.description,
            "status": incident.status,
            "created_at": incident.created_at.isoformat()
        })

    return jsonify(result), 200


# ---------------- ADMIN INCIDENT STATUS UPDATE ----------------


@incidents_bp.route(
    "/admin/incidents/<int:incident_id>/status",
    methods=["PATCH"]
)
@admin_required
def admin_update_incident_status(incident_id):
    """Update incident status and notify the reporting student."""

    incident = db.session.get(Incident, incident_id)

    if incident is None:
        return jsonify({
            "message": "Incident not found"
        }), 404

    data = request.get_json(silent=True) or {}
    status = data.get("status")

    allowed_statuses = {
        "reported",
        "in_progress",
        "resolved"
    }

    if not isinstance(status, str) or status not in allowed_statuses:
        return jsonify({
            "message": "Invalid status",
            "allowed_statuses": sorted(allowed_statuses)
        }), 400

    old_status = incident.status

    # Create a notification only when the status actually changes.
    if old_status != status:
        notification = Notification(
            user_id=incident.user_id,
            message=(
                f'Your incident report #{incident.incident_id} '
                f'status changed to "{status}".'
            ),
            notification_type="incident",
            related_type="incident",
            related_id=incident.incident_id
        )

        db.session.add(notification)

    incident.status = status

    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify({
            "message": "Could not update incident status"
        }), 500

    return jsonify({
        "message": "Incident status updated successfully",
        "incident_id": incident.incident_id,
        "status": incident.status
    }), 200
>>>>>>> 6fbb0e6 (Add project planning architecture and test documentation)
