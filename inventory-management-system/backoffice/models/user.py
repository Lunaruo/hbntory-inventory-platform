#!/usr/bin/env python3

from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from . import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)

    username = Column(String(50), unique=True, nullable=False)

    password_hash = Column(String(255), nullable=False)

    role = Column(String(20), nullable=False)

    branch_id = Column(
        Integer,
        ForeignKey("branches.id"),
        nullable=True,
    )

    is_active = Column(Boolean, default=True)

    created_at = Column(
        DateTime,
        server_default=func.now(),
    )

    updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
    )

    branch = relationship(
        "Branch",
        back_populates="users",
    )

    def __repr__(self):
        return f"<User(username='{self.username}', role='{self.role}')>"
