
"""Main application file for the Campus Resource Booking System."""

import os

from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

from extensions import db, jwt
import models

from routes.auth import auth_bp
from routes.bookings import bookings_bp
from routes.admin import admin_bp
from routes.incidents import incidents_bp
<<<<<<< HEAD
=======
from routes.notifications import notifications_bp
>>>>>>> 6fbb0e6 (Add project planning architecture and test documentation)

load_dotenv()

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")

CORS(app)

db.init_app(app)
jwt.init_app(app)

# Register existing API routes
app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(bookings_bp, url_prefix="/api/bookings")
app.register_blueprint(admin_bp, url_prefix="/api/admin")
app.register_blueprint(incidents_bp, url_prefix="/api/incidents")

# Register Member 2 admin API routes
app.register_blueprint(admin_bp, url_prefix="/api/admin")
app.register_blueprint(incidents_bp, url_prefix="/api")
app.register_blueprint(notifications_bp, url_prefix="/api/notifications")

@app.route("/")
def home():
    """Check whether the API is running."""
    return jsonify({
        "message": "Campus Resource Management API is running!"
    })


@app.route("/api/resources", methods=["GET"])
def get_resources():
    """Return all active campus resources."""

    resources = models.Resource.query.filter_by(
        is_active=True
    ).all()

    return jsonify([
        {
            "resource_id": resource.resource_id,
            "resource_name": resource.resource_name,
            "resource_type": resource.resource_type,
            "location": resource.location,
            "description": resource.description
        }
        for resource in resources
    ])


if __name__ == "__main__":
    app.run(debug=True, port=5000)
