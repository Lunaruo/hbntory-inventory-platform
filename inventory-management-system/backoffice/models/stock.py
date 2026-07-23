#!/usr/bin/env python3

from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    DateTime,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from . import Base


class Stock(Base):
    __tablename__ = "stock"

    id = Column(Integer, primary_key=True)

    branch_id = Column(
        Integer,
        ForeignKey("branches.id"),
        nullable=False,
    )

    product_id = Column(
        Integer,
        nullable=False,
    )

    quantity = Column(
        Integer,
        nullable=False,
        default=0,
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

    branch = relationship(
        "Branch",
        back_populates="stock",
    )

    def __repr__(self):
        return (
            f"<Stock("
            f"branch={self.branch_id}, "
            f"product={self.product_id}, "
            f"quantity={self.quantity})>"
        )
