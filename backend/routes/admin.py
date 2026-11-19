<<<<<<< HEAD
﻿from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from extensions import db
from models import User, Resource, Booking, Incident
from utils.decorators import admin_required
from utils.serializers import (
    resource_to_dict,
    booking_to_dict,
    incident_to_dict,
)
=======

"""Admin routes for campus resource management."""

from functools import wraps

from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

import models
>>>>>>> 6fbb0e6 (Add project planning architecture and test documentation)

admin_bp = Blueprint("admin", __name__)


<<<<<<< HEAD
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
=======
def admin_required(function):
    """Allow access only to authenticated administrators."""

    @wraps(function)
    @jwt_required()
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        user = models.db.session.get(models.User, user_id)

        if user is None or user.role.lower() != "admin":
            return jsonify({"error": "Admin access required"}), 403

        return function(*args, **kwargs)

    return wrapper


# ---------------- RESOURCE MANAGEMENT ----------------


@admin_bp.route("/resources", methods=["GET"])
@admin_required
def get_all_resources():
    """Return active and inactive resources."""

    resources = models.Resource.query.order_by(
        models.Resource.resource_id
    ).all()

    return jsonify([
        {
            "resource_id": resource.resource_id,
            "resource_name": resource.resource_name,
            "resource_type": resource.resource_type,
            "location": resource.location,
            "description": resource.description,
            "is_active": resource.is_active
        }
        for resource in resources
    ]), 200


@admin_bp.route("/resources", methods=["POST"])
@admin_required
def add_resource():
    """Add a new campus resource."""

    data = request.get_json(silent=True) or {}

    required_fields = [
        "resource_name",
        "resource_type",
        "location"
    ]

    missing = [
        field for field in required_fields
        if not isinstance(data.get(field), str)
        or not data[field].strip()
    ]

    if missing:
        return jsonify({
            "error": "Required fields are missing or invalid",
            "fields": missing
        }), 400

    resource = models.Resource(
        resource_name=data["resource_name"].strip(),
        resource_type=data["resource_type"].strip(),
        location=data["location"].strip(),
        description=(
            data.get("description", "").strip()
            if isinstance(data.get("description", ""), str)
            else ""
        ),
        is_active=True
    )

    try:
        models.db.session.add(resource)
        models.db.session.commit()
    except Exception:
        models.db.session.rollback()
        return jsonify({
            "error": "Could not create resource"
        }), 500

    return jsonify({
        "message": "Resource created successfully",
        "resource_id": resource.resource_id
    }), 201


@admin_bp.route("/resources/<int:resource_id>", methods=["PATCH"])
@admin_required
def update_resource(resource_id):
    """Update the details of a campus resource."""

    resource = models.db.session.get(
        models.Resource, resource_id
    )

    if resource is None:
        return jsonify({"error": "Resource not found"}), 404

    data = request.get_json(silent=True)

    if not isinstance(data, dict) or not data:
        return jsonify({
            "error": "Provide fields to update"
        }), 400
>>>>>>> 6fbb0e6 (Add project planning architecture and test documentation)

    allowed_fields = [
        "resource_name",
        "resource_type",
        "location",
<<<<<<< HEAD
        "description",
        "is_active",
=======
        "description"
>>>>>>> 6fbb0e6 (Add project planning architecture and test documentation)
    ]

    for field in allowed_fields:
        if field in data:
<<<<<<< HEAD
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
        return jsonify({
            "message": "Only pending bookings can be approved"
        }), 400

    booking.status = "approved"
    db.session.commit()

    return jsonify({
        "message": "Booking approved successfully",
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
        return jsonify({
            "message": "Only pending bookings can be rejected"
        }), 400

    booking.status = "rejected"
    db.session.commit()

    return jsonify({
        "message": "Booking rejected successfully",
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

    allowed_statuses = [
        "reported",
        "in_progress",
        "resolved",
        "closed",
    ]

    if status not in allowed_statuses:
        return jsonify({"message": "Invalid incident status"}), 400

    incident.status = status
    db.session.commit()

    return jsonify({
        "message": "Incident status updated",
        "incident": incident_to_dict(incident),
=======
            if (
                not isinstance(data[field], str)
                or not data[field].strip()
            ):
                return jsonify({
                    "error": f"{field} must be a non-empty string"
                }), 400

            setattr(resource, field, data[field].strip())

    try:
        models.db.session.commit()
    except Exception:
        models.db.session.rollback()
        return jsonify({
            "error": "Could not update resource"
        }), 500

    return jsonify({
        "message": "Resource updated successfully"
    }), 200


@admin_bp.route("/resources/<int:resource_id>", methods=["DELETE"])
@admin_required
def deactivate_resource(resource_id):
    """Deactivate a resource without deleting its booking history."""

    resource = models.db.session.get(
        models.Resource, resource_id
    )

    if resource is None:
        return jsonify({"error": "Resource not found"}), 404

    resource.is_active = False

    try:
        models.db.session.commit()
    except Exception:
        models.db.session.rollback()
        return jsonify({
            "error": "Could not deactivate resource"
        }), 500

    return jsonify({
        "message": "Resource deactivated successfully"
    }), 200


# ---------------- BOOKING ADMINISTRATION ----------------


@admin_bp.route("/bookings", methods=["GET"])
@admin_required
def get_all_bookings():
    """Allow administrators to view all booking requests."""

    bookings = models.Booking.query.order_by(
        models.Booking.booking_id.desc()
    ).all()

    result = []

    for booking in bookings:
        user = models.db.session.get(
            models.User, booking.user_id
        )

        resource = models.db.session.get(
            models.Resource, booking.resource_id
        )

        result.append({
            "booking_id": booking.booking_id,
            "user_id": booking.user_id,
            "student_name": user.name if user else "Unknown",
            "resource_id": booking.resource_id,
            "resource_name": (
                resource.resource_name if resource else "Unknown"
            ),
            "booking_date": str(booking.booking_date),
            "start_time": str(booking.start_time),
            "end_time": str(booking.end_time),
            "status": booking.status
        })

    return jsonify(result), 200


@admin_bp.route(
    "/bookings/<int:booking_id>/approve",
    methods=["PATCH"]
)
@admin_required
def approve_booking(booking_id):
    """Approve a pending booking if no approved booking overlaps."""

    booking = models.db.session.get(
        models.Booking, booking_id
    )

    if booking is None:
        return jsonify({"error": "Booking not found"}), 404

    if booking.status != "pending":
        return jsonify({
            "error": "Only pending bookings can be approved"
        }), 409

    resource = models.db.session.get(
        models.Resource, booking.resource_id
    )

    if resource is None or not resource.is_active:
        return jsonify({
            "error": "This resource is unavailable"
        }), 409

    overlapping_booking = models.Booking.query.filter(
        models.Booking.resource_id == booking.resource_id,
        models.Booking.booking_date == booking.booking_date,
        models.Booking.status == "approved",
        models.Booking.booking_id != booking.booking_id,
        models.Booking.start_time < booking.end_time,
        models.Booking.end_time > booking.start_time
    ).first()

    if overlapping_booking:
        return jsonify({
            "error": "Another approved booking overlaps this time"
        }), 409

    booking.status = "approved"

    notification = models.Notification(
        user_id=booking.user_id,
        message=(
            f"Your booking request #{booking.booking_id} "
            "has been approved."
        ),
        notification_type="booking",
        related_type="booking",
        related_id=booking.booking_id
    )

    try:
        models.db.session.add(notification)
        models.db.session.commit()
    except Exception:
        models.db.session.rollback()
        return jsonify({
            "error": "Could not approve booking"
        }), 500

    return jsonify({
        "message": "Booking approved successfully",
        "booking_id": booking.booking_id,
        "status": booking.status
    }), 200


@admin_bp.route(
    "/bookings/<int:booking_id>/reject",
    methods=["PATCH"]
)
@admin_required
def reject_booking(booking_id):
    """Reject a pending booking and notify the student."""

    booking = models.db.session.get(
        models.Booking, booking_id
    )

    if booking is None:
        return jsonify({"error": "Booking not found"}), 404

    if booking.status != "pending":
        return jsonify({
            "error": "Only pending bookings can be rejected"
        }), 409

    booking.status = "rejected"

    notification = models.Notification(
        user_id=booking.user_id,
        message=(
            f"Your booking request #{booking.booking_id} "
            "has been rejected."
        ),
        notification_type="booking",
        related_type="booking",
        related_id=booking.booking_id
    )

    try:
        models.db.session.add(notification)
        models.db.session.commit()
    except Exception:
        models.db.session.rollback()
        return jsonify({
            "error": "Could not reject booking"
        }), 500

    return jsonify({
        "message": "Booking rejected successfully",
        "booking_id": booking.booking_id,
        "status": booking.status
>>>>>>> 6fbb0e6 (Add project planning architecture and test documentation)
    }), 200
