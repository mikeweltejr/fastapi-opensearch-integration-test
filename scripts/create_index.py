import os
import time
import json
from opensearchpy import OpenSearch, RequestsHttpConnection
from opensearchpy.helpers import bulk
from opensearch.schema import BOOKS_INDEX, BOOKS_INDEX_SCHEMA
from typing import Dict, Generator, Optional
from fastembed import TextEmbedding

OS_HOST = os.getenv("OS_HOST", "http://localhost:9200")
OS_USER = os.getenv("OS_USER", "admin")
OS_PASSWORD = os.getenv("OS_PASS", "admin")
IS_LOCAL = os.getenv("IS_LOCAL", False)

def get_client() -> OpenSearch:
    return OpenSearch(
        hosts=[OS_HOST],
        http_auth=(OS_USER, OS_PASSWORD),
        use_ssl=IS_LOCAL,
        verify_certs=False,
        connection_class=RequestsHttpConnection,
        timeout=30,
        max_retries=3,
        retry_on_timeout=True
    )

def wait_for_yellow(client, seconds=60):
    deadline = time.time() + seconds
    while time.time() < deadline:
        status = client.cluster.health().get("status")
        if status in {"yellow", "green"}:
            return status
        time.sleep(1)
    raise TimeoutError("Cluster did not reach yellow/green")

def create_index(client: OpenSearch, index: str, schema: dict) -> None:
    if client.indices.exists(index=index):
        return
    client.indices.create(index=index, body=schema)

def generate_actions(filepath: str, index_name: str) -> Generator[Dict, None, None]:
    with open(filepath, "r", encoding="utf-8") as f:
        while True:
            action_line = f.readline()
            if not action_line:
                break  # EOF
            if not action_line.strip():
                continue  # skip blank line

            try:
                action_meta = json.loads(action_line)
            except json.JSONDecodeError as e:
                print(f"Skipping invalid action line: {e}")
                continue

            doc_line = f.readline()
            if not doc_line:
                print("Warning: NDJSON ended with an action line missing its document.")
                break
            if not doc_line.strip():
                print("Warning: empty document line after an action; skipping pair.")
                continue

            try:
                document = json.loads(doc_line)
            except json.JSONDecodeError as e:
                print(f"Skipping invalid document line: {e}")
                continue

            meta = next(iter(action_meta.values()), {})
            doc_id: Optional[str] = meta.get("_id")
            routing: Optional[str] = meta.get("routing") or meta.get("_routing")

            action = {
                "_op_type": "index",
                "_index": index_name,
                "_source": document,
            }
            if doc_id:
                action["_id"] = doc_id
            if routing:
                action["routing"] = routing

            yield action

def index_ndjson(filepath: str, index_name: str, refresh: bool = True) -> tuple[int, int]:
    client = get_client()
    success, errors = bulk(client, generate_actions(filepath, index_name), request_timeout=60)
    if refresh:
        client.indices.refresh(index=index_name)

    error_count = len(errors) if isinstance(errors, list) else 0
    return success, error_count

def generate_embeddings(in_path: str, out_path: str, model_name="BAAI/bge-small-en-v1.5"):
    embedder = TextEmbedding(model_name=model_name)   # 384-D
    with open(in_path, "r", encoding="utf-8") as fin, open(out_path, "w", encoding="utf-8") as fout:
        while True:
            action = fin.readline()
            if not action: break
            doc = fin.readline()
            if not doc: break
            d = json.loads(doc)
            vec = vec = next(iter(embedder.embed([d["chunk_text"]])))
            vec = list(vec)
            d["vector"] = [float(x) for x in vec]
            fout.write(action)
            fout.write(json.dumps(d, ensure_ascii=False) + "\n")

def main():
    client = get_client()
    wait_for_yellow(client=client)
    create_index(client=client, index=BOOKS_INDEX, schema=BOOKS_INDEX_SCHEMA)
    mapping = client.indices.get_mapping(index="")
    print(f"Created/verified index '{BOOKS_INDEX}'. Fields: {list(mapping[BOOKS_INDEX]['mappings']['properties'].keys())}")

    generate_embeddings("opensearch/seed_data/seed_data.ndjson", "opensearch/seed_data/seed_data_embedded.ndjson")

    ok, err = index_ndjson("opensearch/seed_data/seed_data_embedded.ndjson", "books")

    print(f"Indexed {ok} docs; errors: {err}")
    if err:
        raise SystemExit(1)

if __name__ == "__main__":
    main()
