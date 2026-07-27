#!/usr/bin/env python3

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


from .user import User
from .branch import Branch
from .stock import Stock

__all__ = [
    "Base",
    "User",
    "Branch",
    "Stock",
]
