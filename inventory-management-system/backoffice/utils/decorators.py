#!/usr/bin/env python3

"""
Authentication and authorization decorators.
"""

from functools import wraps

from flask import (
    flash,
    redirect,
    session,
    url_for,
)


def login_required(view):
    """
    Allow access only to authenticated users.
    """

    @wraps(view)
    def wrapped_view(*args, **kwargs):

        if "user_id" not in session:
            flash(
                "Please log in to continue.",
                "warning",
            )
            return redirect(
                url_for("auth.login")
            )

        return view(*args, **kwargs)

    return wrapped_view


def admin_required(view):
    """
    Allow access only to administrators.
    """

    @wraps(view)
    def wrapped_view(*args, **kwargs):

        if "user_id" not in session:
            flash(
                "Please log in to continue.",
                "warning",
            )
            return redirect(
                url_for("auth.login")
            )

        if session.get("role") != "admin":
            flash(
                "Administrator access required.",
                "danger",
            )
            return redirect(
                url_for("auth.user_dashboard")
            )

        return view(*args, **kwargs)

    return wrapped_view
