from fastapi import APIRouter, Depends
from models.book import Book
from opensearchpy import OpenSearch, RequestsHttpConnection
from models.retrieve import RetrieveRequest
from services.retrieve_service import search_books_vector

router = APIRouter()

def get_client() -> OpenSearch:
    import os
    host = os.getenv("OS_HOST", "http://localhost:9200")
    user = os.getenv("OS_USER", "admin")
    pwd  = os.getenv("OS_PASS", "admin")
    return OpenSearch(
        hosts=[host],
        http_auth=(user, pwd) if user or pwd else None,
        use_ssl=host.startswith("https://"),
        verify_certs=False,
        connection_class=RequestsHttpConnection,
        timeout=30,
        max_retries=2,
        retry_on_timeout=True,
    )

@router.post("/vector-search", tags=["retrieve"])
def search(req: RetrieveRequest, client: OpenSearch = Depends(get_client)):
    return search_books_vector(client, req)
