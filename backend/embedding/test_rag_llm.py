import json

from embedding.rerank_retrieval import search_bis

from embedding.rag_context_builder import (
    build_structured_llm_prompt,
)

from embedding.llm_client import get_llm_client

from embedding.response_models import PramaanResponse


# ============================================================
# Gemini JSON Schema
# ============================================================

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
                            "related"
                        ]
                    },

                    "explanation": {
                        "type": "string"
                    },

                    "certification": {
                        "type": [
                            "string",
                            "null"
                        ]
                    },

                    "testing": {
                        "type": "array",

                        "items": {
                            "type": "string"
                        }
                    },

                    "amendments": {
                        "type": "array",

                        "items": {
                            "type": "string"
                        }
                    },

                    "relationships": {
                        "type": "array",

                        "items": {
                            "type": "string"
                        }
                    }
                },

                "required": [
                    "standard_number",
                    "standard_name",
                    "relevance",
                    "explanation",
                    "certification",
                    "testing",
                    "amendments",
                    "relationships"
                ]
            }
        },

        "notes": {
            "type": "array",

            "items": {
                "type": "string"
            }
        }
    },

    "required": [
        "query",
        "requirement_understanding",
        "recommendations",
        "notes"
    ]
}


# ============================================================
# Main
# ============================================================

def main():

    query = "concrete blocks"

    print("=" * 80)
    print(f"QUERY: {query}")
    print("=" * 80)

    # --------------------------------------------------------
    # 1. Retrieve BIS standards
    # --------------------------------------------------------

    results = search_bis(
        query,
        retrieval_top_k=30,
        final_top_k=5,
    )

    print("\nRETRIEVED STANDARDS")
    print("=" * 80)

    for index, result in enumerate(results, 1):

        print(
            f"\n{index}. "
            f"{result.get('standard_number')} - "
            f"{result.get('standard_name')}"
        )

    # --------------------------------------------------------
    # 2. Build structured RAG prompt
    # --------------------------------------------------------

    prompt = build_structured_llm_prompt(
        query,
        results,
    )

    # --------------------------------------------------------
    # 3. Initialize Gemini
    # --------------------------------------------------------

    llm = get_llm_client()

    # --------------------------------------------------------
    # 4. Generate + validate structured JSON
    # --------------------------------------------------------

    response = llm.generate_json(
        prompt,
        PRAMAAN_RESPONSE_SCHEMA,
        PramaanResponse,
    )

    # --------------------------------------------------------
    # 5. Display validated response
    # --------------------------------------------------------

    print("\n")
    print("=" * 80)
    print("VALIDATED STRUCTURED GEMINI RESPONSE")
    print("=" * 80)

    print(
        response.model_dump_json(
            indent=2
        )
    )


# ============================================================
# Entry Point
# ============================================================

if __name__ == "__main__":
    main()