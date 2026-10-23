
import chromadb
from data.sports_knowledge import SPORTS_KNOWLEDGE

COLLECTION_NAME = "sports_knowledge"

_client = None
_collection = None


def build_collection():
    global _client, _collection

    if _client is None:
        _client = chromadb.EphemeralClient()

    try:
        _collection = _client.get_collection(COLLECTION_NAME)

        if _collection.count() > 0:
            return _collection

    except Exception:
        _collection = _client.create_collection(
            name=COLLECTION_NAME
        )

    if _collection.count() == 0:

        documents = []
        metadatas = []
        ids = []

        for index, item in enumerate(SPORTS_KNOWLEDGE):

            documents.append(item["fact"])

            metadatas.append({
                "sport": item["sport"],
                "category": item["category"],
                "source_title": item["source_title"],
                "grounding_source": "ChromaDB"
            })

            ids.append(f"sports_fact_{index}")

        _collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )

    return _collection


def get_collection():
    global _collection

    if _collection is None:
        return build_collection()

    return _collection


def search_chroma(
    sport,
    query,
    n_results=5
):

    collection = get_collection()

    sport_items = [
        item
        for item in SPORTS_KNOWLEDGE
        if item["sport"] == sport
    ]

    if not sport_items:
        return []

    results = collection.query(
        query_texts=[query],
        n_results=min(n_results, len(sport_items)),
        where={"sport": sport}
    )

    output = []

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    for document, metadata, distance in zip(
        documents,
        metadatas,
        distances
    ):

        output.append({
            "content": document,
            "sport": metadata.get("sport", sport),
            "category": metadata.get("category", "Historical Fact"),
            "source_title": metadata.get(
                "source_title",
                "Sports Knowledge Base"
            ),
            "source_url": None,
            "grounding_source": "ChromaDB",
            "distance": distance
        })

    return output


def format_chroma_context(results):

    if not results:
        return "No relevant ChromaDB facts retrieved."

    parts = []

    for index, item in enumerate(results, start=1):

        parts.append(
            f"""
CHROMA SOURCE {index}
Grounding Source: ChromaDB
Sport: {item['sport']}
Category: {item['category']}
Source Title: {item['source_title']}
Fact: {item['content']}
"""
        )

    return "\n".join(parts)
