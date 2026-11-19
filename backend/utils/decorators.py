from functools import wraps

from flask import jsonify
from flask_jwt_extended import get_jwt_identity

from extensions import db
from models import User


def admin_required(function):
    @wraps(function)
    def decorated_function(*args, **kwargs):
        user_id = get_jwt_identity()
        user = db.session.get(User, int(user_id))

        if not user:
            return jsonify({"message": "User not found"}), 404

        if user.role != "admin":
            return jsonify({"message": "Admin access required"}), 403

        return function(*args, **kwargs)

    return decorated_function
