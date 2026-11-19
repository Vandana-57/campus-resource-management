from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from extensions import db
from models import User, Resource, Booking, Incident, Notification
from utils.decorators import admin_required
from utils.serializers import (
    resource_to_dict,
    booking_to_dict,
    incident_to_dict,
)

admin_bp = Blueprint("admin", __name__)


# ADMIN DASHBOARD
@admin_bp.route("/dashboard", methods=["GET"])
@jwt_required()
@admin_required
def dashboard():
    return jsonify({
        "total_users": User.query.count(),
        "total_resources": Resource.query.count(),
        "total_bookings": Booking.query.count(),
        "pending_bookings": Booking.query.filter_by(
            status="pending"
        ).count(),
        "total_incidents": Incident.query.count(),
    }), 200


# RESOURCE MANAGEMENT
@admin_bp.route("/resources", methods=["GET"])
@jwt_required()
@admin_required
def get_resources():
    resources = Resource.query.all()
    return jsonify([resource_to_dict(r) for r in resources]), 200


@admin_bp.route("/resources", methods=["POST"])
@jwt_required()
@admin_required
def create_resource():
    data = request.get_json() or {}

    resource_name = data.get("resource_name")
    resource_type = data.get("resource_type")

    if not resource_name or not resource_type:
        return jsonify({
            "message": "resource_name and resource_type are required"
        }), 400

    resource = Resource(
        resource_name=resource_name,
        resource_type=resource_type,
        location=data.get("location"),
        description=data.get("description"),
        is_active=data.get("is_active", True),
    )

    db.session.add(resource)
    db.session.commit()

    return jsonify({
        "message": "Resource created successfully",
        "resource": resource_to_dict(resource),
    }), 201


@admin_bp.route("/resources/<int:resource_id>", methods=["PUT"])
@jwt_required()
@admin_required
def update_resource(resource_id):
    resource = db.session.get(Resource, resource_id)

    if not resource:
        return jsonify({"message": "Resource not found"}), 404

    data = request.get_json() or {}

    allowed_fields = [
        "resource_name",
        "resource_type",
        "location",
        "description",
        "is_active",
    ]

    for field in allowed_fields:
        if field in data:
            setattr(resource, field, data[field])

    db.session.commit()

    return jsonify({
        "message": "Resource updated successfully",
        "resource": resource_to_dict(resource),
    }), 200


@admin_bp.route("/resources/<int:resource_id>/status", methods=["PATCH"])
@jwt_required()
@admin_required
def update_resource_status(resource_id):
    resource = db.session.get(Resource, resource_id)

    if not resource:
        return jsonify({"message": "Resource not found"}), 404

    data = request.get_json() or {}

    if not isinstance(data.get("is_active"), bool):
        return jsonify({"message": "is_active must be true or false"}), 400

    resource.is_active = data["is_active"]
    db.session.commit()

    return jsonify({
        "message": "Resource status updated",
        "resource": resource_to_dict(resource),
    }), 200


# BOOKING MANAGEMENT
@admin_bp.route("/bookings", methods=["GET"])
@jwt_required()
@admin_required
def get_all_bookings():
    query = Booking.query

    status = request.args.get("status")
    if status:
        query = query.filter_by(status=status)

    bookings = query.order_by(Booking.booking_date.desc()).all()

    return jsonify([booking_to_dict(b) for b in bookings]), 200


@admin_bp.route("/bookings/<int:booking_id>", methods=["GET"])
@jwt_required()
@admin_required
def get_booking(booking_id):
    booking = db.session.get(Booking, booking_id)

    if not booking:
        return jsonify({"message": "Booking not found"}), 404

    return jsonify(booking_to_dict(booking)), 200


@admin_bp.route("/bookings/<int:booking_id>/approve", methods=["PATCH"])
@jwt_required()
@admin_required
def approve_booking(booking_id):

    booking = db.session.get(Booking, booking_id)

    if not booking:
        return jsonify({"message": "Booking not found"}), 404

    if booking.status != "pending":
        return jsonify({"message": "Only pending bookings can be approved"}), 409

    overlapping = Booking.query.filter(
        Booking.resource_id == booking.resource_id,
        Booking.booking_date == booking.booking_date,
        Booking.status == "approved",
        Booking.booking_id != booking.booking_id,
        Booking.start_time < booking.end_time,
        Booking.end_time > booking.start_time,
    ).first()

    if overlapping:
        return jsonify({"message": "This resource has an overlapping approved booking"}), 409

    booking.status = "approved"

    db.session.add(Notification(
        user_id=booking.user_id,
        message=f"Your booking #{booking.booking_id} has been approved.",
        notification_type="booking",
        related_type="booking",
        related_id=booking.booking_id,
    ))

    db.session.commit()

    return jsonify({
        "message": "Booking approved successfully",
        "status": booking.status,
        "booking": booking_to_dict(booking),
    }), 200

@admin_bp.route("/bookings/<int:booking_id>/reject", methods=["PATCH"])
@jwt_required()
@admin_required
def reject_booking(booking_id):

    booking = db.session.get(Booking, booking_id)

    if not booking:
        return jsonify({"message": "Booking not found"}), 404

    if booking.status != "pending":
        return jsonify({"message": "Only pending bookings can be rejected"}), 409

    booking.status = "rejected"

    db.session.add(Notification(
        user_id=booking.user_id,
        message=f"Your booking #{booking.booking_id} has been rejected.",
        notification_type="booking",
        related_type="booking",
        related_id=booking.booking_id,
    ))

    db.session.commit()

    return jsonify({
        "message": "Booking rejected successfully",
        "status": booking.status,
        "booking": booking_to_dict(booking),
    }), 200

@admin_bp.route("/bookings/<int:booking_id>/status", methods=["PATCH"])
@jwt_required()
@admin_required
def update_booking_status(booking_id):
    booking = db.session.get(Booking, booking_id)

    if not booking:
        return jsonify({"message": "Booking not found"}), 404

    data = request.get_json() or {}
    status = data.get("status")

    allowed_statuses = ["pending", "approved", "rejected", "cancelled"]

    if status not in allowed_statuses:
        return jsonify({"message": "Invalid booking status"}), 400

    booking.status = status
    db.session.commit()

    return jsonify({
        "message": "Booking status updated",
        "booking": booking_to_dict(booking),
    }), 200


# INCIDENT MANAGEMENT
@admin_bp.route("/incidents", methods=["GET"])
@jwt_required()
@admin_required
def get_all_incidents():
    query = Incident.query

    status = request.args.get("status")
    if status:
        query = query.filter_by(status=status)

    incidents = query.order_by(Incident.created_at.desc()).all()

    return jsonify([incident_to_dict(i) for i in incidents]), 200


@admin_bp.route("/incidents/<int:incident_id>", methods=["GET"])
@jwt_required()
@admin_required
def get_incident(incident_id):
    incident = db.session.get(Incident, incident_id)

    if not incident:
        return jsonify({"message": "Incident not found"}), 404

    return jsonify(incident_to_dict(incident)), 200


@admin_bp.route("/incidents/<int:incident_id>/status", methods=["PATCH"])
@jwt_required()
@admin_required
def update_incident_status(incident_id):

    incident = db.session.get(Incident, incident_id)

    if not incident:
        return jsonify({"message": "Incident not found"}), 404

    data = request.get_json() or {}
    status = data.get("status")

    allowed_statuses = ["reported", "in_progress", "resolved", "closed"]

    if status not in allowed_statuses:
        return jsonify({"message": "Invalid incident status"}), 400

    previous_status = incident.status
    incident.status = status

    if previous_status != status:
        db.session.add(Notification(
            user_id=incident.user_id,
            message=f"Your incident #{incident.incident_id} status changed to {status}.",
            notification_type="incident",
            related_type="incident",
            related_id=incident.incident_id,
        ))

    db.session.commit()

    return jsonify({
        "message": "Incident status updated",
        "incident": incident_to_dict(incident),
    }), 200