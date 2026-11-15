"""Resource booking API routes."""

from datetime import datetime

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError

from extensions import db
from models import Booking, Resource

bookings_bp = Blueprint("bookings", __name__)


# CREATE A RESOURCE BOOKING
# pylint: disable=too-many-return-statements
@bookings_bp.route("/", methods=["POST"])
@jwt_required()
def create_booking():
    """Create a booking request for a campus resource."""
    data = request.get_json()

    if not isinstance(data, dict):
        return jsonify({"error": "Invalid request data"}), 400

    resource_id = data.get("resource_id")
    booking_date = data.get("booking_date")
    start_time = data.get("start_time")
    end_time = data.get("end_time")

    if not all([resource_id, booking_date, start_time, end_time]):
        return jsonify({"error": "All booking fields are required"}), 400

    try:
        resource_id = int(resource_id)
        booking_date = datetime.strptime(
            booking_date, "%Y-%m-%d"
        ).date()
        start_time = datetime.strptime(
            start_time, "%H:%M"
        ).time()
        end_time = datetime.strptime(
            end_time, "%H:%M"
        ).time()

    except (ValueError, TypeError):
        return jsonify({
            "error": "Invalid resource ID, date or time format"
        }), 400

    if resource_id <= 0:
        return jsonify({"error": "Invalid resource ID"}), 400

    if end_time <= start_time:
        return jsonify({
            "error": "End time must be after start time"
        }), 400

    try:
        # Lock the resource while checking for overlapping bookings
        resource = (
            Resource.query
            .filter_by(resource_id=resource_id)
            .with_for_update()
            .first()
        )

        if not resource or not resource.is_active:
            return jsonify({"error": "Resource not available"}), 404

        # Check whether the resource is already booked
        existing_booking = Booking.query.filter(
            Booking.resource_id == resource_id,
            Booking.booking_date == booking_date,
            Booking.status.in_(["pending", "approved"]),
            Booking.start_time < end_time,
            Booking.end_time > start_time
        ).first()

        if existing_booking:
            return jsonify({
                "error": "This resource is already booked for that time"
            }), 409

        new_booking = Booking(
            user_id=int(get_jwt_identity()),
            resource_id=resource_id,
            booking_date=booking_date,
            start_time=start_time,
            end_time=end_time,
            status="pending"
        )

        db.session.add(new_booking)
        db.session.commit()

        return jsonify({
            "message": "Booking request submitted successfully",
            "booking": {
                "booking_id": new_booking.booking_id,
                "resource_id": new_booking.resource_id,
                "booking_date": str(new_booking.booking_date),
                "start_time": str(new_booking.start_time),
                "end_time": str(new_booking.end_time),
                "status": new_booking.status
            }
        }), 201

    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({"error": "Unable to create booking"}), 500

# VIEW MY BOOKING HISTORY
@bookings_bp.route("/my", methods=["GET"])
@jwt_required()
def my_bookings():
    """Return the booking history of the logged-in user."""
    user_id = int(get_jwt_identity())

    bookings = (
        Booking.query
        .filter_by(user_id=user_id)
        .order_by(Booking.booking_date.desc())
        .all()
    )

    return jsonify([
        {
            "booking_id": booking.booking_id,
            "resource_id": booking.resource_id,
            "booking_date": str(booking.booking_date),
            "start_time": str(booking.start_time),
            "end_time": str(booking.end_time),
            "status": booking.status
        }
        for booking in bookings
    ]), 200


# CANCEL MY BOOKING
@bookings_bp.route("/<int:booking_id>", methods=["DELETE"])
@jwt_required()
def cancel_booking(booking_id):
    """Cancel a booking belonging to the logged-in user."""
    user_id = int(get_jwt_identity())

    booking = Booking.query.filter_by(
        booking_id=booking_id,
        user_id=user_id
    ).first()

    if not booking:
        return jsonify({"error": "Booking not found"}), 404

    if booking.status in ["cancelled", "rejected"]:
        return jsonify({
            "error": "This booking cannot be cancelled"
        }), 400

    booking.status = "cancelled"
    db.session.commit()

    return jsonify({
        "message": "Booking cancelled successfully",
        "booking_id": booking.booking_id,
        "status": booking.status
    }), 200
