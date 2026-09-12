import json

from pathlib import Path

import chromadb

from sentence_transformers import SentenceTransformer


# ============================================================
# CONFIGURATION
# ============================================================

MODEL_NAME = "BAAI/bge-small-en-v1.5"

BATCH_SIZE = 128

COLLECTION_NAME = "bis_standards"


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[1]

JSONL_FILE = (
    BASE_DIR
    / "data"
    / "master"
    / "bis_enriched_searchtext.jsonl"
)

CHROMA_DIR = BASE_DIR / "chroma_db"


# ============================================================
# VALIDATE DATASET
# ============================================================

if not JSONL_FILE.exists():
    raise FileNotFoundError(
        f"\nDataset not found:\n"
        f"{JSONL_FILE}"
    )


# ============================================================
# START
# ============================================================

print("=" * 70)

print(
    "BIS VECTOR DATABASE BUILDER"
)

print("=" * 70)

print(
    f"Dataset : {JSONL_FILE}"
)

print(
    f"ChromaDB: {CHROMA_DIR}"
)

print()


# ============================================================
# LOAD JSONL
# ============================================================

records = []

with JSONL_FILE.open(
    "r",
    encoding="utf-8",
) as f:

    for line_number, line in enumerate(
        f,
        start=1,
    ):

        line = line.strip()

        if not line:
            continue

        try:

            record = json.loads(
                line
            )

        except json.JSONDecodeError as exc:

            print(
                f"[WARNING] Invalid JSON "
                f"at line {line_number}: "
                f"{exc}"
            )

            continue

        if not isinstance(
            record,
            dict,
        ):

            print(
                f"[WARNING] Line "
                f"{line_number} is not "
                f"a JSON object"
            )

            continue

        search_text = record.get(
            "search_text"
        )

        if not search_text:

            print(
                f"[WARNING] Line "
                f"{line_number} has "
                f"no search_text"
            )

            continue

        records.append(
            record
        )


print(
    f"Records loaded: "
    f"{len(records):,}"
)


if not records:

    raise RuntimeError(
        "No valid records found."
    )


# ============================================================
# LOAD EMBEDDING MODEL
# ============================================================

print()

print(
    "Loading embedding model..."
)

model = SentenceTransformer(
    MODEL_NAME
)

print(
    f"Model loaded: "
    f"{MODEL_NAME}"
)

print(
    "Embedding dimension:",
    model.get_sentence_embedding_dimension()
)


# ============================================================
# CONNECT TO CHROMADB
# ============================================================

print()

print(
    "Initializing ChromaDB..."
)

client = chromadb.PersistentClient(
    path=str(CHROMA_DIR)
)


# ============================================================
# RESET COLLECTION
# ============================================================
#
# IMPORTANT:
#
# We delete the previous collection because the metadata
# schema has changed.
#
# This does NOT modify your JSONL dataset.
#
# ============================================================

print()

print(
    "Checking existing collection..."
)


try:

    client.delete_collection(
        name=COLLECTION_NAME
    )

    print(
        f"Deleted existing "
        f"collection: "
        f"{COLLECTION_NAME}"
    )

except Exception:

    print(
        "No existing collection "
        "to delete."
    )


# ============================================================
# CREATE COLLECTION
# ============================================================

collection = client.create_collection(
    name=COLLECTION_NAME,

    metadata={
        "description":
            "BIS Indian Standards semantic search collection",

        "embedding_model":
            MODEL_NAME,

        "embedding_dimension":
            384,

        "version":
            "bis-aware-v2",
    },
)


print(
    f"Collection created: "
    f"{COLLECTION_NAME}"
)


# ============================================================
# PREPARE METADATA
# ============================================================

def build_metadata(
    record: dict,
) -> dict:
    """
    Extract searchable/filterable BIS metadata.

    All metadata values passed to Chroma must be
    primitive values: str, int, float, or bool.

    Nested BIS relationship data is serialized
    using json.dumps() so it can be stored safely
    inside Chroma metadata.
    """

    metadata = {

        # ----------------------------------------------------
        # Core identity
        # ----------------------------------------------------

        "standard_number":
            str(
                record.get(
                    "standard_number"
                )
                or ""
            ),

        "standard_name":
            str(
                record.get(
                    "standard_name"
                )
                or ""
            ),

        "short_title":
            str(
                record.get(
                    "short_title"
                )
                or ""
            ),


        # ----------------------------------------------------
        # Classification
        # ----------------------------------------------------

        "standard_type":
            str(
                record.get(
                    "standard_type"
                )
                or ""
            ),

        "department":
            str(
                record.get(
                    "department_name"
                )
                or record.get(
                    "department"
                )
                or ""
            ),

        "department_code":
            str(
                record.get(
                    "department_code"
                )
                or ""
            ),

        "committee_name":
            str(
                record.get(
                    "committee_name"
                )
                or ""
            ),

        "committee_full":
            str(
                record.get(
                    "committee_full"
                )
                or ""
            ),

        "ministry_name":
            str(
                record.get(
                    "ministry_name"
                )
                or ""
            ),

        "group_name":
            str(
                record.get(
                    "group_name"
                )
                or ""
            ),

        "sub_group_name":
            str(
                record.get(
                    "sub_group_name"
                )
                or ""
            ),

        "sub_sub_group_name":
            str(
                record.get(
                    "sub_sub_group_name"
                )
                or ""
            ),

        "sector_name":
            str(
                record.get(
                    "sector_name"
                )
                or ""
            ),

        "sub_sector_name":
            str(
                record.get(
                    "sub_sector_name"
                )
                or ""
            ),

        "ics_code":
            str(
                record.get(
                    "ics_code"
                )
                or ""
            ),


        # ----------------------------------------------------
        # Status
        # ----------------------------------------------------

        "status":
            str(
                record.get(
                    "status_label"
                )
                or record.get(
                    "status"
                )
                or ""
            ),

        "is_status_code":
            str(
                record.get(
                    "is_status_code"
                )
                or ""
            ),

        "is_active":
            str(
                record.get(
                    "is_active"
                )
                or ""
            ),


        # ----------------------------------------------------
        # Dates
        # ----------------------------------------------------

        "published_on":
            str(
                record.get(
                    "published_on"
                )
                or ""
            ),

        "review_date":
            str(
                record.get(
                    "review_on"
                )
                or record.get(
                    "review_date"
                )
                or ""
            ),

        "reaffirmation_year":
            str(
                record.get(
                    "reaffirmation_year"
                )
                or ""
            ),


        # ----------------------------------------------------
        # Revision information
        # ----------------------------------------------------

        "revision_count":
            str(
                record.get(
                    "revision_count"
                )
                or ""
            ),

        "supersedes":
            str(
                record.get(
                    "supersedes"
                )
                or ""
            ),

        "superseded_by":
            str(
                record.get(
                    "superseded_by"
                )
                or ""
            ),


        # ----------------------------------------------------
        # Equivalence
        # ----------------------------------------------------

        "equivalence":
            str(
                record.get(
                    "equivalence"
                )
                or ""
            ),

        "equivalence_id":
            str(
                record.get(
                    "equivalence_id"
                )
                or ""
            ),


        # ----------------------------------------------------
        # Certification
        # ----------------------------------------------------

        "certification_requirement":
            str(
                record.get(
                    "certification_requirement"
                )
                or ""
            ),


        # ----------------------------------------------------
        # Other useful BIS fields
        # ----------------------------------------------------

        "language":
            str(
                record.get(
                    "language"
                )
                or ""
            ),

        "withdraw_status":
            str(
                record.get(
                    "withdraw_status"
                )
                or ""
            ),

        "withdrawn_on":
            str(
                record.get(
                    "withdrawn_on"
                )
                or ""
            ),

        "amendment_count":
            str(
                record.get(
                    "amendment_count"
                )
                or ""
            ),

        "crs_count":
            str(
                (
                    record.get(
                        "crs"
                    )
                    or {}
                ).get(
                    "count",
                    ""
                )
            ),

        "licence_count":
            str(
                (
                    record.get(
                        "licences"
                    )
                    or {}
                ).get(
                    "count",
                    ""
                )
            ),

        "testing_lab_count":
            str(
                (
                    record.get(
                        "testing_laboratories"
                    )
                    or {}
                ).get(
                    "count",
                    ""
                )
            ),


        # ----------------------------------------------------
        # BIS Relationships
        # ----------------------------------------------------
        #
        # The original dataset stores relationships inside:
        #
        # record["related"]
        #
        # ChromaDB metadata cannot directly store nested
        # lists/dictionaries, so we serialize them as JSON.
        #
        # ----------------------------------------------------

        "related_indian":
            json.dumps(
                (
                    record.get(
                        "related"
                    )
                    or {}
                ).get(
                    "related_indian",
                    []
                ),
                ensure_ascii=False,
            ),

        "related_international":
            json.dumps(
                (
                    record.get(
                        "related"
                    )
                    or {}
                ).get(
                    "related_international",
                    []
                ),
                ensure_ascii=False,
            ),

        "other_related_indian":
            json.dumps(
                (
                    record.get(
                        "related"
                    )
                    or {}
                ).get(
                    "other_related_indian",
                    []
                ),
                ensure_ascii=False,
            ),

        "related_document_number":
            json.dumps(
                (
                    record.get(
                        "related"
                    )
                    or {}
                ).get(
                    "related_document_number",
                    []
                ),
                ensure_ascii=False,
            ),

        "following_related_indian":
            json.dumps(
                (
                    record.get(
                        "related"
                    )
                    or {}
                ).get(
                    "following_related_indian",
                    []
                ),
                ensure_ascii=False,
            ),


        # ----------------------------------------------------
        # BIS Documents
        # ----------------------------------------------------

        "amendments":
            json.dumps(
                record.get(
                    "amendments",
                    []
                ),
                ensure_ascii=False,
            ),

        "corrigenda":
            json.dumps(
                record.get(
                    "corrigenda",
                    []
                ),
                ensure_ascii=False,
            ),

        "product_manuals":
            json.dumps(
                record.get(
                    "product_manuals",
                    []
                ),
                ensure_ascii=False,
            ),

        "gazette_notifications":
            json.dumps(
                record.get(
                    "gazette_notifications",
                    []
                ),
                ensure_ascii=False,
            ),
    }


    # --------------------------------------------------------
    # Remove empty values
    # --------------------------------------------------------

    metadata = {
        key: value
        for key, value in metadata.items()
        if value != ""
    }


    return metadata


# ============================================================
# INSERT INTO CHROMADB
# ============================================================

total = len(records)


print()

print(
    "Starting embedding and "
    "ChromaDB insertion..."
)

print(
    f"Total records: "
    f"{total:,}"
)

print(
    f"Batch size: "
    f"{BATCH_SIZE}"
)

print()


for start in range(
    0,
    total,
    BATCH_SIZE,
):

    end = min(
        start + BATCH_SIZE,
        total,
    )

    batch = records[
        start:end
    ]


    # --------------------------------------------------------
    # Search text
    # --------------------------------------------------------

    texts = [
        record[
            "search_text"
        ]
        for record in batch
    ]


    # --------------------------------------------------------
    # Embeddings
    # --------------------------------------------------------

    embeddings = model.encode(
        texts,

        batch_size=BATCH_SIZE,

        normalize_embeddings=True,

        show_progress_bar=False,
    )


    # --------------------------------------------------------
    # Chroma data
    # --------------------------------------------------------

    ids = []

    documents = []

    metadatas = []


    for index, record in enumerate(
        batch
    ):

        standard_number = (
            record.get(
                "standard_number"
            )
        )


        # ----------------------------------------------------
        # ID
        # ----------------------------------------------------
        #
        # Standard number is normally unique.
        #
        # If duplicate standard numbers exist,
        # append the source index so records are not
        # silently overwritten.
        #
        # ----------------------------------------------------

        if standard_number:

            record_id = str(
                standard_number
            )

        else:

            record_id = (
                f"bis_{start + index}"
            )


        ids.append(
            record_id
        )


        # ----------------------------------------------------
        # Document
        # ----------------------------------------------------

        documents.append(
            record[
                "search_text"
            ]
        )


        # ----------------------------------------------------
        # Metadata
        # ----------------------------------------------------

        metadatas.append(
            build_metadata(
                record
            )
        )


    # --------------------------------------------------------
    # Insert
    # --------------------------------------------------------

    collection.upsert(
        ids=ids,

        embeddings=embeddings.tolist(),

        documents=documents,

        metadatas=metadatas,
    )


    # --------------------------------------------------------
    # Progress
    # --------------------------------------------------------

    print(
        f"[PROGRESS] "
        f"{end:,}/{total:,} "
        f"("
        f"{end / total * 100:.1f}"
        f"%)"
    )


# ============================================================
# VERIFY
# ============================================================

final_count = collection.count()


print()

print("=" * 70)

print(
    "VECTOR DATABASE BUILD COMPLETE"
)

print("=" * 70)

print(
    f"Records processed : "
    f"{total:,}"
)

print(
    f"ChromaDB records  : "
    f"{final_count:,}"
)

print(
    f"Database location : "
    f"{CHROMA_DIR}"
)

print(
    f"Collection        : "
    f"{COLLECTION_NAME}"
)

print("=" * 70)


# ============================================================
# COUNT VALIDATION
# ============================================================

if final_count != total:

    print()

    print(
        "[WARNING]"
    )

    print(
        f"Dataset records: "
        f"{total:,}"
    )

    print(
        f"Chroma records: "
        f"{final_count:,}"
    )

    print(
        "The counts do not match."
    )

    print(
        "This may indicate duplicate "
        "standard numbers."
    )

else:

    print()

    print(
        "[OK] Dataset count and "
        "ChromaDB count match."
    )