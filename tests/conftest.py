"""
Pytest configuration and fixtures.
Shared test fixtures for the test suite.
"""

import pytest
import asyncio
from typing import AsyncGenerator
from httpx import AsyncClient
from app.main import app
from app.db.database import db


@pytest.fixture(scope="session")
def event_loop():
    """
    Create an event loop for the test session.
    """
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    """
    Create an async HTTP client for testing endpoints.

    Usage:
        async def test_endpoint(client):
            response = await client.get("/api/v1/users")
            assert response.status_code == 200
    """
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="function")
async def test_db():
    """
    Setup and teardown test database connection.
    """
    # Setup: Connect to test database
    await db.connect()

    yield db

    # Teardown: Clean up and disconnect
    await db.disconnect()


# Add more fixtures here as needed
# Example:
# @pytest.fixture
# async def test_user(test_db):
#     """Create a test user"""
#     # Create and return a test user
#     pass
