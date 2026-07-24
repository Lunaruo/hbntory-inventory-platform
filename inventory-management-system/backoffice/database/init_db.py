#!/usr/bin/env python3

from werkzeug.security import generate_password_hash

from backoffice.database.database import (
    init_database,
    SessionLocal,
)

from backoffice.models.user import User
from backoffice.models.branch import Branch
from backoffice.models.stock import Stock


def seed_database():
    init_database()

    session = SessionLocal()

    # Avoid duplicate initialization
    if session.query(User).first():
        print("Database already initialized.")
        session.close()
        return

    # Create branches
    paris = Branch(name="Paris")
    lille = Branch(name="Lille")

    session.add_all([paris, lille])
    session.commit()

    # Create admin user
    admin = User(
        username="admin",
        password_hash=generate_password_hash("admin123"),
        role="admin",
        branch_id=None,
    )

    session.add(admin)
    session.commit()

    # Sample stock
    sample_stock = [
        Stock(branch_id=paris.id, product_id=1, quantity=20),
        Stock(branch_id=paris.id, product_id=2, quantity=10),
        Stock(branch_id=paris.id, product_id=3, quantity=5),
        Stock(branch_id=lille.id, product_id=1, quantity=15),
        Stock(branch_id=lille.id, product_id=4, quantity=30),
        Stock(branch_id=lille.id, product_id=5, quantity=12),
    ]

    session.add_all(sample_stock)
    session.commit()

    session.close()

    print("Database initialized successfully.")


if __name__ == "__main__":
    seed_database()
