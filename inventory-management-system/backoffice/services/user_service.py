#!/usr/bin/env python3

from werkzeug.security import generate_password_hash

from backoffice.database.database import SessionLocal
from backoffice.models.user import User


class UserService:
    """
    Service responsible for admin user management.
    """

    @staticmethod
    def list_users():
        session = SessionLocal()
        try:
            return session.query(User).all()
        finally:
            session.close()

    @staticmethod
    def get_user(user_id: int):
        session = SessionLocal()
        try:
            return session.query(User).filter(User.id == user_id).first()
        finally:
            session.close()

    @staticmethod
    def create_user(username, password, role, branch_id):
        """
        Create a new user.

        Returns:
            (User, None) on success.
            (None, error_message) on failure.
        """
        session = SessionLocal()
        try:
            existing = (
                session.query(User)
                .filter(User.username == username)
                .first()
            )
            if existing:
                return None, "Username already exists."

            if role == "admin":
                branch_id = None

            user = User(
                username=username,
                password_hash=generate_password_hash(password),
                role=role,
                branch_id=branch_id,
                is_active=True,
            )
            session.add(user)
            session.commit()
            session.refresh(user)
            return user, None
        finally:
            session.close()

    @staticmethod
    def update_user(user_id, username=None, role=None, branch_id=None):
        session = SessionLocal()
        try:
            user = session.query(User).filter(User.id == user_id).first()
            if user is None:
                return None, "User not found."

            if username:
                user.username = username
            if role:
                user.role = role
                if role == "admin":
                    user.branch_id = None
            if branch_id is not None and user.role != "admin":
                user.branch_id = branch_id

            session.commit()
            session.refresh(user)
            return user, None
        finally:
            session.close()

    @staticmethod
    def change_password(user_id, new_password):
        session = SessionLocal()
        try:
            user = session.query(User).filter(User.id == user_id).first()
            if user is None:
                return False, "User not found."

            user.password_hash = generate_password_hash(new_password)
            session.commit()
            return True, None
        finally:
            session.close()

    @staticmethod
    def soft_delete_user(user_id):
        session = SessionLocal()
        try:
            user = session.query(User).filter(User.id == user_id).first()
            if user is None:
                return False, "User not found."

            user.is_active = False
            session.commit()
            return True, None
        finally:
            session.close()
            