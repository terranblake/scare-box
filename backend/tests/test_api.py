"""Tests for REST API endpoints."""

import pytest
from httpx import AsyncClient
from backend.main import app
from backend.controller import ScareBoxController


@pytest.fixture
async def client():
    """Create test client."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
async def test_root_endpoint(client):
    """Test root endpoint returns status."""
    response = await client.get("/")

    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert "version" in data


@pytest.mark.asyncio
async def test_get_config(client):
    """Test getting configuration."""
    response = await client.get("/api/config")

    assert response.status_code == 200
    data = response.json()
    assert "mode" in data
    assert "audio" in data
    assert "timing" in data


@pytest.mark.asyncio
async def test_get_mode(client):
    """Test getting current mode."""
    response = await client.get("/api/mode")

    assert response.status_code == 200
    data = response.json()
    assert "mode" in data
    assert data["mode"] in ["child", "adult"]


@pytest.mark.asyncio
async def test_set_mode(client):
    """Test setting mode."""
    response = await client.put("/api/mode", json={"mode": "adult"})

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True


@pytest.mark.asyncio
async def test_get_state(client):
    """Test getting system state."""
    response = await client.get("/api/state")

    assert response.status_code == 200
    data = response.json()
    assert "state" in data
    assert "mode" in data
    assert "is_running" in data


@pytest.mark.asyncio
async def test_get_devices(client):
    """Test getting device statuses."""
    response = await client.get("/api/devices")

    assert response.status_code == 200
    data = response.json()
    assert "microphone" in data
    assert "lights" in data
    assert "speaker" in data


@pytest.mark.asyncio
async def test_get_events(client):
    """Test getting event history."""
    response = await client.get("/api/events?limit=10")

    assert response.status_code == 200
    data = response.json()
    assert "events" in data
    assert "total" in data
    assert isinstance(data["events"], list)


@pytest.mark.asyncio
async def test_get_event_stats(client):
    """Test getting event statistics."""
    response = await client.get("/api/events/stats")

    assert response.status_code == 200
    data = response.json()
    assert "total_events" in data
    assert "by_level" in data
    assert "by_category" in data


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
