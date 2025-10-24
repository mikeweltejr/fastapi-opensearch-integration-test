import pytest


@pytest.mark.asyncio
async def test_vector_search_with_category_filter(client):
    payload = {
        "query": "derelict space station",
        "filters": { "category": "scifi" },
        "size": 3,
        "num_candidates": 100
    }

    r = await client.post("/vector-search", json=payload)

    assert r.status_code == 200, r.text
    data = r.json()
    assert "results" in data
    assert len(data["results"]) >= 1
    assert all(item["source"]["category"] == "scifi" for item in data["results"])

@pytest.mark.asyncio
async def test_vector_search_with_author_filter(client):
    payload = {
        "query": "echoes and memories",
        "filters": {"author": "Alex Stone"},
        "size": 2,
        "num_candidates": 100
    }
    r = await client.post("/vector-search", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert len(data["results"]) >= 0
    if data["results"]:
        assert all(hit["source"]["author"] == "Alex Stone" for hit in data["results"])

@pytest.mark.asyncio
async def test_bad_isbn_rejected(client):
    payload = {
        "query": "anything",
        "filters": {"isbn": "bad-isbn"},  # your validator should 422 this
        "size": 1,
        "num_candidates": 10
    }
    r = await client.post("/vector-search", json=payload)
    assert r.status_code in (400, 422)
