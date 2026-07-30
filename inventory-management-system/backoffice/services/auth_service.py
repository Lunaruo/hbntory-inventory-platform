#!/usr/bin/env python3

from werkzeug.security import check_password_hash

from backoffice.database.database import SessionLocal
from backoffice.models.user import User


class AuthService:
    """
    Service responsible for user authentication.
    """

    @staticmethod
    def authenticate(username: str, password: str):
        """
        Authenticate a user.

        Returns:
            User object if credentials are valid.
            None otherwise.
        """

        session = SessionLocal()

        try:
            user = (
                session.query(User)
                .filter(
                    User.username == username,
                    User.is_active == True,
                )
                .first()
            )

            if user is None:
                return None

            if not check_password_hash(
                user.password_hash,
                password,
            ):
                return None

            return user

        finally:
            session.close()
