from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from embedding.rerank_retrieval import search_bis
from embedding.rag_context_builder import build_structured_llm_prompt
from embedding.llm_client import get_llm_client
from embedding.response_models import (
    PramaanResponse,
    RetrievedStandard,
)


llm = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global llm

    print("=" * 60)
    print("Initializing Pramaan backend...")
    print("=" * 60)

    llm = get_llm_client()

    print("Gemini client initialized.")
    print("Pramaan backend ready.")

    yield

    print("Shutting down Pramaan backend...")

    llm = None

    print("Pramaan backend shut down.")


app = FastAPI(
    title="Pramaan API",
    description="AI-powered Indian Standards recommendation engine",
    version="1.0.0",
    lifespan=lifespan,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class RecommendationRequest(BaseModel):
    query: str = Field(
        ...,
        min_length=1,
        description="Procurement or technical requirement",
    )

    retrieval_top_k: int = Field(
        default=30,
        ge=1,
        le=100,
    )

    final_top_k: int = Field(
        default=5,
        ge=1,
        le=20,
    )


PRAMAAN_RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "query": {
            "type": "string"
        },
        "requirement_understanding": {
            "type": "string"
        },
        "recommendations": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "standard_number": {
                        "type": "string"
                    },
                    "standard_name": {
                        "type": "string"
                    },
                    "relevance": {
                        "type": "string",
                        "enum": [
                            "direct",
                            "specialized",
                            "supporting",
                            "testing",
                            "related",
                        ],
                    },
                    "explanation": {
                        "type": "string"
                    },
                    "certification": {
                        "type": [
                            "string",
                            "null",
                        ]
                    },
                    "testing": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        },
                    },
                    "amendments": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        },
                    },
                    "relationships": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        },
                    },
                },
                "required": [
                    "standard_number",
                    "standard_name",
                    "relevance",
                    "explanation",
                    "certification",
                    "testing",
                    "amendments",
                    "relationships",
                ],
            },
        },
        "notes": {
            "type": "array",
            "items": {
                "type": "string"
            },
        },
    },
    "required": [
        "query",
        "requirement_understanding",
        "recommendations",
        "notes",
    ],
}


def build_retrieved_standard(
    result: dict[str, Any],
) -> RetrievedStandard:
    return RetrievedStandard(
        standard_number=result.get(
            "standard_number",
            ""
        ),
        standard_name=result.get(
            "standard_name",
            ""
        ),
        standard_type=result.get(
            "standard_type"
        ),
        department=result.get(
            "metadata",
            {}
        ).get("department"),
        hybrid_score=result.get(
            "hybrid_score"
        ),
    )


def build_retrieved_standards(
    results: list[dict[str, Any]],
) -> list[RetrievedStandard]:
    return [
        build_retrieved_standard(result)
        for result in results
    ]


@app.get("/")
def root():
    return {
        "name": "Pramaan API",
        "status": "running",
        "version": "1.0.0",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "llm_initialized": llm is not None,
    }


@app.post(
    "/recommend",
    response_model=PramaanResponse,
)
def recommend(
    request: RecommendationRequest,
):
    if llm is None:
        raise HTTPException(
            status_code=503,
            detail="LLM client is not initialized.",
        )

    try:
        results = search_bis(
            request.query,
            retrieval_top_k=request.retrieval_top_k,
            final_top_k=request.final_top_k,
        )

        if not results:
            raise HTTPException(
                status_code=404,
                detail="No relevant BIS standards found.",
            )

        prompt = build_structured_llm_prompt(
            request.query,
            results,
        )

        response = llm.generate_json(
            prompt,
            PRAMAAN_RESPONSE_SCHEMA,
            PramaanResponse,
        )

        response.retrieved_standards = (
            build_retrieved_standards(results)
        )

        return response

    except HTTPException:
        raise

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Recommendation generation failed: {exc}",
        )