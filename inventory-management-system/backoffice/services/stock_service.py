#!/usr/bin/env python3

from sqlalchemy.orm import joinedload

from backoffice.database.database import SessionLocal
from backoffice.models.stock import Stock


class StockService:
    """
    Service responsible for stock management.
    """

    @staticmethod
    def list_stock_for_branch(branch_id):
        session = SessionLocal()
        try:
            return (
                session.query(Stock)
                .options(joinedload(Stock.branch))
                .filter(Stock.branch_id == branch_id)
                .all()
            )
        finally:
            session.close()

    @staticmethod
    def list_all_stock():
        session = SessionLocal()
        try:
            return (
                session.query(Stock)
                .options(joinedload(Stock.branch))
                .all()
            )
        finally:
            session.close()

    @staticmethod
    def add_stock(branch_id, product_id, quantity):
        """
        Add quantity to an existing stock entry, or create one.

        Returns:
            (Stock, None) on success.
            (None, error_message) on failure.
        """
        if quantity <= 0:
            return None, "Quantity must be a positive integer."

        session = SessionLocal()
        try:
            entry = (
                session.query(Stock)
                .filter(
                    Stock.branch_id == branch_id,
                    Stock.product_id == product_id,
                )
                .first()
            )

            if entry:
                entry.quantity += quantity
            else:
                entry = Stock(
                    branch_id=branch_id,
                    product_id=product_id,
                    quantity=quantity,
                )
                session.add(entry)

            session.commit()
            session.refresh(entry)
            return entry, None
        finally:
            session.close()

    @staticmethod
    def remove_stock(branch_id, product_id, quantity):
        """
        Remove quantity from an existing stock entry.
        Never allows the quantity to go negative.

        Returns:
            (Stock, None) on success.
            (None, error_message) on failure.
        """
        if quantity <= 0:
            return None, "Quantity must be a positive integer."

        session = SessionLocal()
        try:
            entry = (
                session.query(Stock)
                .filter(
                    Stock.branch_id == branch_id,
                    Stock.product_id == product_id,
                )
                .first()
            )

            if entry is None:
                return None, "No stock entry found for this product."

            if entry.quantity - quantity < 0:
                return None, (
                    f"Cannot remove {quantity} units: only "
                    f"{entry.quantity} available."
                )

            entry.quantity -= quantity
            session.commit()
            session.refresh(entry)
            return entry, None
        finally:
            session.close()