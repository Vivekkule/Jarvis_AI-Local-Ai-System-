import chromadb
from sentence_transformers import SentenceTransformer
import datetime, hashlib

# Load embedding model (runs locally, no API needed)
print("Loading memory model...")
embed_model = SentenceTransformer("all-MiniLM-L6-v2")

# Local persistent database saved in your project folder
db_client = chromadb.PersistentClient(path="./jarvis_memory_db")
collection = db_client.get_or_create_collection("jarvis_memories")

def remember(text: str):
    doc_id = hashlib.md5(
        (text + str(datetime.datetime.now())).encode()
    ).hexdigest()
    embedding = embed_model.encode(text).tolist()
    collection.upsert(
        documents=[text],
        embeddings=[embedding],
        ids=[doc_id],
        metadatas=[{"timestamp": str(datetime.datetime.now())}]
    )
    return doc_id

def recall(query: str, n: int = 3) -> list:
    embedding = embed_model.encode(query).tolist()
    try:
        results = collection.query(
            query_embeddings=[embedding],
            n_results=n
        )
        return results["documents"][0] if results["documents"] else []
    except:
        return []

def forget_all():
    db_client.delete_collection("jarvis_memories")
    print("Memory cleared.")