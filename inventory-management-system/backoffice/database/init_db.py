#!/usr/bin/env python3

from werkzeug.security import generate_password_hash

from backoffice.database.database import (
    SessionLocal,
    init_db,
)

from backoffice.models.user import User
from backoffice.models.branch import Branch
from backoffice.models.stock import Stock


def seed_database():
    init_db()

    session = SessionLocal()

    if session.query(User).first():
        print("Database already initialized.")
        session.close()
        return

    # -------------------------
    # Create branches
    # -------------------------
    paris = Branch(name="Paris")
    lille = Branch(name="Lille")

    session.add_all([paris, lille])
    session.commit()

    # -------------------------
    # Create admin user
    # -------------------------
    admin = User(
        username="admin",
        password_hash=generate_password_hash("admin123"),
        role="admin",
        branch_id=None,
        is_active=True,
    )

    session.add(admin)
    session.commit()

    # -------------------------
    # Sample stock
    # Product IDs come from the
    # external HBntory Product API
    # -------------------------

    sample_stock = [

        # -------- Paris --------

        Stock(
            branch_id=paris.id,
            product_id="HB-LAP-1001",
            quantity=15,
        ),

        Stock(
            branch_id=paris.id,
            product_id="HB-KBD-3001",
            quantity=10,
        ),

        Stock(
            branch_id=paris.id,
            product_id="HB-MSE-4001",
            quantity=20,
        ),

        Stock(
            branch_id=paris.id,
            product_id="HB-USB-5001",
            quantity=35,
        ),

        Stock(
            branch_id=paris.id,
            product_id="HB-WEB-7001",
            quantity=8,
        ),

        # -------- Lille --------

        Stock(
            branch_id=lille.id,
            product_id="HB-LAP-1002",
            quantity=7,
        ),

        Stock(
            branch_id=lille.id,
            product_id="HB-MON-2001",
            quantity=12,
        ),

        Stock(
            branch_id=lille.id,
            product_id="HB-HDP-8001",
            quantity=18,
        ),

        Stock(
            branch_id=lille.id,
            product_id="HB-CAM-9001",
            quantity=6,
        ),

        Stock(
            branch_id=lille.id,
            product_id="HB-CHA-10001",
            quantity=14,
        ),
    ]

    session.add_all(sample_stock)
    session.commit()

    session.close()

    print("Database initialized successfully.")


if __name__ == "__main__":
    seed_database()
