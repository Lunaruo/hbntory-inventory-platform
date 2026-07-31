#!/usr/bin/env python3

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
)

from backoffice.services.user_service import UserService
from backoffice.database.database import SessionLocal
from backoffice.models.branch import Branch
from backoffice.utils.decorators import admin_required

users_bp = Blueprint("users", __name__)


def _get_branches():
    session = SessionLocal()
    try:
        return session.query(Branch).all()
    finally:
        session.close()


@users_bp.route("/users")
@admin_required
def list_users():
    """
    List all users (admin only).
    """
    users = UserService.list_users()
    return render_template("users_list.html", users=users)


@users_bp.route("/users/create", methods=["GET", "POST"])
@admin_required
def create_user():
    """
    Create a new user (admin only).
    """
    branches = _get_branches()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        role = request.form.get("role")
        branch_id = request.form.get("branch_id") or None

        user, error = UserService.create_user(
            username, password, role, branch_id
        )

        if error:
            flash(error, "danger")
            return redirect(url_for("users.create_user"))

        flash("User created successfully.", "success")
        return redirect(url_for("users.list_users"))

    return render_template("user_form.html", branches=branches, user=None)


@users_bp.route("/users/<int:user_id>/edit", methods=["GET", "POST"])
@admin_required
def edit_user(user_id):
    """
    Edit an existing user (admin only).
    """
    branches = _get_branches()
    user = UserService.get_user(user_id)

    if user is None:
        flash("User not found.", "danger")
        return redirect(url_for("users.list_users"))

    if request.method == "POST":
        username = request.form.get("username")
        role = request.form.get("role")
        branch_id = request.form.get("branch_id") or None

        _, error = UserService.update_user(
            user_id, username=username, role=role, branch_id=branch_id
        )

        if error:
            flash(error, "danger")
            return redirect(url_for("users.edit_user", user_id=user_id))

        flash("User updated successfully.", "success")
        return redirect(url_for("users.list_users"))

    return render_template("user_form.html", branches=branches, user=user)


@users_bp.route("/users/<int:user_id>/password", methods=["POST"])
@admin_required
def change_password(user_id):
    """
    Change a user's password (admin only).
    """
    new_password = request.form.get("password")

    success, error = UserService.change_password(user_id, new_password)

    if not success:
        flash(error, "danger")
    else:
        flash("Password updated successfully.", "success")

    return redirect(url_for("users.list_users"))


@users_bp.route("/users/<int:user_id>/delete", methods=["POST"])
@admin_required
def delete_user(user_id):
    """
    Soft-delete a user (admin only).
    """
    success, error = UserService.soft_delete_user(user_id)

    if not success:
        flash(error, "danger")
    else:
        flash("User deactivated.", "success")

    return redirect(url_for("users.list_users"))