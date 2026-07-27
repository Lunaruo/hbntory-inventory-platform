#!/usr/bin/env python3

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from . import Base


class Branch(Base):
    __tablename__ = "branches"

    id = Column(Integer, primary_key=True)

    name = Column(
        String(100),
        unique=True,
        nullable=False,
    )

    created_at = Column(
        DateTime,
        server_default=func.now(),
    )

    updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
    )

    users = relationship(
        "User",
        back_populates="branch",
    )

    stock = relationship(
        "Stock",
        back_populates="branch",
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"<Branch(name='{self.name}')>"
