VECTOR_DIM = 384
BOOKS_INDEX = "books"

BOOKS_INDEX_SCHEMA = {
    "settings": {
        "index.knn": True,  # enable vector search
    },
    "mappings": {
        "properties": {
            "id": {"type": "keyword"},
            "isbn": {"type": "keyword"},
            "chapter": {"type": "integer"},
            "title": {
                "type": "text",
                "fields": {"keyword": {"type": "keyword"}}
            },
            "chunk_text": {"type": "text"},
            "author": {
                "type": "text",
                "fields": {"keyword": {"type": "keyword"}}
            },
            "category": {"type": "keyword"},
            "vector": {
                "type": "knn_vector",
                "dimension": VECTOR_DIM,
                "method": {
                    "name": "hnsw",
                    "space_type": "cosinesimil",
                    "engine": "lucene"
                }
            }
        }
    }
}
