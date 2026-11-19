
"""Routes for viewing and managing user notifications."""

from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from extensions import db
from models import Notification, User


notifications_bp = Blueprint("notifications", __name__)


@notifications_bp.route("/", methods=["GET"])
@jwt_required()
def get_notifications():
    """Return notifications belonging only to the logged-in user."""

    user_id = int(get_jwt_identity())

    user = db.session.get(User, user_id)

    if user is None:
        return jsonify({"message": "User not found"}), 404

    notifications = (
        Notification.query
        .filter_by(user_id=user_id)
        .order_by(Notification.created_at.desc())
        .all()
    )

    result = []

    for notification in notifications:
        result.append({
            "notification_id": notification.notification_id,
            "message": notification.message,
            "notification_type": notification.notification_type,
            "related_type": notification.related_type,
            "related_id": notification.related_id,
            "is_read": notification.is_read,
            "created_at": notification.created_at.isoformat()
        })

    unread_count = sum(
        1 for notification in notifications
        if not notification.is_read
    )

    return jsonify({
        "notifications": result,
        "unread_count": unread_count
    }), 200


@notifications_bp.route("/<int:notification_id>/read", methods=["PATCH"])
@jwt_required()
def mark_notification_read(notification_id):
    """Mark a notification as read if it belongs to the logged-in user."""

    user_id = int(get_jwt_identity())

    notification = Notification.query.filter_by(
        notification_id=notification_id,
        user_id=user_id
    ).first()

    if notification is None:
        return jsonify({"message": "Notification not found"}), 404

    notification.is_read = True
    db.session.commit()

    return jsonify({
        "message": "Notification marked as read",
        "notification_id": notification.notification_id,
        "is_read": notification.is_read
    }), 200


@notifications_bp.route("/read-all", methods=["PATCH"])
@jwt_required()
def mark_all_notifications_read():
    """Mark all notifications belonging to the logged-in user as read."""

    user_id = int(get_jwt_identity())

    user = db.session.get(User, user_id)

    if user is None:
        return jsonify({"message": "User not found"}), 404

    Notification.query.filter_by(
        user_id=user_id,
        is_read=False
    ).update({"is_read": True})

    db.session.commit()

    return jsonify({
        "message": "All notifications marked as read"
    }), 200
