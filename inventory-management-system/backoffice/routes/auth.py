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

from backoffice.services.auth_service import AuthService

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

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        user = AuthService.authenticate(
            username,
            password,
        )

        if user is None:
            flash(
                "Invalid username or password.",
                "danger",
            )
            return redirect(url_for("auth.login"))

        session["user_id"] = user.id
        session["username"] = user.username
        session["role"] = user.role

        if user.role == "admin":
            return redirect(url_for("auth.admin_dashboard"))

        return redirect(url_for("auth.user_dashboard"))

    return render_template("login.html")

@auth_bp.route("/logout")
def logout():
    """
    Log out the current user.
    """
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("auth.login"))

@auth_bp.route("/admin")
def admin_dashboard():

    return render_template("admin_dashboard.html")


@auth_bp.route("/dashboard")
def user_dashboard():

    return render_template("user_dashboard.html")
