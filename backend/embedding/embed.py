import json
from pathlib import Path

# pyright: reportMissingImports=false
try:
    from sentence_transformers import SentenceTransformer
except ImportError as exc:
    raise ImportError(
        "sentence-transformers is required to run this script. "
        "Install it with: pip install sentence-transformers"
    ) from exc


# ============================================================
# PATHS
# ============================================================

# embed_bis.py
#     ↓
# aiml/
#     ↓
# ai services/
BASE_DIR = Path(__file__).resolve().parents[1]

JSONL_FILE = (
    BASE_DIR
    / "data"
    / "master"
    / "bis_enriched_searchtext.jsonl"
)


# ============================================================
# CHECK FILE
# ============================================================

if not JSONL_FILE.exists():
    raise FileNotFoundError(
        f"Dataset not found:\n{JSONL_FILE}"
    )

print("=" * 60)
print("BIS EMBEDDING TEST")
print("=" * 60)

print(f"Dataset: {JSONL_FILE}")


# ============================================================
# READ JSONL
# ============================================================

data = []

with JSONL_FILE.open("r", encoding="utf-8") as f:

    for line_number, line in enumerate(f, start=1):

        line = line.strip()

        if not line:
            continue

        try:
            record = json.loads(line)
            data.append(record)

        except json.JSONDecodeError as e:
            print(
                f"[WARNING] Invalid JSON at line {line_number}: {e}"
            )


print(f"Records: {len(data):,}")


# ============================================================
# LOAD EMBEDDING MODEL
# ============================================================

print("\nLoading BGE model...")

model = SentenceTransformer(
    "BAAI/bge-small-en-v1.5"
)

print("Model loaded.")


# ============================================================
# TEST FIRST RECORD
# ============================================================

sample = data[0]["search_text"]

print("\nSample search_text:")
print("-" * 60)
print(sample[:1000])
print("-" * 60)


# ============================================================
# GENERATE EMBEDDING
# ============================================================

embedding = model.encode(
    [sample],
    normalize_embeddings=True
)[0]


# ============================================================
# RESULT
# ============================================================

print("\nEmbedding information:")
print(f"Embedding size: {len(embedding)}")
print(f"First 10 values: {embedding[:10]}")

print("\n" + "=" * 60)
print("TEST COMPLETE")
print("=" * 60)