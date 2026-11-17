from getpass import getpass

from app import app
from extensions import db
from models import User
from werkzeug.security import generate_password_hash


def create_admin():
    print("\n=== Campus Resource Management - Admin Setup ===")

    name = input("Enter admin name: ").strip()
    email = input("Enter admin email: ").strip().lower()
    password = getpass("Enter admin password (minimum 8 characters): ")
    confirm_password = getpass("Confirm admin password: ")

    if not name or not email:
        print("Name and email are required.")
        return

    if len(password) < 8:
        print("Password must contain at least 8 characters.")
        return

    if password != confirm_password:
        print("Passwords do not match.")
        return

    with app.app_context():
        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            print("An account with this email already exists.")
            return

        admin = User(
            name=name,
            email=email,
            password_hash=generate_password_hash(password),
            role="admin"
        )

        db.session.add(admin)
        db.session.commit()

        print("\nAdmin account created successfully!")
        print("Name:", admin.name)
        print("Email:", admin.email)
        print("Role:", admin.role)


if __name__ == "__main__":
    create_admin()
