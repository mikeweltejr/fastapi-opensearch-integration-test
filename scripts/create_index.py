import os
import time
from opensearchpy import OpenSearch, RequestsHttpConnection
from opensearch.schema import BOOKS_INDEX, BOOKS_INDEX_SCHEMA

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

def main():
    client = get_client()
    wait_for_yellow(client=client)
    create_index(client=client, index=BOOKS_INDEX, schema=BOOKS_INDEX_SCHEMA)
    mapping = client.indices.get_mapping(index="")
    print(f"Created/verified index '{BOOKS_INDEX}'. Fields: {list(mapping[BOOKS_INDEX]['mappings']['properties'].keys())}")

if __name__ == "__main__":
    main()
