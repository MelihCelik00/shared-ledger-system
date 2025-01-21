from datetime import datetime
from typing import Optional, Type, Dict, List
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.ledger import LedgerEntry
from ..operations.base import BaseLedgerOperations
from ..schemas.ledger import (
    LedgerEntryCreate,
    LedgerBalance,
    LedgerOperationResponse
)

class InsufficientCreditsError(Exception):
    """Raised when an operation would result in negative balance."""
    pass

class DuplicateTransactionError(Exception):
    """Raised when attempting to process a duplicate transaction."""
    pass

async def get_balance(
    session: AsyncSession,
    owner_id: str
) -> LedgerBalance:
    """
    Get the current balance for an owner.
    
    Args:
        session: Database session
        owner_id: ID of the owner
        
    Returns:
        LedgerBalance object containing current balance and last update time
    """
    result = await session.execute(
        select(
            func.sum(LedgerEntry.amount).label("balance"),
            func.max(LedgerEntry.created_at).label("last_updated")
        ).where(LedgerEntry.owner_id == owner_id)
    )
    row = result.first()
    
    return LedgerBalance(
        owner_id=owner_id,
        balance=row.balance or 0,
        last_updated=row.last_updated or datetime.utcnow()
    )

async def validate_operation(
    session: AsyncSession,
    operations: Type[BaseLedgerOperations],
    entry: LedgerEntryCreate
) -> None:
    """
    Validate a ledger operation before processing.
    
    Args:
        session: Database session
        operations: Operations class containing configuration
        entry: Entry to validate
        
    Raises:
        ValueError: If operation is invalid
        InsufficientCreditsError: If user has insufficient credits
        DuplicateTransactionError: If transaction is a duplicate
    """
    # Validate operation exists in configuration
    operation_config = operations.get_operation_config()
    if entry.operation not in operation_config:
        raise ValueError(f"Invalid operation: {entry.operation}")
    
    # Check for duplicate nonce
    result = await session.execute(
        select(LedgerEntry).where(LedgerEntry.nonce == entry.nonce)
    )
    if result.first() is not None:
        raise DuplicateTransactionError(f"Duplicate transaction: {entry.nonce}")
    
    # For debit operations, check sufficient balance
    if operation_config.get(entry.operation, 0) < 0:
        balance = await get_balance(session, entry.owner_id)
        if balance.balance + entry.amount < 0:
            raise InsufficientCreditsError(
                f"Insufficient credits. Required: {abs(entry.amount)}, "
                f"Available: {balance.balance}"
            )

async def process_ledger_operation(
    session: AsyncSession,
    operations: Type[BaseLedgerOperations],
    entry: LedgerEntryCreate
) -> LedgerOperationResponse:
    """
    Process a ledger operation.
    
    Args:
        session: Database session
        operations: Operations class containing configuration
        entry: Entry to process
        
    Returns:
        LedgerOperationResponse with operation result
        
    Raises:
        ValueError: If operation is invalid
        InsufficientCreditsError: If user has insufficient credits
        DuplicateTransactionError: If transaction is a duplicate
    """
    try:
        # Check for duplicate transaction
        stmt = select(LedgerEntry).where(LedgerEntry.nonce == entry.nonce)
        result = await session.execute(stmt)
        if result.first() is not None:
            raise DuplicateTransactionError(f"Transaction with nonce {entry.nonce} already exists")
        
        # Get operation amount from configuration or entry
        operation_config = operations.get_operation_config()
        if entry.operation not in operation_config:
            raise ValueError(f"Invalid operation: {entry.operation}")
        operation_amount = entry.amount if entry.amount is not None else operation_config[entry.operation]
        
        # Create new entry with configured amount
        db_entry = LedgerEntry(
            operation=entry.operation,
            owner_id=entry.owner_id,
            amount=operation_amount,
            nonce=entry.nonce
        )
        
        # Check if operation would result in negative balance
        if operation_amount < 0:
            current_balance = await get_balance(session, entry.owner_id)
            if current_balance.balance + operation_amount < 0:
                raise InsufficientCreditsError(
                    f"Insufficient credits: {current_balance.balance} available, {abs(operation_amount)} needed"
                )
        
        # Save entry and get updated balance
        session.add(db_entry)
        await session.commit()
        await session.refresh(db_entry)
        
        current_balance = await get_balance(session, entry.owner_id)
        
        return LedgerOperationResponse(
            entry=db_entry,
            balance=current_balance.balance
        )
    except (ValueError, InsufficientCreditsError, DuplicateTransactionError) as e:
        await session.rollback()
        raise 