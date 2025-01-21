"""
Ledger entry model for tracking credit operations.
"""

from datetime import datetime
from sqlalchemy import String, Integer, DateTime, Index
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from .base import Base


class LedgerEntry(Base):
    """
    Represents a single ledger entry for credit operations.
    Each entry tracks a credit operation (add/spend) for a specific owner.
    """
    __tablename__ = "ledger_entries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    owner_id: Mapped[str] = mapped_column(String, nullable=False, index=True)
    operation: Mapped[str] = mapped_column(String, nullable=False, index=True)
    amount: Mapped[int] = mapped_column(Integer, nullable=False)
    nonce: Mapped[str] = mapped_column(String, nullable=False, unique=True, index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    # Indexes for common queries
    __table_args__ = (
        Index('ix_ledger_entries_owner_operation', 'owner_id', 'operation'),
    )

    def __repr__(self) -> str:
        return f"<LedgerEntry(id={self.id}, owner_id='{self.owner_id}', operation='{self.operation}', amount={self.amount})>" 