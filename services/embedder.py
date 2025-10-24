from typing import List
from fastembed import TextEmbedding

_EMBEDDER: TextEmbedding | None = None

def _get_embedder(model: str = "BAAI/bge-small-en-v1.5") -> TextEmbedding:
    global _EMBEDDER
    if _EMBEDDER is None:
        _EMBEDDER = TextEmbedding(model_name=model)
    return _EMBEDDER

def embed_query(text: str) -> List[float]:
    emb = next(iter(_get_embedder().embed([text])))
    return [float(x) for x in emb]
