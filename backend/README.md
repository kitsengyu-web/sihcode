# Pramaan — BIS Standards Recommendation Engine

> **SIH 2026** — AI-powered Indian Standards recommendation engine using grounded RAG.

Pramaan retrieves and recommends Bureau of Indian Standards (BIS) standards for procurement and technical requirements using semantic search, cross-encoder reranking, and Gemini-powered reasoning — all grounded in real BIS data.

---

## Architecture

```
User Query
    │
    ▼
FastAPI  (/recommend)
    │
    ├── BGE Semantic Retrieval (ChromaDB)
    │
    ├── Cross-Encoder Reranking
    │
    ├── BIS-Aware Hybrid Ranking
    │
    ├── Relationship Expansion & Filtering
    │
    ├── RAG Context Builder
    │
    └── Gemini (Structured JSON + Grounding)
            │
            ▼
      Validated BIS Recommendations
```

## Tech Stack

| Component | Technology |
|-----------|-----------|
| API | FastAPI + Uvicorn |
| Embeddings | `BAAI/bge-small-en-v1.5` via sentence-transformers |
| Vector DB | ChromaDB (persistent) |
| Reranker | `cross-encoder/ms-marco-MiniLM-L-6-v2` |
| LLM | Google Gemini (`gemini-3.8-flash`) |
| Validation | Pydantic v2 |

## Setup

### 1. Clone & install dependencies

```bash
git clone https://github.com/kitsengyu-web/sihcode.git
cd sihcode/backend
pip install -r requirements.txt
```

### 2. Configure environment

```bash
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
```

### 3. Build the vector database

> You need the BIS dataset file `data/master/bis_enriched_searchtext.jsonl` (not included in the repo due to size).

```bash
python -m embedding.build_vector_db
```

### 4. Run the API

```bash
uvicorn api.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.  
Swagger docs: `http://127.0.0.1:8000/docs`

## API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| `GET` | `/` | Status check |
| `GET` | `/health` | Health + LLM initialization status |
| `POST` | `/recommend` | Generate BIS recommendations |

### POST `/recommend`

```json
{
  "query": "500 KVA outdoor distribution transformer",
  "retrieval_top_k": 30,
  "final_top_k": 5
}
```

See [Pramaan_Frontend_API_Integration_Guide.txt](./Pramaan_Frontend_API_Integration_Guide.txt) for the full API reference.

## Project Structure

```
backend/
├── api/
│   └── main.py                  # FastAPI application
├── embedding/
│   ├── build_vector_db.py       # ChromaDB vector DB builder
│   ├── embed.py                 # BGE embedding test
│   ├── llm_client.py            # Gemini client wrapper
│   ├── rag_context_builder.py   # RAG context + LLM prompt
│   ├── relationship_expansion.py # BIS relationship expansion
│   ├── relationship_filter.py   # Query-aware relationship filtering
│   ├── rerank_retrieval.py      # Hybrid retrieval + reranking
│   ├── response_models.py       # Pydantic response models
│   ├── test_rag_llm.py          # End-to-end RAG test
│   ├── test_relationships.py    # Relationship test
│   └── test_retrieval.py        # Retrieval test
├── evaluation/
│   ├── evaluate_retrieval.py    # Retrieval evaluation
│   ├── metrics.py               # Recall@K, MRR, nDCG
│   └── queries.json             # Evaluation queries
├── rag/
│   └── context_builder.py       # Structured RAG context builder
├── .env.example
├── requirements.txt
└── README.md
```

## License

SIH 2026 project.
