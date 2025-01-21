import pytest
import uuid
from sqlalchemy.ext.asyncio import AsyncSession

from core.shared_ledger.operations.base import BaseLedgerOperations, LedgerOperationType
from core.shared_ledger.schemas.ledger import LedgerEntryCreate
from core.shared_ledger.utils.ledger import (
    get_balance,
    process_ledger_operation,
    InsufficientCreditsError,
    DuplicateTransactionError
)

@pytest.mark.asyncio
async def test_get_balance_empty(
    test_session: AsyncSession,
    test_owner_id: str
):
    """Test getting balance for a new user."""
    # Use a different owner ID to avoid getting signup credits
    empty_balance_owner = "empty_balance_user"
    balance = await get_balance(test_session, empty_balance_owner)
    assert balance.balance == 0

@pytest.mark.asyncio
async def test_process_credit_add(
    test_session: AsyncSession,
    test_owner_id: str,
    test_operation: LedgerOperationType,
    test_amount: int
):
    """Test adding credits to a user's balance."""
    # Use a different owner ID to avoid signup credits
    test_credit_owner = "credit_test_user"
    entry = LedgerEntryCreate(
        operation=test_operation.value,
        amount=test_amount,
        owner_id=test_credit_owner,
        nonce=str(uuid.uuid4())
    )
    await process_ledger_operation(test_session, BaseLedgerOperations, entry)
    balance = await get_balance(test_session, test_credit_owner)
    assert balance.balance == test_amount

@pytest.mark.asyncio
async def test_duplicate_transaction(
    test_session: AsyncSession,
    test_owner_id: str,
    test_operation: LedgerOperationType,
    test_amount: int
):
    """Test handling of duplicate transactions."""
    nonce = str(uuid.uuid4())
    entry = LedgerEntryCreate(
        operation=test_operation.value,
        amount=test_amount,
        owner_id=test_owner_id,
        nonce=nonce
    )
    await process_ledger_operation(test_session, BaseLedgerOperations, entry)
    
    # Try to process the same transaction again
    with pytest.raises(DuplicateTransactionError):
        await process_ledger_operation(test_session, BaseLedgerOperations, entry)

@pytest.mark.asyncio
async def test_insufficient_credits(
    test_session: AsyncSession,
    test_owner_id: str
):
    """Test handling of insufficient credits."""
    # Use a different owner ID to avoid signup credits
    test_credit_owner = "insufficient_credit_user"
    # Try to spend more credits than available
    entry = LedgerEntryCreate(
        operation=LedgerOperationType.CREDIT_SPEND.value,
        amount=-1000,  # Use negative amount for spending
        owner_id=test_credit_owner,
        nonce=str(uuid.uuid4())
    )
    with pytest.raises(InsufficientCreditsError):
        await process_ledger_operation(test_session, BaseLedgerOperations, entry)

@pytest.mark.asyncio
async def test_invalid_operation(
    test_session: AsyncSession,
    test_owner_id: str
):
    """Test handling of invalid operation type."""
    entry = LedgerEntryCreate(
        operation="INVALID_OPERATION",
        amount=100,
        owner_id=test_owner_id,
        nonce=str(uuid.uuid4())
    )
    with pytest.raises(ValueError, match="Invalid operation: INVALID_OPERATION"):
        await process_ledger_operation(test_session, BaseLedgerOperations, entry) 