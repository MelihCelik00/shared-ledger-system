import pytest
from httpx import AsyncClient
import uuid

from core.shared_ledger.operations.base import LedgerOperationType
from apps.example_app.operations import ExampleAppOperationType

@pytest.mark.asyncio
async def test_health_check(test_client: AsyncClient):
    """Test health check endpoint."""
    response = await test_client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

@pytest.mark.asyncio
async def test_get_balance(
    test_client: AsyncClient,
    test_owner_id: str
):
    """Test getting user balance."""
    response = await test_client.get(f"/ledger/{test_owner_id}/balance")
    assert response.status_code == 200
    assert response.json()["balance"] >= 0

@pytest.mark.asyncio
async def test_create_ledger_entry(
    test_client: AsyncClient,
    test_owner_id: str
):
    """Test creating a new ledger entry."""
    payload = {
        "operation": LedgerOperationType.CREDIT_ADD.value,
        "owner_id": test_owner_id,
        "nonce": str(uuid.uuid4())
    }
    
    response = await test_client.post("/ledger/entry", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["entry"] is not None
    assert data["entry"]["amount"] == 10  # From operation config
    assert data["balance"] is not None

@pytest.mark.asyncio
async def test_create_content(
    test_client: AsyncClient,
    test_owner_id: str
):
    """Test content creation endpoint."""
    # First add some credits
    add_credits = {
        "operation": LedgerOperationType.CREDIT_ADD.value,
        "owner_id": test_owner_id,
        "nonce": str(uuid.uuid4()),
        "amount": 100
    }
    await test_client.post("/ledger/entry", json=add_credits)

    # Then try to create content
    response = await test_client.post(f"/content?owner_id={test_owner_id}")

    assert response.status_code == 200
    assert response.json()["balance"] >= 0

@pytest.mark.asyncio
async def test_access_content(
    test_client: AsyncClient,
    test_owner_id: str
):
    """Test content access endpoint."""
    content_id = "test_content_123"
    response = await test_client.post(
        f"/content/{content_id}/access?owner_id={test_owner_id}"
    )

    assert response.status_code == 200
    assert response.json()["balance"] >= 0

@pytest.mark.asyncio
async def test_insufficient_credits_api(
    test_client: AsyncClient
):
    """Test API handling of insufficient credits."""
    # Try to create content without any credits
    no_credits_user = "user_without_credits"
    response = await test_client.post(f"/content?owner_id={no_credits_user}")

    assert response.status_code == 400
    assert "Insufficient credits" in response.json()["detail"]

@pytest.mark.asyncio
async def test_duplicate_transaction_api(
    test_client: AsyncClient,
    test_owner_id: str
):
    """Test API handling of duplicate transactions."""
    nonce = str(uuid.uuid4())
    payload = {
        "operation": LedgerOperationType.CREDIT_ADD.value,
        "owner_id": test_owner_id,
        "nonce": nonce,
        "amount": 100
    }

    # First request should succeed
    response1 = await test_client.post("/ledger/entry", json=payload)
    assert response1.status_code == 200

    # Second request with same nonce should fail
    response2 = await test_client.post("/ledger/entry", json=payload)
    assert response2.status_code == 400
    assert "already exists" in response2.json()["detail"] 