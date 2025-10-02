import pytest
from httpx import AsyncClient
from app.main import app
import asyncio
import os

@pytest.mark.asyncio
async def test_health():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.get("/health")
        assert r.status_code == 200
        assert r.json() == {"status": "ok"}

@pytest.mark.asyncio
async def test_token_and_protected():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.post("/token")
        assert r.status_code == 200
        token = r.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        r2 = await ac.get("/proxy/data", headers=headers)
        assert r2.status_code == 200
        # second call should return cached data structure (stringify logic returns str)
        r3 = await ac.get("/proxy/data", headers=headers)
        assert r3.status_code == 200
