
import re

from typing import Any


# ============================================================
# CONFIGURATION
# ============================================================

MAX_RELATED_PER_TYPE = 8

MIN_RELATIONSHIP_SCORE = 0.30

DIRECT_MATCH_BONUS = 0.25

TITLE_MATCH_WEIGHT = 0.35

SEMANTIC_WEIGHT = 0.45

KEYWORD_WEIGHT = 0.20


# ============================================================
# NORMALIZATION
# ============================================================

def normalize_text(text: Any) -> str:
    """
    Normalize text for deterministic matching.
    """

    if text is None:
        return ""

    text = str(text).lower()

    text = text.replace("-", " ")
    text = text.replace("/", " ")
    text = text.replace("_", " ")

    text = re.sub(
        r"[^a-z0-9\s]",
        " ",
        text,
    )

    text = re.sub(
        r"\s+",
        " ",
        text,
    )

    return text.strip()


# ============================================================
# TOKENIZATION
# ============================================================

STOPWORDS = {

    "the",

    "a",

    "an",

    "and",

    "or",

    "of",

    "for",

    "to",

    "in",

    "on",

    "with",

    "by",

    "from",

    "used",

    "use",

    "requirement",

    "requirements",

    "specification",

    "specifications",

    "standard",

    "standards",

    "testing",

    "test",

    "tests",

    "method",

    "methods",

    "quality",
}


def tokenize(text: Any) -> set[str]:
    """
    Convert text into meaningful normalized tokens.
    """

    normalized = normalize_text(
        text
    )

    if not normalized:
        return set()

    return {
        token

        for token in normalized.split()

        if token not in STOPWORDS

        and len(token) > 1
    }


# ============================================================
# CANONICALIZATION
# ============================================================

SYNONYMS = {

    "automobile": "automotive",

    "automobiles": "automotive",

    "motor": "automotive",

    "motorized": "automotive",

    "motorised": "automotive",

    "automotive": "automotive",

    "tyre": "tire",

    "tyres": "tire",

    "tire": "tire",

    "tires": "tire",

    "transformers": "transformer",

    "transformer": "transformer",

    "photovoltaic": "pv",

    "pv": "pv",

    "cables": "cable",

    "cable": "cable",

    "wires": "wire",

    "wire": "wire",

    "pumps": "pump",

    "pump": "pump",

    "bars": "bar",

    "bar": "bar",

    "reinforcing": "reinforcement",

    "reinforced": "reinforcement",

    "reinforcement": "reinforcement",

    "concrete": "cement",

    "cement": "cement",

    "modules": "module",

    "module": "module",
}


def canonicalize_token(
    token: str,
) -> str:

    return SYNONYMS.get(
        token,
        token,
    )


def canonicalize_tokens(
    tokens: set[str],
) -> set[str]:

    return {
        canonicalize_token(
            token
        )

        for token in tokens
    }


# ============================================================
# QUERY KEYWORDS
# ============================================================

def extract_query_tokens(
    query: str,
) -> set[str]:

    return canonicalize_tokens(
        tokenize(query)
    )


# ============================================================
# RELATED STANDARD TEXT
# ============================================================

def build_related_text(
    related_standard: dict,
) -> str:
    """
    Build searchable text from a BIS relationship entry.
    """

    standard_number = (
        related_standard.get(
            "standard_number"
        )
        or ""
    )

    standard_name = (
        related_standard.get(
            "standard_name"
        )
        or ""
    )

    identical_is = (
        related_standard.get(
            "identical_is"
        )
        or ""
    )

    equivalent_is = (
        related_standard.get(
            "equivalent_is"
        )
        or ""
    )

    return " ".join(
        [
            str(standard_number),
            str(standard_name),
            str(identical_is),
            str(equivalent_is),
        ]
    )


# ============================================================
# TITLE SCORE
# ============================================================

def title_match_score(
    query: str,
    standard_name: str,
) -> float:
    """
    Calculate lexical overlap between the query
    and related standard title.
    """

    query_tokens = (
        extract_query_tokens(
            query
        )
    )

    title_tokens = (
        canonicalize_tokens(
            tokenize(
                standard_name
            )
        )
    )

    if not query_tokens:
        return 0.0

    if not title_tokens:
        return 0.0

    overlap = (
        query_tokens
        & title_tokens
    )

    return (
        len(overlap)
        / len(query_tokens)
    )


# ============================================================
# KEYWORD SCORE
# ============================================================

def keyword_match_score(
    query: str,
    standard_text: str,
) -> float:
    """
    Calculate token-level overlap between
    query and related standard.
    """

    query_tokens = (
        extract_query_tokens(
            query
        )
    )

    standard_tokens = (
        canonicalize_tokens(
            tokenize(
                standard_text
            )
        )
    )

    if not query_tokens:
        return 0.0

    if not standard_tokens:
        return 0.0

    overlap = (
        query_tokens
        & standard_tokens
    )

    return (
        len(overlap)
        / len(query_tokens)
    )


# ============================================================
# PRODUCT DETECTION
# ============================================================

PRIMARY_PRODUCTS = {

    "transformer": {

        "transformer",

        "transformers",
    },

    "tire": {

        "tire",

        "tyre",

        "tires",

        "tyres",
    },

    "reinforcement": {

        "reinforcement",

        "reinforcing",

        "reinforced",

        "bar",

        "bars",
    },

    "concrete": {

        "concrete",

        "cement",
    },

    "water": {

        "water",

        "drinking",
    },

    "solar": {

        "solar",

        "photovoltaic",

        "pv",
    },

    "oxygen": {

        "oxygen",
    },

    "cable": {

        "cable",

        "cables",
    },

    "pump": {

        "pump",

        "pumps",
    },
}

# ============================================================
# PRODUCT FAMILY DETECTION
# ============================================================

PRODUCT_FAMILY_TERMS = {

    "reinforcement": {
        "reinforcement",
        "reinforcing",
        "steel reinforcement",
        "reinforcement bar",
        "reinforcement bars",
        "steel bar",
        "steel bars",
        "rebar",
        "rebars",
        "deformed bar",
        "deformed bars",
    },

    "transformer": {
        "transformer",
        "transformers",
    },

    "tire": {
        "tire",
        "tyre",
        "tires",
        "tyres",
    },

    "cable": {
        "cable",
        "cables",
    },

    "pump": {
        "pump",
        "pumps",
    },

    "water": {
        "water",
        "drinking water",
        "packaged water",
        "mineral water",
    },

    "solar": {
        "solar",
        "photovoltaic",
        "pv",
        "solar module",
        "solar modules",
    },

    "concrete": {
        "concrete",
        "cement",
    },
}


def detect_product_families(
    text: str,
) -> set[str]:

    normalized = normalize_text(text)

    detected = set()

    for (
        family,
        terms
    ) in PRODUCT_FAMILY_TERMS.items():

        for term in terms:

            if normalize_text(term) in normalized:

                detected.add(family)

                break

    return detected

# ============================================================
# FUNCTION DETECTION
# ============================================================

FUNCTION_TERMS = {

    "welding": {
        "welding",
        "weld",
        "welded",
    },

    "coupling": {
        "coupler",
        "couplers",
        "coupling",
        "mechanical splice",
        "mechanical splices",
    },

    "bending_fixing": {
        "bending",
        "bending and fixing",
        "fixing of bars",
    },

    "coating": {
        "galvanized",
        "galvanizing",
        "zinc coating",
        "zinc coated",
        "hot dip zinc",
        "hot dip galvanized",
    },

    "testing": {
        "testing",
        "test method",
        "test methods",
    },

    "design": {
        "design",
        "design criteria",
        "design of",
    },

    "construction": {
        "construction",
        "construction practice",
        "code of practice",
    },
}


def detect_functions(
    text: str,
) -> set[str]:

    normalized = normalize_text(text)

    detected = set()

    for (
        function,
        terms
    ) in FUNCTION_TERMS.items():

        for term in terms:

            if normalize_text(term) in normalized:

                detected.add(function)

                break

    return detected
def detect_primary_products(
    text: str,
) -> set[str]:
    """
    Detect broad product categories.
    """

    normalized = normalize_text(
        text
    )

    detected = set()

    for (
        product,
        aliases
    ) in PRIMARY_PRODUCTS.items():

        for alias in aliases:

            alias_normalized = (
                normalize_text(
                    alias
                )
            )

            # Token-aware matching prevents
            # accidental substring matches.
            alias_tokens = set(
                alias_normalized.split()
            )

            normalized_tokens = set(
                normalized.split()
            )

            if alias_tokens <= normalized_tokens:

                detected.add(
                    product
                )

                break

    return detected


# ============================================================
# PRODUCT MATCH
# ============================================================

def product_match_score(
    query: str,
    standard_text: str,
) -> float:
    """
    Measure whether the related standard belongs
    to the same broad product domain.
    """

    query_products = (
        detect_primary_products(
            query
        )
    )

    standard_products = (
        detect_primary_products(
            standard_text
        )
    )

    if not query_products:
        return 0.0

    if not standard_products:
        return 0.0

    overlap = (
        query_products
        & standard_products
    )

    if overlap:
        return 1.0

    return 0.0

# ============================================================
# PRODUCT FAMILY COMPATIBILITY
# ============================================================

def product_family_compatibility(
    query: str,
    standard_text: str,
) -> float:

    query_families = detect_product_families(
        query
    )

    standard_families = detect_product_families(
        standard_text
    )

    if not query_families:
        return 0.5

    if not standard_families:
        return 0.25

    overlap = (
        query_families
        & standard_families
    )

    if overlap:
        return 1.0

    return 0.0


# ============================================================
# PRODUCT FAMILY MISMATCH PENALTY
# ============================================================

PRODUCT_FAMILY_MISMATCH_PENALTY = 0.18


def product_family_mismatch_penalty(
    query: str,
    standard_text: str,
) -> float:

    compatibility = (
        product_family_compatibility(
            query=query,
            standard_text=standard_text,
        )
    )

    if compatibility == 0.0:
        return PRODUCT_FAMILY_MISMATCH_PENALTY

    return 0.0
# ============================================================
# SPECIALIZED PRODUCT DETECTION
# ============================================================

SPECIALIZED_TERMS = {

    "galvanized": {

        "galvanized",

        "zinc coated",

        "zinc coating",

        "hot dip galvanized",

        "hot dip",
    },

    "stainless": {

        "stainless",

        "stainless steel",
    },

    "coupler": {

        "coupler",

        "couplers",

        "mechanical splice",

        "mechanical splices",
    },

    "repair": {

        "repair",

        "repairs",

        "repairing",
    },

    "retread": {

        "retread",

        "retreaded",

        "retreading",
    },

    "pneumatic": {

        "pneumatic",
    },

    "outdoor": {

        "outdoor",
    },

    "indoor": {

        "indoor",
    },
}


def detect_specialized_terms(
    text: str,
) -> set[str]:
    """
    Detect specialization attributes.
    """

    normalized = normalize_text(
        text
    )

    detected = set()

    for (
        category,
        terms
    ) in SPECIALIZED_TERMS.items():

        for term in terms:

            normalized_term = (
                normalize_text(
                    term
                )
            )

            if normalized_term in normalized:

                detected.add(
                    category
                )

                break

    return detected


# ============================================================
# SPECIFICITY PENALTY
# ============================================================

def specificity_penalty(
    query: str,
    standard_text: str,
) -> float:
    """
    Penalize a related standard when it is significantly
    more specialized than the user's query.
    """

    query_specializations = (
        detect_specialized_terms(
            query
        )
    )

    standard_specializations = (
        detect_specialized_terms(
            standard_text
        )
    )

    if not standard_specializations:
        return 0.0

    # Query explicitly asks for the specialization.
    if query_specializations:

        if (
            query_specializations
            & standard_specializations
        ):

            return 0.0

    # Generic query but highly specialized result.
    return min(
        0.10,
        0.03
        * len(
            standard_specializations
        ),
    )


# ============================================================
# SEMANTIC SCORE
# ============================================================

def semantic_similarity(
    query_embedding,
    standard_embedding,
) -> float:
    """
    Calculate cosine similarity for normalized embeddings.

    Since BGE embeddings are normalized, cosine similarity
    is the dot product.

    This function is kept here so the relationship filter
    can use BGE semantic scores when they are supplied.
    """

    if (
        query_embedding is None
        or standard_embedding is None
    ):

        return 0.0

    try:

        score = float(
            query_embedding
            @ standard_embedding
        )

    except Exception:

        return 0.0

    # Convert approximately from [-1, 1]
    # to [0, 1].

    score = (
        score + 1.0
    ) / 2.0

    return max(
        0.0,
        min(
            1.0,
            score,
        ),
    )


# ============================================================
# RELATIONSHIP SCORE
# ============================================================

def calculate_relationship_relevance(
    query: str,
    related_standard: dict,
    semantic_score: float = 0.0,
) -> dict:
    """
    Calculate the relevance of one BIS related standard.

    Signals:
        semantic similarity
        title overlap
        keyword overlap
        product match
        product family compatibility
        shared function
        specialization penalty
    """

    standard_name = (
        related_standard.get(
            "standard_name"
        )
        or ""
    )

    standard_text = build_related_text(
        related_standard
    )

    title_score = (
        title_match_score(
            query,
            standard_name,
        )
    )

    keyword_score = (
        keyword_match_score(
            query,
            standard_text,
        )
    )

    product_score = (
        product_match_score(
            query,
            standard_text,
        )
    )

    family_compatibility = (
        product_family_compatibility(
            query=query,
            standard_text=standard_text,
        )
    )

    family_mismatch_penalty = (
        product_family_mismatch_penalty(
            query=query,
            standard_text=standard_text,
        )
    )

    specificity = (
        specificity_penalty(
            query,
            standard_text,
        )
    )

    # --------------------------------------------------------
    # FUNCTION MATCHING
    # --------------------------------------------------------

    query_functions = detect_functions(
        query
    )

    standard_functions = detect_functions(
        standard_text
    )

    shared_functions = (
        query_functions
        & standard_functions
    )

    # --------------------------------------------------------
    # BASE SCORE
    # --------------------------------------------------------

    score = (
        SEMANTIC_WEIGHT
        * semantic_score
        +
        TITLE_MATCH_WEIGHT
        * title_score
        +
        KEYWORD_WEIGHT
        * keyword_score
    )

    # --------------------------------------------------------
    # SAME PRODUCT FAMILY
    # --------------------------------------------------------

    if product_score == 1.0:
        score += DIRECT_MATCH_BONUS

    if family_compatibility == 1.0:
        score += 0.10

    elif family_compatibility == 0.0:
        score -= family_mismatch_penalty

    # --------------------------------------------------------
    # SHARED FUNCTION
    # --------------------------------------------------------

    if (
        query_functions
        and shared_functions
    ):
        score += 0.05

    # --------------------------------------------------------
    # SPECIALIZATION PENALTY
    # --------------------------------------------------------

    score -= specificity

    # --------------------------------------------------------
    # FINAL SCORE
    # --------------------------------------------------------

    score = max(
        0.0,
        min(1.0, score),
    )

    return {
        "score": score,

        "semantic_score": (
            semantic_score
        ),

        "title_score": (
            title_score
        ),

        "keyword_score": (
            keyword_score
        ),

        "product_score": (
            product_score
        ),

        "product_family_compatibility": (
            family_compatibility
        ),

        "product_family_mismatch_penalty": (
            family_mismatch_penalty
        ),

        "query_functions": (
            sorted(query_functions)
        ),

        "standard_functions": (
            sorted(standard_functions)
        ),

        "shared_functions": (
            sorted(shared_functions)
        ),

        "specificity_penalty": (
            specificity
        ),
    }


# ============================================================
# FILTER RELATIONSHIP LIST
# ============================================================

def filter_relationships(
    query: str,
    relationship_type: str,
    relationships: list[dict],
    semantic_scores: dict[str, float] | None = None,
    max_results: int = MAX_RELATED_PER_TYPE,
) -> list[dict]:
    """
    Filter and rank one relationship category.

    semantic_scores should map:

        standard_number -> BGE similarity

    when semantic scores are available.
    """

    if not relationships:

        return []

    semantic_scores = (
        semantic_scores
        or {}
    )

    ranked = []

    for related_standard in relationships:

        if not isinstance(
            related_standard,
            dict,
        ):

            continue

        standard_number = str(
            related_standard.get(
                "standard_number"
            )
            or ""
        )

        semantic_score = (
            semantic_scores.get(
                standard_number,
                0.0,
            )
        )

        relevance = (
            calculate_relationship_relevance(

                query=query,

                related_standard=(
                    related_standard
                ),

                semantic_score=(
                    semantic_score
                ),
            )
        )

        score = relevance[
            "score"
        ]

        if (
            score
            < MIN_RELATIONSHIP_SCORE
        ):

            continue

        result = dict(
            related_standard
        )

        result[
            "relationship_type"
        ] = relationship_type

        result[
            "relationship_score"
        ] = score

        result[
            "relationship_features"
        ] = relevance

        ranked.append(
            result
        )

    ranked.sort(

        key=lambda item:
            item[
                "relationship_score"
            ],

        reverse=True,
    )

    return ranked[
        :max_results
    ]


# ============================================================
# FILTER ALL RELATIONSHIPS
# ============================================================

RELATIONSHIP_LABELS = {

    "related_indian":
        "Related Indian Standards",

    "related_international":
        "Related International Standards",

    "other_related_indian":
        "Other Related Indian Standards",

    "following_related_indian":
        "Following Related Indian Standards",
}


def filter_all_relationships(
    query: str,
    relationships: dict,
    semantic_scores: dict[str, float] | None = None,
    max_results_per_type: int = MAX_RELATED_PER_TYPE,
) -> dict:
    """
    Filter all BIS relationship categories.
    """

    filtered = {}

    for (
        relationship_type,
        values
    ) in relationships.items():

        if (
            relationship_type
            not in RELATIONSHIP_LABELS
        ):

            continue

        if not isinstance(
            values,
            list,
        ):

            continue

        results = filter_relationships(

            query=query,

            relationship_type=(
                relationship_type
            ),

            relationships=values,

            semantic_scores=(
                semantic_scores
            ),

            max_results=(
                max_results_per_type
            ),
        )

        if results:

            filtered[
                relationship_type
            ] = {

                "label":
                    RELATIONSHIP_LABELS[
                        relationship_type
                    ],

                "values":
                    results,
            }

    return filtered


# ============================================================
# BUILD CLEAN CONTEXT
# ============================================================

def build_filtered_relationship_context(
    filtered_relationships: dict,
) -> str:
    """
    Build concise relationship context for RAG/LLM.
    """

    if not filtered_relationships:

        return (
            "No highly relevant BIS relationships "
            "were identified."
        )

    lines = []

    for (
        relationship_type,
        relationship_data
    ) in filtered_relationships.items():

        # Support both:

        # {
        #     "label": "...",
        #     "values": [...]
        # }

        # and direct list format.

        if isinstance(
            relationship_data,
            dict,
        ):

            label = (
                relationship_data.get(
                    "label",
                    RELATIONSHIP_LABELS.get(
                        relationship_type,
                        relationship_type,
                    ),
                )
            )

            standards = (
                relationship_data.get(
                    "values",
                    []
                )
            )

        else:

            label = (
                RELATIONSHIP_LABELS.get(
                    relationship_type,
                    relationship_type,
                )
            )

            standards = (
                relationship_data
            )


        lines.append(
            f"{label}:"
        )


        for standard in standards:

            if not isinstance(
                standard,
                dict,
            ):

                lines.append(
                    f"- {standard}"
                )

                continue

            standard_number = (
                standard.get(
                    "standard_number"
                )
                or "Unknown"
            )

            standard_name = (
                standard.get(
                    "standard_name"
                )
                or "Unknown"
            )

            score = (
                standard.get(
                    "relationship_score",
                    0.0,
                )
            )

            lines.append(

                f"- {standard_number} - "
                f"{standard_name} "
                f"(relevance: {score:.3f})"
            )


    return "\n".join(
        lines
    )

