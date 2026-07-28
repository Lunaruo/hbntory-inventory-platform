#!/usr/bin/env python3

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
)

auth_bp = Blueprint(
    "auth",
    __name__,
)


@auth_bp.route("/")
def home():
    """
    Redirect users to the login page.
    """
    return redirect(url_for("auth.login"))


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """
    Display the login page.

    The authentication logic will be added later.
    """
    if request.method == "POST":
        flash("Authentication not implemented yet.", "info")
        return redirect(url_for("auth.login"))

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    """
    Log out the current user.
    """
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("auth.login"))
