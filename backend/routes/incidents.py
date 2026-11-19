from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from extensions import db
from models import Incident, User, Resource
from utils.serializers import incident_to_dict

incidents_bp = Blueprint("incidents", __name__)


# REPORT A NEW INCIDENT
@incidents_bp.route("/", methods=["POST"])
@jwt_required()
def report_incident():
    data = request.get_json() or {}

    title = data.get("title")
    description = data.get("description")
    resource_id = data.get("resource_id")

    if not title or not description or not resource_id:
        return jsonify({
            "message": "title, description and resource_id are required"
        }), 400

    try:
        resource_id = int(resource_id)
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
        .order_by(Incident.created_at.desc())
        .all()
    )

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
