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

from backoffice.services.stock_service import StockService
from backoffice.utils.decorators import login_required

stock_bp = Blueprint("stock", __name__)


@stock_bp.route("/stock")
@login_required
def view_stock():
    """
    View stock: all branches for admin, own branch only for common users.
    """
    if session.get("role") == "admin":
        stock_entries = StockService.list_all_stock()
    else:
        stock_entries = StockService.list_stock_for_branch(
            session.get("branch_id")
        )

    return render_template("stock_list.html", stock_entries=stock_entries)


@stock_bp.route("/stock/add", methods=["POST"])
@login_required
def add_stock():
    """
    Add stock for the current user's own branch.
    """
    product_id = request.form.get("product_id")
    quantity = int(request.form.get("quantity", 0))
    branch_id = session.get("branch_id")

    if session.get("role") == "admin":
        flash("Admins cannot modify stock directly.", "danger")
        return redirect(url_for("stock.view_stock"))

    _, error = StockService.add_stock(branch_id, product_id, quantity)

    if error:
        flash(error, "danger")
    else:
        flash(f"Added {quantity} units of {product_id}.", "success")

    return redirect(url_for("stock.view_stock"))


@stock_bp.route("/stock/remove", methods=["POST"])
@login_required
def remove_stock():
    """
    Remove stock for the current user's own branch.
    """
    product_id = request.form.get("product_id")
    quantity = int(request.form.get("quantity", 0))
    branch_id = session.get("branch_id")

    if session.get("role") == "admin":
        flash("Admins cannot modify stock directly.", "danger")
        return redirect(url_for("stock.view_stock"))

    _, error = StockService.remove_stock(branch_id, product_id, quantity)

    if error:
        flash(error, "danger")
    else:
        flash(f"Removed {quantity} units of {product_id}.", "success")

    return redirect(url_for("stock.view_stock"))