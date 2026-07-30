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
    """Initialize the database with sample data."""

    init_db()

    session = SessionLocal()

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
        is_active=True,
    )

    session.add(admin)
    session.commit()

    # Sample stock using product IDs from the external Product API
    sample_stock = [

        # Paris
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
            product_id="HB-MON-2102",
            quantity=31,
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
        Stock(
            branch_id=paris.id,
            product_id="HB-KBD-4101",
            quantity=8,
        ),
        Stock(
            branch_id=paris.id,
            product_id="HB-CBL-6301",
            quantity=2,
        ),
        Stock(
            branch_id=paris.id,
            product_id="HB-SSD-7101",
            quantity=14,
        ),
        Stock(
            branch_id=paris.id,
            product_id="HB-SSD-7102",
            quantity=18,
        ),
        Stock(
            branch_id=paris.id,
            product_id="HB-USB-7201",
            quantity=25,
        ),
        Stock(
            branch_id=paris.id,
            product_id="HB-USB-7202",
            quantity=3,
        ),
        Stock(
            branch_id=paris.id,
            product_id="HB-PWR-8101",
            quantity=1,
        ),
        Stock(
            branch_id=paris.id,
            product_id="HB-PWR-8102",
            quantity=5,
        ),
        Stock(
            branch_id=paris.id,
            product_id="HB-PWR-8201",
            quantity=9,
        ),
        Stock(
            branch_id=paris.id,
            product_id="HB-CHR-9101",
            quantity=4,
        ),
        Stock(
            branch_id=paris.id,
            product_id="HB-DSK-9201",
            quantity=3,
        ),
        Stock(
            branch_id=paris.id,
            product_id="HB-PRN-1501",
            quantity=10,
        ),
        Stock(
            branch_id=paris.id,
            product_id="HB-WHT-9301",
            quantity=3,
        ),
        Stock(
            branch_id=paris.id,
            product_id="HB-BAG-1011",
            quantity=8,
        ),
        Stock(
            branch_id=paris.id,
            product_id="HB-BAG-1012",
            quantity=2,
        ),
        Stock(
            branch_id=paris.id,
            product_id="HB-ACC-1212",
            quantity=33,
        ),

        # Lille
        Stock(
            branch_id=lille.id,
            product_id="HB-LAP-1001",
            quantity=6,
        ),
        Stock(
            branch_id=lille.id,
            product_id="HB-MON-2101",
            quantity=8,
        ),
        Stock(
            branch_id=lille.id,
            product_id="HB-DCK-3001",
            quantity=8,
        ),
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
        Stock(
            branch_id=lille.id,
            product_id="HB-USB-5001",
            quantity=18,
        ),
        Stock(
            branch_id=lille.id,
            product_id="HB-KBD-4102",
            quantity=12,
        ),
        Stock(
            branch_id=lille.id,
            product_id="HB-MSE-4201",
            quantity=11,
        ),
        Stock(
            branch_id=lille.id,
            product_id="HB-CAM-5101",
            quantity=2,
        ),
        Stock(
            branch_id=lille.id,
            product_id="HB-MIC-5201",
            quantity=1,
        ),
        Stock(
            branch_id=lille.id,
            product_id="HB-HDS-5301",
            quantity=1,
        ),
        Stock(
            branch_id=lille.id,
            product_id="HB-RTR-6101",
            quantity=7,
        ),
        Stock(
            branch_id=lille.id,
            product_id="HB-SWT-6201",
            quantity=5,
        ),
        Stock(
            branch_id=lille.id,
            product_id="HB-DEV-1111",
            quantity=4,
        ),
        Stock(
            branch_id=lille.id,
            product_id="HB-DEV-1112",
            quantity=19,
        ),
        Stock(
            branch_id=lille.id,
            product_id="HB-DEV-1113",
            quantity=3,
        ),
        Stock(
            branch_id=lille.id,
            product_id="HB-ACC-1211",
            quantity=34,
        ),
        Stock(
            branch_id=lille.id,
            product_id="HB-ACC-1212",
            quantity=33,
        ),
        Stock(
            branch_id=lille.id,
            product_id="HB-OLD-1301",
            quantity=12,
        ),
        Stock(
            branch_id=lille.id,
            product_id="HB-SEC-1401",
            quantity=12,
        ),
        Stock(
            branch_id=lille.id,
            product_id="HB-SEC-1402",
            quantity=12,
        ),
        Stock(
            branch_id=lille.id,
            product_id="HB-PRN-1501",
            quantity=10,
        ),
        Stock(
            branch_id=lille.id,
            product_id="HB-LBL-1502",
            quantity=9,
        ),
        Stock(
            branch_id=lille.id,
            product_id="HB-SCN-1601",
            quantity=3,
        ),
        Stock(
            branch_id=lille.id,
            product_id="HB-TAB-1701",
            quantity=9,
        ),
        Stock(
            branch_id=lille.id,
            product_id="HB-TAB-1702",
            quantity=2,
        ),
        Stock(
            branch_id=lille.id,
            product_id="HB-LGT-1801",
            quantity=4,
        ),
    ]

    session.add_all(sample_stock)
    session.commit()

    session.close()

    print("Database initialized successfully.")


if __name__ == "__main__":
    seed_database()
