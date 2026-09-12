
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer


# ============================================================
# CONFIG
# ============================================================

MODEL_NAME = "BAAI/bge-small-en-v1.5"
COLLECTION_NAME = "bis_standards"
TOP_K = 10

BASE_DIR = Path(__file__).resolve().parents[1]
CHROMA_DIR = BASE_DIR / "chroma_db"


# ============================================================
# CHECK CHROMADB
# ============================================================

if not CHROMA_DIR.exists():
    raise FileNotFoundError(
        f"ChromaDB directory not found:\n{CHROMA_DIR}\n\n"
        "Run build_vector_db.py first."
    )


# ============================================================
# LOAD EMBEDDING MODEL
# ============================================================

print("=" * 70)
print("BIS SEMANTIC RETRIEVAL TEST")
print("=" * 70)

print("\nLoading embedding model...")

model = SentenceTransformer(MODEL_NAME)

print(f"Model loaded: {MODEL_NAME}")


# ============================================================
# CONNECT TO CHROMADB
# ============================================================

print("\nConnecting to ChromaDB...")

client = chromadb.PersistentClient(
    path=str(CHROMA_DIR)
)

collection = client.get_collection(
    name=COLLECTION_NAME
)

print(f"Collection: {COLLECTION_NAME}")
print(f"Records: {collection.count():,}")


# ============================================================
# QUERY FUNCTION
# ============================================================

def search_bis(query: str, top_k: int = TOP_K):

    print("\n" + "=" * 70)
    print(f"QUERY: {query}")
    print("=" * 70)

    # Convert user query into embedding
    query_embedding = model.encode(
        query,
        normalize_embeddings=True
    ).tolist()

    # Search ChromaDB
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=[
            "documents",
            "metadatas",
            "distances"
        ]
    )

    ids = results["ids"][0]
    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    # Display results
    for i in range(len(ids)):

        metadata = metadatas[i]

        print(f"\n{'-' * 70}")
        print(f"Rank       : {i + 1}")
        print(f"Distance   : {distances[i]:.4f}")
        print(
            f"Standard   : "
            f"{metadata.get('standard_number', 'N/A')}"
        )
        print(
            f"Title      : "
            f"{metadata.get('standard_name', 'N/A')}"
        )
        print(
            f"Department : "
            f"{metadata.get('department', 'N/A')}"
        )
        print(
            f"Type       : "
            f"{metadata.get('standard_type', 'N/A')}"
        )
        print(
            f"Status     : "
            f"{metadata.get('status', 'N/A')}"
        )
        print(
            f"Active     : "
            f"{metadata.get('is_active', 'N/A')}"
        )

        print("\nSearch text:")
        print(documents[i][:800])


# ============================================================
# TEST QUERIES
# ============================================================

queries = [
    "500 KVA outdoor distribution transformer",
    "cement concrete for construction",
    "personal protective equipment for industrial workers",
    "medical oxygen cylinders",
    "steel reinforcement bars for concrete",
    "drinking water quality",
    "solar photovoltaic modules",
    "automobile tyres",
]


# ============================================================
# RUN TESTS
# ============================================================

for query in queries:
    search_bis(query)


print("\n" + "=" * 70)
print("RETRIEVAL TEST COMPLETE")
print("=" * 70)
