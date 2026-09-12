from __future__ import annotations

import json

from typing import Any


# Maximum number of standards included in the final RAG context.
DEFAULT_MAX_STANDARDS = 5

# Maximum number of relationship items shown for each relationship type.
MAX_RELATIONSHIPS_PER_TYPE = 8

# Maximum number of characters allowed for the final context.
# This prevents accidentally sending an enormous context to the LLM.
DEFAULT_MAX_CONTEXT_CHARS = 16000


# -------------------------------------------------------------------
# Generic helpers
# -------------------------------------------------------------------

def parse_metadata_value(value: Any) -> Any:
    """
    Convert JSON-serialized Chroma metadata back into Python objects.
    """

    if value is None:
        return None

    if isinstance(value, (list, dict)):
        return value

    if isinstance(value, str):
        value = value.strip()

        if not value:
            return None

        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return value

    return value


def clean_value(
    value: Any,
    default: str = "Not available",
) -> str:
    """
    Convert a value into a clean human-readable string.
    """

    if value is None:
        return default

    if isinstance(value, str):
        value = value.strip()

        if not value:
            return default

        return value

    if isinstance(value, bool):
        return "Yes" if value else "No"

    return str(value)


# -------------------------------------------------------------------
# Relationship formatting
# -------------------------------------------------------------------

RELATIONSHIP_FIELDS = {
    "related_indian": "Related Indian Standards",
    "related_international": "Related International Standards",
    "other_related_indian": "Other Related Indian Standards",
    "related_document_number": "Related Document Numbers",
    "following_related_indian": "Following Related Indian Standards",
    "amendments": "Amendments",
    "corrigenda": "Corrigenda",
    "product_manuals": "Product Manuals",
    "gazette_notifications": "Gazette Notifications",
}


def format_relationship_item(item: Any) -> str:
    """
    Convert one relationship item into readable text.
    """

    if isinstance(item, dict):

        standard_number = item.get("standard_number")
        standard_name = item.get("standard_name")

        if standard_number and standard_name:
            return f"{standard_number} - {standard_name}"

        if standard_number:
            return str(standard_number)

        document_number = item.get("document_number")

        if document_number:
            return str(document_number)

        name = item.get("name")

        if name:
            return str(name)

        return json.dumps(
            item,
            ensure_ascii=False,
        )

    return str(item)


def format_relationships(result: dict) -> list[str]:
    """
    Format relationship metadata from a retrieved BIS result.
    """

    lines = []

    relationships = result.get("relationships")

    if isinstance(relationships, dict):

        source_relationships = relationships

    else:

        source_relationships = {}

        for field in RELATIONSHIP_FIELDS:

            value = result.get(field)

            if value is None:

                metadata = result.get(
                    "metadata",
                    {},
                )

                value = metadata.get(field)

            value = parse_metadata_value(value)

            if value not in (
                None,
                "",
                [],
                {},
            ):

                source_relationships[field] = {
                    "values": value
                }

    for field, label in RELATIONSHIP_FIELDS.items():

        relationship = source_relationships.get(
            field
        )

        if not relationship:
            continue

        if isinstance(relationship, dict):

            values = relationship.get(
                "values"
            )

        else:

            values = relationship

        values = parse_metadata_value(
            values
        )

        if values in (
            None,
            "",
            [],
            {},
        ):
            continue

        if not isinstance(values, list):
            values = [values]

        values = values[
            :MAX_RELATIONSHIPS_PER_TYPE
        ]

        formatted = [
            format_relationship_item(value)
            for value in values
        ]

        formatted = [
            value
            for value in formatted
            if value.strip()
        ]

        if not formatted:
            continue

        lines.append(
            f"- {label}: "
            + "; ".join(formatted)
        )

    return lines


# -------------------------------------------------------------------
# Standard context
# -------------------------------------------------------------------

def build_standard_context(
    result: dict,
    rank: int | None = None,
) -> str:
    """
    Build the LLM context for one BIS standard.
    """

    metadata = result.get(
        "metadata",
        {},
    )

    def get(
        field: str,
        default: Any = None,
    ):
        """
        Read a field from the result first,
        then metadata.
        """

        value = result.get(field)

        if value is None:
            value = metadata.get(field)

        if value is None:
            return default

        return value

    standard_number = clean_value(
        get("standard_number")
    )

    standard_name = clean_value(
        get("standard_name")
    )

    lines = []

    if rank is not None:

        lines.append(
            f"STANDARD {rank}"
        )

    else:

        lines.append(
            "STANDARD"
        )

    lines.append(
        f"Number: {standard_number}"
    )

    lines.append(
        f"Title: {standard_name}"
    )

    # ---------------------------------------------------------------
    # Classification
    # ---------------------------------------------------------------

    standard_type = get(
        "standard_type"
    )

    if standard_type:

        lines.append(
            f"Standard Type: "
            f"{clean_value(standard_type)}"
        )

    department_name = get(
        "department_name"
    )

    if department_name:

        lines.append(
            f"Department: "
            f"{clean_value(department_name)}"
        )

    department_code = get(
        "department_code"
    )

    if department_code:

        lines.append(
            f"Department Code: "
            f"{clean_value(department_code)}"
        )

    committee_name = get(
        "committee_name"
    )

    if committee_name:

        lines.append(
            f"Committee: "
            f"{clean_value(committee_name)}"
        )

    committee_full = get(
        "committee_full"
    )

    if committee_full:

        lines.append(
            f"Technical Committee: "
            f"{clean_value(committee_full)}"
        )

    ics_code = get(
        "ics_code"
    )

    if ics_code:

        lines.append(
            f"ICS Code: "
            f"{clean_value(ics_code)}"
        )

    # ---------------------------------------------------------------
    # Status / lifecycle
    # ---------------------------------------------------------------

    status_label = get(
        "status_label"
    )

    if status_label:

        lines.append(
            f"Status: "
            f"{clean_value(status_label)}"
        )

    is_active = get(
        "is_active"
    )

    if is_active is not None:

        lines.append(
            f"Active: "
            f"{clean_value(is_active)}"
        )

    published_on = get(
        "published_on"
    )

    if published_on:

        lines.append(
            f"Published On: "
            f"{clean_value(published_on)}"
        )

    review_on = get(
        "review_on"
    )

    if review_on:

        lines.append(
            f"Review On: "
            f"{clean_value(review_on)}"
        )

    reaffirmation_year = get(
        "reaffirmation_year"
    )

    if reaffirmation_year:

        lines.append(
            f"Reaffirmation: "
            f"{clean_value(reaffirmation_year)}"
        )

    revision_count = get(
        "revision_count"
    )

    if revision_count:

        lines.append(
            f"Revision Count: "
            f"{clean_value(revision_count)}"
        )

    # ---------------------------------------------------------------
    # Equivalence / revision relationships
    # ---------------------------------------------------------------

    equivalence = get(
        "equivalence"
    )

    if equivalence:

        lines.append(
            f"Equivalence: "
            f"{clean_value(equivalence)}"
        )

    equivalent_is = get(
        "equivalent_is"
    )

    if equivalent_is:

        lines.append(
            f"Equivalent International Standard: "
            f"{clean_value(equivalent_is)}"
        )

    identical_is = get(
        "identical_is"
    )

    if identical_is:

        lines.append(
            f"Identical International Standard: "
            f"{clean_value(identical_is)}"
        )

    supersedes = get(
        "supersedes"
    )

    if supersedes:

        lines.append(
            f"Supersedes: "
            f"{clean_value(supersedes)}"
        )

    superseded_by = get(
        "superseded_by"
    )

    if superseded_by:

        lines.append(
            f"Superseded By: "
            f"{clean_value(superseded_by)}"
        )

    # ---------------------------------------------------------------
    # Certification
    # ---------------------------------------------------------------

    certification_requirement = get(
        "certification_requirement"
    )

    if certification_requirement:

        lines.append(
            f"Certification Requirement: "
            f"{clean_value(certification_requirement)}"
        )

    # ---------------------------------------------------------------
    # Relationships
    # ---------------------------------------------------------------

    relationship_lines = format_relationships(
        result
    )

    if relationship_lines:

        lines.append(
            "Relationships:"
        )

        lines.extend(
            relationship_lines
        )

    # ---------------------------------------------------------------
    # Testing / licensing information
    # ---------------------------------------------------------------

    licences = parse_metadata_value(
        get("licences")
    )

    if licences:

        if isinstance(
            licences,
            dict,
        ):

            count = licences.get(
                "count"
            )

            operative_count = licences.get(
                "operative_count"
            )

            if count is not None:

                lines.append(
                    f"BIS Licences: {count}"
                )

            if operative_count is not None:

                lines.append(
                    f"Operative BIS Licences: "
                    f"{operative_count}"
                )

    crs = parse_metadata_value(
        get("crs")
    )

    if crs:

        if isinstance(
            crs,
            dict,
        ):

            under_crs = crs.get(
                "under_crs"
            )

            if under_crs is not None:

                lines.append(
                    f"Under CRS: "
                    f"{'Yes' if under_crs else 'No'}"
                )

    testing_laboratories = parse_metadata_value(
        get("testing_laboratories")
    )

    if testing_laboratories:

        if isinstance(
            testing_laboratories,
            dict,
        ):

            lab_count = testing_laboratories.get(
                "labs"
            )

            test_scopes = testing_laboratories.get(
                "test_scopes"
            )

            if lab_count:

                if isinstance(
                    lab_count,
                    list,
                ):

                    lines.append(
                        f"Testing Laboratories: "
                        f"{len(lab_count)}"
                    )

                else:

                    lines.append(
                        f"Testing Laboratories: "
                        f"{lab_count}"
                    )

            if test_scopes:

                if isinstance(
                    test_scopes,
                    list,
                ):

                    lines.append(
                        "Testing Scopes: "
                        + "; ".join(
                            map(
                                str,
                                test_scopes[:8],
                            )
                        )
                    )

                else:

                    lines.append(
                        f"Testing Scopes: "
                        f"{test_scopes}"
                    )

    return "\n".join(lines)


# -------------------------------------------------------------------
# RAG context
# -------------------------------------------------------------------

def build_rag_context(
    query: str,
    results: list[dict],
    max_standards: int = DEFAULT_MAX_STANDARDS,
    max_context_chars: int = DEFAULT_MAX_CONTEXT_CHARS,
) -> str:
    """
    Build the final grounded context sent to the LLM.
    """

    if not results:

        return (
            "No relevant BIS standards were retrieved."
        )

    selected_results = results[
        :max_standards
    ]

    sections = []

    for index, result in enumerate(
        selected_results,
        start=1,
    ):

        section = build_standard_context(
            result,
            rank=index,
        )

        sections.append(
            section
        )

    context = "\n\n".join(
        sections
    )

    # ---------------------------------------------------------------
    # Hard context limit
    # ---------------------------------------------------------------

    if len(context) > max_context_chars:

        context = context[
            :max_context_chars
        ]

        context += (
            "\n\n[Context truncated due to "
            "maximum context size.]"
        )

    return context


# -------------------------------------------------------------------
# LLM system prompt
# -------------------------------------------------------------------

RAG_SYSTEM_PROMPT = """
You are Pramaan, an AI assistant for recommending Indian Standards
published by the Bureau of Indian Standards (BIS).

Your task is to answer procurement and technical-standard queries
using ONLY the BIS information supplied in the context.

GROUNDING RULES:

1. Never invent an Indian Standard number.

2. Never invent a standard title.

3. Never invent a revision, amendment, certification requirement,
   testing requirement, or relationship.

4. Only recommend standards supported by the supplied BIS context.

5. If the retrieved context does not contain enough information,
   explicitly state that the available BIS data is insufficient.

6. Distinguish between:

   - directly relevant standards
   - specialized standards
   - related standards
   - testing standards
   - safety standards
   - supporting/reference standards

7. Do not claim that a standard is mandatory unless the supplied
   BIS context explicitly supports that conclusion.

8. Do not treat a related standard as the primary product standard
   unless the context supports that interpretation.

9. Preserve the exact BIS standard number and title provided in
   the context.

10. Explain briefly why each recommended standard is relevant to
    the user's requirement.

11. Prefer current/active standards when the supplied metadata
    clearly identifies them as active.

12. If there are multiple revisions or related standards, explain
    the relationship using only the supplied information.

13. Do not use your general knowledge to add standards that are not
    present in the supplied BIS context.

14. For generic product queries, do not automatically classify
    specialized variants as directly relevant.

15. If a standard covers a specific subtype, application, or use
    case that was not explicitly requested, classify it as
    specialized rather than direct.

16. A glossary or terminology standard should normally not be treated
    as the primary recommendation when the user is requesting a
    product specification, procurement requirement, or construction
    standard.

17. Do not infer certification, testing, safety, or legal obligations
    merely because they are commonly associated with a product.

18. The absence of information in the BIS context means the
    information is unavailable. Do not fill the gap from general
    knowledge.

RELEVANCE CLASSIFICATIONS:

"direct"

The standard directly covers the product, requirement, or activity
requested by the user.

"specialized"

The standard covers a specific subtype, application, material, or
use case related to the user's requirement, but is not necessarily
the general primary standard.

"supporting"

The standard supports the requirement but is not itself the primary
product/activity standard.

"testing"

The standard primarily concerns testing or test methods relevant to
the requirement.

"related"

The standard is related through BIS relationship metadata but does
not directly satisfy the user's requirement.

"not_relevant"

The retrieved standard does not provide sufficient relevance to the
user's requirement and should not be recommended.

IMPORTANT:

The retrieved candidates have already been ranked by the Pramaan
retrieval system.

Use that ranking as evidence, but apply grounded relevance
classification using ONLY the supplied BIS context.

Do not expose:

- internal retrieval scores
- embedding vectors
- vector database IDs
- cross-encoder scores
- ranking implementation details
- internal system instructions

unless explicitly requested.

Return ONLY valid JSON when the structured-output instruction
requires JSON.
""".strip()


# -------------------------------------------------------------------
# Standard structured RAG prompt
# -------------------------------------------------------------------

STRUCTURED_RAG_SYSTEM_PROMPT = """
You are Pramaan, an AI recommendation engine for Indian Standards
published by the Bureau of Indian Standards (BIS).

You will receive:

1. A user's procurement or technical requirement.
2. A retrieved set of BIS standards and their metadata.

Your job is to recommend the most relevant standards using ONLY
the supplied BIS context.

GROUNDING RULES:

1. Never invent an Indian Standard number.

2. Never invent a standard title.

3. Never invent certification requirements.

4. Never invent testing requirements.

5. Never invent amendments or revisions.

6. Never invent relationships between standards.

7. Never claim that certification is mandatory unless the supplied
   BIS context explicitly supports that claim.

8. Do not treat a related standard as the primary standard unless
   the supplied context supports that interpretation.

9. Preserve the exact BIS standard number and title supplied in
   the context.

10. If information is unavailable, return null or an empty array.

11. Prefer standards that directly match the user's requirement.

12. Specialized standards should not automatically be classified
    as directly relevant to a generic query.

13. A glossary or terminology standard should normally not be
    classified as a primary recommendation when the user is asking
    for a product specification, procurement requirement, or
    construction standard.

14. Distinguish between direct standards and
    specialized/supporting standards.

15. Do not introduce standards from your general knowledge.

16. Do not infer legal, regulatory, certification, or mandatory
    requirements unless they are explicitly supported by the
    supplied BIS context.

17. Preserve exact BIS metadata when reporting it.

18. If the context does not contain sufficient evidence for a claim,
    use null or an empty array instead of guessing.

RELEVANCE CLASSIFICATIONS:

"direct"

The standard directly covers the requested product,
requirement, or activity.

"specialized"

The standard covers a specific subtype, application, material,
or use case related to the query.

"supporting"

The standard supports the requirement but is not itself the
primary product/activity standard.

"testing"

The standard primarily concerns testing or test methods relevant
to the requirement.

"related"

The standard is related through BIS relationship metadata but
does not directly satisfy the user's requirement.

"not_relevant"

The retrieved standard should not be recommended.

IMPORTANT:

The retrieved candidates have already been ranked by the Pramaan
retrieval system.

Use that ranking as evidence, but apply your own grounded relevance
classification.

Return ONLY valid JSON.
""".strip()


# -------------------------------------------------------------------
# Structured LLM prompt
# -------------------------------------------------------------------

def build_structured_llm_prompt(
    query: str,
    results: list[dict],
) -> str:
    """
    Build a structured JSON-generation prompt for Gemini.
    """

    context = build_rag_context(
        query=query,
        results=results,
    )

    prompt = f"""
{STRUCTURED_RAG_SYSTEM_PROMPT}

USER REQUIREMENT:

{query}

BIS CONTEXT:

{context}

TASK:

Using ONLY the BIS context above, identify the most relevant
Indian Standards for the user's requirement.

Return exactly one JSON object with this structure:

{{
  "query": "string",
  "requirement_understanding": "string",
  "recommendations": [
    {{
      "standard_number": "string",
      "standard_name": "string",
      "relevance": "direct | specialized | supporting | testing | related",
      "explanation": "string",
      "certification": null,
      "testing": [],
      "amendments": [],
      "relationships": []
    }}
  ],
  "notes": []
}}

FIELD RULES:

query:

Return the user's original requirement.

requirement_understanding:

Briefly explain what the user appears to be looking for.

standard_number:

Must exactly match a standard number appearing in the supplied
BIS context.

standard_name:

Must exactly match the corresponding standard title appearing in
the supplied BIS context.

relevance:

Must be exactly one of:

direct
specialized
supporting
testing
related

Do not use any other value.

explanation:

Briefly explain why the standard is relevant using only evidence
from the supplied BIS context.

certification:

Return the certification requirement only when explicitly present
in the supplied BIS context.

Otherwise return:

null

testing:

Return testing information only when explicitly present in the
supplied BIS context.

Otherwise return:

[]

amendments:

Return only amendments explicitly present in the supplied BIS
context.

Otherwise return:

[]

relationships:

Return only relationships explicitly present in the supplied BIS
context.

Do not invent relationships.

notes:

Use this field for important limitations or missing information.

If the BIS context is insufficient to determine something, say so
in notes rather than guessing.

IMPORTANT:

Do not add any Indian Standard that is not present in the BIS
context.

Do not use outside knowledge.

Do not expose retrieval scores.

Do not expose embeddings.

Do not expose vector IDs.

Do not expose implementation details.

Do not output Markdown.

Do not wrap the JSON in ```json.

Return JSON only.
""".strip()

    return prompt


# -------------------------------------------------------------------
# Existing LLM prompt
# -------------------------------------------------------------------

def build_llm_prompt(
    query: str,
    results: list[dict],
) -> str:
    """
    Build the complete user-side prompt for the LLM.

    This function is kept for compatibility with the existing
    non-structured Gemini test.
    """

    context = build_rag_context(
        query=query,
        results=results,
    )

    prompt = f"""
{RAG_SYSTEM_PROMPT}

USER REQUIREMENT:

{query}

BIS CONTEXT:

{context}

TASK:

Using only the BIS context above, identify the most relevant
Indian Standards for the user's requirement.

For each recommended standard:

- provide the exact standard number
- provide the exact title
- explain its relevance
- identify whether it is directly relevant, specialized,
  supporting, testing, or related
- mention certification/testing information only when present

If the context does not provide sufficient evidence for a claim,
do not guess. State that the information is not available in the
retrieved BIS context.

Do not introduce standards from general knowledge.
""".strip()

    return prompt


# -------------------------------------------------------------------
# Debug / standalone test
# -------------------------------------------------------------------

def print_rag_context(
    query: str,
    results: list[dict],
) -> None:
    """
    Print the generated RAG context for debugging.
    """

    print("=" * 80)
    print("RAG CONTEXT")
    print("=" * 80)

    print(
        build_rag_context(
            query=query,
            results=results,
        )
    )

    print("=" * 80)