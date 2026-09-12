import json
from typing import Any


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


def parse_metadata_value(value: Any) -> Any:
    """
    Convert JSON-encoded Chroma metadata back into Python objects.
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


def extract_relationships(result: dict) -> dict:
    """
    Extract BIS relationship metadata from a retrieved result.
    """

    metadata = result.get("metadata", {})

    relationships = {}

    for field, label in RELATIONSHIP_FIELDS.items():

        value = metadata.get(field)

        if value is None:
            # Also allow fields directly on the result.
            value = result.get(field)

        value = parse_metadata_value(value)

        if value in (None, "", [], {}):
            continue

        relationships[field] = {
            "label": label,
            "values": value,
        }

    return relationships


def expand_relationships(results: list[dict]) -> list[dict]:
    """
    Add relationship information to retrieved BIS results.
    """

    expanded_results = []

    for result in results:

        expanded = dict(result)

        expanded["relationships"] = extract_relationships(result)

        expanded_results.append(expanded)

    return expanded_results


def build_relationship_context(result: dict) -> str:
    """
    Convert BIS relationship metadata into readable context.
    """

    standard_number = result.get(
        "standard_number",
        "Unknown"
    )

    standard_name = result.get(
        "standard_name",
        "Unknown"
    )

    lines = [
        f"Standard: {standard_number}",
        f"Title: {standard_name}",
    ]

    relationships = result.get(
        "relationships",
        {}
    )

    if not relationships:

        lines.append(
            "Relationships: None available"
        )

        return "\n".join(lines)

    lines.append("Relationships:")

    for relationship in relationships.values():

        label = relationship["label"]
        values = relationship["values"]

        if isinstance(values, list):

            formatted_values = []

            for value in values:

                if isinstance(value, dict):

                    standard_number = value.get(
                        "standard_number"
                    )

                    standard_name = value.get(
                        "standard_name"
                    )

                    if standard_number and standard_name:

                        formatted_values.append(
                            f"{standard_number} - {standard_name}"
                        )

                    elif standard_number:

                        formatted_values.append(
                            standard_number
                        )

                    else:

                        formatted_values.append(
                            str(value)
                        )

                else:

                    formatted_values.append(
                        str(value)
                    )

            lines.append(
                f"- {label}: "
                + "; ".join(formatted_values)
            )

        else:

            lines.append(
                f"- {label}: {values}"
            )

    return "\n".join(lines)