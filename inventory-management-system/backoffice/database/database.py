#!/usr/bin/env python3

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backoffice.models import Base

DATABASE_URL = "sqlite:///inventory.db"

engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(bind=engine)


def init_database():
    Base.metadata.create_all(bind=engine)
