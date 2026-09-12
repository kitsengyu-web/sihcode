import json
from typing import Any


# ============================================================
# CONFIGURATION
# ============================================================

MAX_RELATIONSHIPS_PER_TYPE = 5


# ============================================================
# HELPERS
# ============================================================

def safe_json_loads(value: Any) -> Any:
    """
    Safely parse JSON stored inside Chroma metadata.
    """

    if value is None:
        return None

    if isinstance(value, (list, dict)):
        return value

    if not isinstance(value, str):
        return value

    value = value.strip()

    if not value:
        return None

    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return value


def get_metadata(result: dict) -> dict:
    """
    Supports results where metadata is stored under
    result['metadata'] as well as flattened results.
    """

    metadata = result.get("metadata")

    if isinstance(metadata, dict):
        return metadata

    return result


def get_value(result: dict, key: str, default=None):
    """
    Get a value from either the result itself or its metadata.
    """

    if key in result:
        return result[key]

    metadata = result.get("metadata", {})

    if isinstance(metadata, dict):
        return metadata.get(key, default)

    return default


# ============================================================
# RELATIONSHIP EXTRACTION
# ============================================================

RELATIONSHIP_FIELDS = {
    "related_indian": "Related Indian Standards",
    "related_international": "Related International Standards",
    "other_related_indian": "Other Related Indian Standards",
    "following_related_indian": "Following Related Indian Standards",
}


def extract_relationships(result: dict) -> dict:
    """
    Extract already-filtered relationships.

    Priority:
        filtered_relationships
        relationships
        raw metadata
    """

    filtered = result.get("filtered_relationships")

    if isinstance(filtered, dict):
        return filtered

    relationships = result.get("relationships")

    if isinstance(relationships, dict):
        extracted = {}

        for relationship_type, value in relationships.items():

            if isinstance(value, dict):
                values = value.get("values", [])

            else:
                values = value

            if isinstance(values, list):
                extracted[relationship_type] = values

        return extracted

    metadata = get_metadata(result)

    extracted = {}

    for relationship_type in RELATIONSHIP_FIELDS:

        value = metadata.get(relationship_type)

        value = safe_json_loads(value)

        if isinstance(value, list) and value:
            extracted[relationship_type] = value

    return extracted


# ============================================================
# FORMAT STANDARD
# ============================================================

def format_standard_reference(standard: Any) -> str:

    if isinstance(standard, str):
        return standard

    if not isinstance(standard, dict):
        return str(standard)

    number = (
        standard.get("standard_number")
        or standard.get("standard")
        or "Unknown"
    )

    name = (
        standard.get("standard_name")
        or standard.get("title")
        or ""
    )

    if name:
        return f"{number} - {name}"

    return str(number)


# ============================================================
# CORE STANDARD CONTEXT
# ============================================================

def build_standard_context(result: dict) -> dict:
    """
    Extract only useful BIS information from a ranked result.
    """

    metadata = get_metadata(result)

    context = {
        "standard_number": get_value(
            result,
            "standard_number",
            "Unknown",
        ),

        "standard_name": get_value(
            result,
            "standard_name",
            "Unknown",
        ),

        "short_title": get_value(
            result,
            "short_title",
        ),

        "standard_type": get_value(
            result,
            "standard_type",
        ),

        "department": get_value(
            result,
            "department",
        ),

        "department_name": get_value(
            result,
            "department_name",
        ),

        "committee_name": get_value(
            result,
            "committee_name",
        ),

        "ics_code": get_value(
            result,
            "ics_code",
        ),

        "status": get_value(
            result,
            "status_label",
        ),

        "is_active": get_value(
            result,
            "is_active",
        ),

        "published_on": get_value(
            result,
            "published_on",
        ),

        "review_on": get_value(
            result,
            "review_on",
        ),

        "reaffirmation_year": get_value(
            result,
            "reaffirmation_year",
        ),

        "revision_count": get_value(
            result,
            "revision_count",
        ),

        "certification_requirement": get_value(
            result,
            "certification_requirement",
        ),

        "equivalence": get_value(
            result,
            "equivalence",
        ),

        "equivalent_is": get_value(
            result,
            "equivalent_is",
        ),

        "identical_is": get_value(
            result,
            "identical_is",
        ),

        "supersedes": get_value(
            result,
            "supersedes",
        ),

        "superseded_by": get_value(
            result,
            "superseded_by",
        ),
    }

    # Remove empty fields
    context = {
        key: value
        for key, value in context.items()
        if value not in (None, "", [], {})
    }

    return context


# ============================================================
# RELATED DOCUMENTS
# ============================================================

DOCUMENT_FIELDS = {
    "amendments": "Amendments",
    "corrigenda": "Corrigenda",
    "product_manuals": "Product Manuals",
    "gazette_notifications": "Gazette Notifications",
    "testing_laboratories": "Testing Laboratories",
    "licences": "BIS Licences",
    "crs": "CRS",
}


def extract_documents(result: dict) -> dict:

    documents = {}
    metadata = get_metadata(result)

    for field, label in DOCUMENT_FIELDS.items():

        value = metadata.get(field)

        value = safe_json_loads(value)

        if value in (None, "", [], {}):
            continue

        documents[field] = {
            "label": label,
            "values": value,
        }

    return documents


# ============================================================
# FILTER RELATIONSHIPS
# ============================================================

def build_relationship_context(
    result: dict,
    max_per_type: int = MAX_RELATIONSHIPS_PER_TYPE,
) -> dict:

    relationships = extract_relationships(result)

    cleaned = {}

    for relationship_type, values in relationships.items():

        if not isinstance(values, list):
            continue

        formatted = []

        for value in values[:max_per_type]:

            if isinstance(value, dict):

                standard_number = (
                    value.get("standard_number")
                    or value.get("standard")
                )

                standard_name = (
                    value.get("standard_name")
                    or value.get("title")
                )

                item = {}

                if standard_number:
                    item["standard_number"] = standard_number

                if standard_name:
                    item["standard_name"] = standard_name

                if "relationship_score" in value:
                    item["relationship_score"] = value[
                        "relationship_score"
                    ]

                if item:
                    formatted.append(item)

            else:
                formatted.append(str(value))

        if formatted:
            cleaned[relationship_type] = formatted

    return cleaned


# ============================================================
# COMPLETE RAG CONTEXT
# ============================================================

def build_rag_context(
    ranked_results: list[dict],
    max_standards: int = 5,
) -> dict:
    """
    Build the final structured context that will be sent to the LLM.

    The LLM receives:
        - ranked BIS standards
        - metadata
        - filtered relationships
        - amendments/corrigenda
        - certification information

    It does NOT receive raw ChromaDB results.
    """

    standards = []

    for rank, result in enumerate(
        ranked_results[:max_standards],
        start=1,
    ):

        standard_context = build_standard_context(result)

        standard_context["rank"] = rank

        # Retrieval scores
        if "hybrid_score" in result:
            standard_context["retrieval_score"] = round(
                float(result["hybrid_score"]),
                4,
            )

        if "cross_encoder_score" in result:
            standard_context["cross_encoder_score"] = round(
                float(result["cross_encoder_score"]),
                4,
            )

        # Relationships
        relationships = build_relationship_context(result)

        if relationships:
            standard_context["relationships"] = relationships

        # BIS documents
        documents = extract_documents(result)

        if documents:
            standard_context["documents"] = documents

        # Useful BIS URLs
        bis_url = get_value(
            result,
            "bis_detail_url",
        )

        pdf_path = get_value(
            result,
            "pdf_path",
        )

        if bis_url:
            standard_context["bis_detail_url"] = bis_url

        if pdf_path:
            standard_context["pdf_path"] = pdf_path

        standards.append(standard_context)

    return {
        "source": "BIS Indian Standards dataset",
        "grounding_policy": (
            "Only recommend standards present in the retrieved "
            "BIS context. Do not invent standard numbers."
        ),
        "standards": standards,
    }


# ============================================================
# LLM-READY TEXT
# ============================================================

def build_llm_context(
    query: str,
    ranked_results: list[dict],
    max_standards: int = 5,
) -> str:
    """
    Convert the structured RAG context into a clean text block
    for the LLM prompt.
    """

    rag_context = build_rag_context(
        ranked_results=ranked_results,
        max_standards=max_standards,
    )

    lines = []

    lines.append("BIS RETRIEVED CONTEXT")
    lines.append("=" * 60)

    lines.append(f"User Requirement: {query}")
    lines.append("")

    lines.append(
        "IMPORTANT: "
        "The following standards were retrieved from the BIS dataset. "
        "Use only these standards when making recommendations."
    )

    lines.append("")

    for standard in rag_context["standards"]:

        lines.append(
            f"{standard['rank']}. "
            f"{standard.get('standard_number', 'Unknown')}"
        )

        lines.append(
            f"Title: "
            f"{standard.get('standard_name', 'Unknown')}"
        )

        if "short_title" in standard:
            lines.append(
                f"Short Title: {standard['short_title']}"
            )

        if "department_name" in standard:
            lines.append(
                f"Department: {standard['department_name']}"
            )

        if "committee_name" in standard:
            lines.append(
                f"Committee: {standard['committee_name']}"
            )

        if "status" in standard:
            lines.append(
                f"Status: {standard['status']}"
            )

        if "published_on" in standard:
            lines.append(
                f"Published: {standard['published_on']}"
            )

        if "revision_count" in standard:
            lines.append(
                f"Revision Count: {standard['revision_count']}"
            )

        if "certification_requirement" in standard:
            lines.append(
                "Certification Requirement: "
                f"{standard['certification_requirement']}"
            )

        if "supersedes" in standard:
            lines.append(
                f"Supersedes: {standard['supersedes']}"
            )

        if "superseded_by" in standard:
            lines.append(
                f"Superseded By: {standard['superseded_by']}"
            )

        relationships = standard.get(
            "relationships",
            {},
        )

        if relationships:

            lines.append("Relationships:")

            for relationship_type, values in relationships.items():

                label = RELATIONSHIP_FIELDS.get(
                    relationship_type,
                    relationship_type,
                )

                lines.append(f"  {label}:")

                for value in values:

                    if isinstance(value, dict):

                        number = value.get(
                            "standard_number",
                            "Unknown",
                        )

                        name = value.get(
                            "standard_name",
                            "",
                        )

                        if name:
                            lines.append(
                                f"    - {number} - {name}"
                            )
                        else:
                            lines.append(
                                f"    - {number}"
                            )

                    else:
                        lines.append(
                            f"    - {value}"
                        )

        documents = standard.get(
            "documents",
            {},
        )

        if documents:

            lines.append("Related BIS Documents:")

            for document in documents.values():

                label = document["label"]
                values = document["values"]

                if isinstance(values, list):

                    for value in values[:5]:
                        lines.append(
                            f"  - {label}: "
                            f"{format_standard_reference(value)}"
                        )

                else:

                    lines.append(
                        f"  - {label}: {values}"
                    )

        lines.append("")

    return "\n".join(lines)


# ============================================================
# DEBUG
# ============================================================

def print_rag_context(
    query: str,
    ranked_results: list[dict],
) -> None:

    context = build_llm_context(
        query=query,
        ranked_results=ranked_results,
    )

    print()
    print(context)
    print()