import os
import pytest_asyncio
import httpx

API = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")

@pytest_asyncio.fixture
async def client():
    async with httpx.AsyncClient(base_url=API, timeout=15.0) as c:
        yield c
