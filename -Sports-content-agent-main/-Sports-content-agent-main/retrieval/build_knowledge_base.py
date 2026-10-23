
import os
import sys
import chromadb

PROJECT_PATH = "/content/sports-content-agent"

if PROJECT_PATH not in sys.path:
    sys.path.insert(0, PROJECT_PATH)

from data.sports_knowledge import SPORTS_KNOWLEDGE


CHROMA_PATH = "/content/sports-content-agent/chroma_db"
COLLECTION_NAME = "sports_knowledge"


def build_knowledge_base():

    os.makedirs(
        CHROMA_PATH,
        exist_ok=True
    )

    client = chromadb.PersistentClient(
        path=CHROMA_PATH
    )

    try:
        client.delete_collection(
            COLLECTION_NAME
        )
    except Exception:
        pass

    collection = client.create_collection(
        name=COLLECTION_NAME
    )

    documents = []
    metadatas = []
    ids = []

    for index, item in enumerate(
        SPORTS_KNOWLEDGE
    ):

        documents.append(
            item["fact"]
        )

        metadatas.append(
            {
                "sport": item["sport"],
                "category": item["category"],
                "source_title": item["source_title"],
                "grounding_source": "ChromaDB"
            }
        )

        ids.append(
            f"sports_fact_{index}"
        )

    collection.add(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )

    print(
        f"Knowledge base created with "
        f"{collection.count()} facts ✅"
    )


if __name__ == "__main__":
    build_knowledge_base()
