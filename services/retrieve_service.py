from typing import Any, Dict, List
from opensearchpy import OpenSearch
from models.retrieve import RetrieveRequest
from .embedder import embed_query

BOOKS_INDEX = "books"
VECTOR_FIELD = "vector"
VECTOR_DIM = 384

def _filters_to_list(req: RetrieveRequest) -> List[Dict[str, Any]]:
    f = req.filters
    out: List[Dict[str, Any]] = []
    if f.category:
        out.append({"term": {"category": f.category}})
    if f.isbn:
        out.append({"term": {"isbn": f.isbn}})
    if f.author:
        out.append({"term": {"author.keyword": f.author}})
    return out

def search_books_vector(client: OpenSearch, req: RetrieveRequest, index: str = BOOKS_INDEX) -> Dict[str, Any]:
    q_vec = embed_query(req.query)
    if len(q_vec) != VECTOR_DIM:
        raise ValueError(f"Expected {VECTOR_DIM}-D embedding, got {len(q_vec)}")

    filters = _filters_to_list(req)
    knn_obj: Dict[str, Any] = {
        "vector": q_vec,
        "k": req.size,
    }
    if filters:
        knn_obj["filter"] = {"bool": {"filter": filters}}

    body: Dict[str, Any] = {
        "size": req.size,
        "track_total_hits": False,
        "query": {
            "knn": {
                VECTOR_FIELD: knn_obj
            }
        },
        "highlight": {"fields": {"title": {}, "chunk_text": {}}}
    }

    resp = client.search(index=index, body=body)

    hits = resp.get("hits", {})
    results = [
        {
            "id": h["_source"].get("id"),
            "score": h.get("_score"),
            "source": h["_source"],
            "highlight": h.get("highlight", {})
        }
        for h in hits.get("hits", [])
    ]
    return {
        "total": len(results),
        "results": results,
        "raw": {"took": resp.get("took")}
    }
