from embedding.relationship_expansion import expand_relationships
from embedding.relationship_filter import filter_all_relationships

from pathlib import Path
import re

import chromadb
from sentence_transformers import SentenceTransformer, CrossEncoder


# ============================================================
# CONFIG
# ============================================================

EMBEDDING_MODEL_NAME = "BAAI/bge-small-en-v1.5"
RERANKER_MODEL_NAME = "cross-encoder/ms-marco-MiniLM-L-6-v2"

COLLECTION_NAME = "bis_standards"

RETRIEVAL_TOP_K = 30
FINAL_TOP_K = 5


# ============================================================
# HYBRID RANKING WEIGHTS
# ============================================================

CROSS_ENCODER_WEIGHT = 0.30
TITLE_WEIGHT = 0.12
PRODUCT_WEIGHT = 0.12
PHRASE_WEIGHT = 0.08
KEYWORD_WEIGHT = 0.04
TYPE_WEIGHT = 0.08
STATUS_WEIGHT = 0.04
RELATIONSHIP_WEIGHT = 0.07
PUBLICATION_YEAR_WEIGHT = 0.03
STANDARD_NUMBER_WEIGHT = 0.05
APPLICATION_WEIGHT = 0.07


# ============================================================
# SCORE ADJUSTMENTS
# ============================================================

EXACT_PRODUCT_BONUS = 0.10
PRODUCT_FAMILY_BONUS = 0.08
APPLICATION_BONUS = 0.08

PRODUCT_MISMATCH_PENALTY = 0.18
SPECIFICITY_PENALTY = 0.08
APPLICATION_MISMATCH_PENALTY = 0.12

COMPOUND_PRODUCT_BONUS = 0.18
COMPOUND_PRODUCT_MISMATCH_PENALTY = 0.15


# ============================================================
# COMPOUND PRODUCTS
# ============================================================

COMPOUND_PRODUCT_TERMS = {
    "oxygen_cylinder": {
        "oxygen cylinder",
        "oxygen cylinders",
        "medical oxygen cylinder",
        "medical oxygen cylinders",
    },

    "oxygen_concentrator": {
        "oxygen concentrator",
        "oxygen concentrators",
        "oxygen concentration equipment",
    },

    "oxygen_conserving_equipment": {
        "oxygen conserving equipment",
        "oxygen conserving devices",
    },

    "reinforcement_bar": {
        "reinforcement bar",
        "reinforcement bars",
        "steel reinforcement bar",
        "steel reinforcement bars",
        "rebar",
        "rebars",
    },

    "distribution_transformer": {
        "distribution transformer",
        "distribution transformers",
    },

    "solar_module": {
        "solar module",
        "solar modules",
        "photovoltaic module",
        "photovoltaic modules",
    },
}


# ============================================================
# PRODUCT FAMILIES
# ============================================================

PRODUCT_FAMILIES = {

    "concrete": {
        "concrete",
        "cement concrete",
        "plain concrete",
        "reinforced concrete",
        "prestressed concrete",
        "fresh concrete",
        "concrete mix",
        "concrete construction",
    },

    "cement": {
        "cement",
        "ordinary portland cement",
        "portland cement",
        "portland pozzolana cement",
        "portland slag cement",
    },

    "concrete_block": {
        "concrete block",
        "concrete blocks",
        "masonry block",
        "masonry blocks",
        "concrete masonry unit",
        "concrete masonry units",
    },

    "reinforcement": {
        "reinforcement",
        "reinforcement bar",
        "reinforcement bars",
        "steel reinforcement",
        "rebar",
        "rebars",
    },

    "transformer": {
        "transformer",
        "transformers",
        "distribution transformer",
        "distribution transformers",
        "power transformer",
        "power transformers",
    },

    "tire": {
        "tire",
        "tyre",
        "tires",
        "tyres",
        "automobile tyre",
        "automobile tire",
    },

    "water": {
        "water",
        "drinking water",
        "potable water",
    },

    "solar": {
        "solar",
        "photovoltaic",
        "photovoltaic module",
        "solar module",
        "pv module",
    },

    "oxygen": {
        "oxygen",
        "oxygen cylinder",
        "medical oxygen",
        "oxygen equipment",
    },

    "cable": {
        "cable",
        "cables",
        "power cable",
        "electrical cable",
    },

    "pump": {
        "pump",
        "pumps",
        "water pump",
    },
}


# ============================================================
# APPLICATION / FUNCTION TERMS
# ============================================================

APPLICATION_TERMS = {

    "construction": {
        "construction",
        "building",
        "building construction",
        "civil construction",
        "structural",
        "structure",
        "structural work",
        "construction work",
    },

    "concrete_construction": {
        "concrete construction",
        "cement concrete",
        "plain concrete",
        "reinforced concrete",
        "concrete structure",
        "concrete structures",
    },

    "testing": {
        "test",
        "testing",
        "method of test",
        "testing method",
        "laboratory test",
        "determination",
    },

    "manufacturing": {
        "manufacture",
        "manufacturing",
        "production",
        "fabrication",
    },

    "installation": {
        "installation",
        "install",
        "erection",
    },

    "repair": {
        "repair",
        "maintenance",
        "rehabilitation",
    },

    "specification": {
        "specification",
        "requirements",
        "requirement",
        "technical requirements",
        "quality requirements",
    },

    "code_of_practice": {
        "code of practice",
        "practice",
        "guidelines",
        "procedure",
    },
}


# ============================================================
# PRIMARY PRODUCTS
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
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[1]

CHROMA_DIR = BASE_DIR / "chroma_db"


# ============================================================
# MODELS
# ============================================================

print("Loading embedding model...")

embedding_model = SentenceTransformer(
    EMBEDDING_MODEL_NAME
)

print("Loading reranker...")

reranker = CrossEncoder(
    RERANKER_MODEL_NAME
)


# ============================================================
# CHROMA
# ============================================================

client = chromadb.PersistentClient(
    path=str(CHROMA_DIR)
)

collection = client.get_collection(
    name=COLLECTION_NAME
)


# ============================================================
# TEXT UTILITIES
# ============================================================

def normalize_text(text):
    if text is None:
        return ""

    return re.sub(
        r"\s+",
        " ",
        str(text).lower().strip()
    )


def tokenize(text):
    text = normalize_text(text)

    return set(
        re.findall(
            r"[a-z0-9]+",
            text
        )
    )


def canonicalize_token(token):

    token = token.lower().strip()

    irregular = {
        "tyres": "tyre",
        "tires": "tire",
        "cylinders": "cylinder",
        "transformers": "transformer",
        "pumps": "pump",
        "cables": "cable",
        "bars": "bar",
        "modules": "module",
        "blocks": "block",
        "structures": "structure",
        "buildings": "building",
    }

    return irregular.get(
        token,
        token
    )


def canonicalize_tokens(tokens):

    return {
        canonicalize_token(token)
        for token in tokens
    }


# ============================================================
# INTENT
# ============================================================

def detect_intent(query):

    q = normalize_text(query)

    if any(
        term in q
        for term in [
            "test",
            "testing",
            "method of test",
            "testing method",
            "determination",
        ]
    ):
        return "TESTING"

    if any(
        term in q
        for term in [
            "repair",
            "maintenance",
            "rehabilitation",
        ]
    ):
        return "REPAIR"

    if any(
        term in q
        for term in [
            "install",
            "installation",
            "erection",
        ]
    ):
        return "INSTALLATION"

    if any(
        term in q
        for term in [
            "manufacture",
            "manufacturing",
            "production",
        ]
    ):
        return "MANUFACTURING"

    if any(
        term in q
        for term in [
            "requirement",
            "requirements",
            "specification",
            "specifications",
        ]
    ):
        return "SPECIFICATION"

    if any(
        term in q
        for term in [
            "code of practice",
            "construction",
            "construction work",
            "building construction",
        ]
    ):
        return "CONSTRUCTION"

    return "PRODUCT"


# ============================================================
# PRODUCT FAMILY DETECTION
# ============================================================

def detect_product_families(query):

    q = normalize_text(query)

    detected = set()

    for family, terms in PRODUCT_FAMILIES.items():

        for term in terms:

            if term in q:
                detected.add(family)
                break

    return detected


def detect_compound_products(query):

    q = normalize_text(query)

    detected = set()

    for product, terms in COMPOUND_PRODUCT_TERMS.items():

        for term in terms:

            if term in q:
                detected.add(product)
                break

    return detected


# ============================================================
# APPLICATION DETECTION
# ============================================================

def detect_applications(query):

    q = normalize_text(query)

    detected = set()

    for application, terms in APPLICATION_TERMS.items():

        for term in terms:

            if term in q:
                detected.add(application)
                break

    return detected


# ============================================================
# PRIMARY PRODUCT DETECTION
# ============================================================

def detect_primary_products(query):

    tokens = canonicalize_tokens(
        tokenize(query)
    )

    detected = set()

    for product, terms in PRIMARY_PRODUCTS.items():

        canonical_terms = {
            canonicalize_token(term)
            for term in terms
        }

        if tokens & canonical_terms:
            detected.add(product)

    return detected


# ============================================================
# PRODUCT MATCH
# ============================================================

def product_match_score(query, text):

    query_products = detect_primary_products(
        query
    )

    if not query_products:
        return 0.0

    text_products = detect_primary_products(
        text
    )

    if not text_products:
        return 0.0

    overlap = (
        query_products
        & text_products
    )

    return min(
        1.0,
        len(overlap)
        / max(1, len(query_products))
    )


def product_family_score(query, text):

    query_families = detect_product_families(
        query
    )

    if not query_families:
        return 0.0

    text_families = detect_product_families(
        text
    )

    if not text_families:
        return 0.0

    overlap = (
        query_families
        & text_families
    )

    return min(
        1.0,
        len(overlap)
        / max(1, len(query_families))
    )


# ============================================================
# COMPOUND PRODUCT MATCH
# ============================================================

def compound_product_match_score(
    query,
    text
):

    query_products = detect_compound_products(
        query
    )

    if not query_products:
        return 0.0

    text_products = detect_compound_products(
        text
    )

    if not text_products:
        return 0.0

    overlap = (
        query_products
        & text_products
    )

    if not overlap:
        return 0.0

    return min(
        1.0,
        len(overlap)
        / max(1, len(query_products))
    )


def compound_product_mismatch_score(
    query,
    text
):

    query_products = detect_compound_products(
        query
    )

    if not query_products:
        return 0.0

    text_products = detect_compound_products(
        text
    )

    if not text_products:
        return 0.0

    if query_products & text_products:
        return 0.0

    return 1.0


# ============================================================
# APPLICATION SCORE
# ============================================================

def application_score(query, text):

    query_apps = detect_applications(
        query
    )

    if not query_apps:
        return 0.0

    text_apps = detect_applications(
        text
    )

    if not text_apps:
        return 0.0

    overlap = (
        query_apps
        & text_apps
    )

    return min(
        1.0,
        len(overlap)
        / max(1, len(query_apps))
    )


# ============================================================
# TITLE SCORE
# ============================================================

def extract_title_tokens(metadata):

    title = metadata.get(
        "standard_name",
        ""
    )

    return canonicalize_tokens(
        tokenize(title)
    )


def title_match_score(
    query,
    metadata
):

    query_tokens = canonicalize_tokens(
        tokenize(query)
    )

    title_tokens = extract_title_tokens(
        metadata
    )

    if not query_tokens:
        return 0.0

    if not title_tokens:
        return 0.0

    overlap = (
        query_tokens
        & title_tokens
    )

    return min(
        1.0,
        len(overlap)
        / max(1, len(query_tokens))
    )


# ============================================================
# PHRASE SCORE
# ============================================================

def phrase_match_score(
    query,
    text
):

    q = normalize_text(query)
    t = normalize_text(text)

    if not q or not t:
        return 0.0

    if q in t:
        return 1.0

    query_words = q.split()

    if len(query_words) < 2:
        return 0.0

    matched = 0

    for i in range(
        len(query_words) - 1
    ):

        phrase = (
            query_words[i]
            + " "
            + query_words[i + 1]
        )

        if phrase in t:
            matched += 1

    return min(
        1.0,
        matched
        / max(1, len(query_words) - 1)
    )


# ============================================================
# KEYWORD SCORE
# ============================================================

def keyword_match_score(
    query,
    text
):

    query_tokens = canonicalize_tokens(
        tokenize(query)
    )

    text_tokens = canonicalize_tokens(
        tokenize(text)
    )

    if not query_tokens:
        return 0.0

    overlap = (
        query_tokens
        & text_tokens
    )

    return min(
        1.0,
        len(overlap)
        / max(1, len(query_tokens))
    )


# ============================================================
# STANDARD TYPE SCORE
# ============================================================

def type_relevance_score(
    query,
    metadata
):

    intent = detect_intent(query)

    standard_type = normalize_text(
        metadata.get(
            "standard_type",
            ""
        )
    )

    title = normalize_text(
        metadata.get(
            "standard_name",
            ""
        )
    )

    if not standard_type and not title:
        return 0.0

    # --------------------------------------------------------
    # TESTING
    # --------------------------------------------------------

    if intent == "TESTING":

        if (
            "test" in standard_type
            or "test" in title
            or "testing" in title
            or "method" in title
        ):
            return 1.0

        return 0.0

    # --------------------------------------------------------
    # CONSTRUCTION
    # --------------------------------------------------------

    if intent == "CONSTRUCTION":

        if (
            "code of practice"
            in standard_type
            or "code of practice"
            in title
        ):
            return 1.0

        if (
            "specification"
            in standard_type
            or "specification"
            in title
        ):
            return 0.85

        if (
            "glossary" in title
            or "terminology" in title
        ):
            return 0.25

        return 0.4

    # --------------------------------------------------------
    # SPECIFICATION
    # --------------------------------------------------------

    if intent == "SPECIFICATION":

        if "specification" in standard_type:
            return 1.0

        if "specification" in title:
            return 1.0

        if "code of practice" in title:
            return 0.7

        if (
            "glossary" in title
            or "terminology" in title
        ):
            return 0.2

        return 0.4

    # --------------------------------------------------------
    # REPAIR
    # --------------------------------------------------------

    if intent == "REPAIR":

        if "repair" in title:
            return 1.0

        if "maintenance" in title:
            return 0.9

        return 0.3

    # --------------------------------------------------------
    # INSTALLATION
    # --------------------------------------------------------

    if intent == "INSTALLATION":

        if "installation" in title:
            return 1.0

        if "erection" in title:
            return 0.9

        return 0.3

    # --------------------------------------------------------
    # MANUFACTURING
    # --------------------------------------------------------

    if intent == "MANUFACTURING":

        if (
            "manufacture" in title
            or "manufacturing" in title
        ):
            return 1.0

        return 0.3

    return 0.5


# ============================================================
# STATUS SCORE
# ============================================================

def status_score(metadata):

    if metadata.get(
        "is_active"
    ) is True:

        return 1.0

    status = normalize_text(
        metadata.get(
            "status_label",
            ""
        )
    )

    if "active" in status:
        return 1.0

    if "withdraw" in status:
        return 0.0

    return 0.5


# ============================================================
# YEAR
# ============================================================

def extract_year(query):

    match = re.search(
        r"\b(19|20)\d{2}\b",
        query
    )

    if not match:
        return None

    return int(
        match.group(0)
    )


def publication_year_score(
    query,
    metadata
):

    query_year = extract_year(
        query
    )

    if query_year is None:
        return 0.5

    published_on = str(
        metadata.get(
            "published_on",
            ""
        )
    )

    match = re.search(
        r"\b(19|20)\d{2}\b",
        published_on
    )

    if not match:
        return 0.0

    standard_year = int(
        match.group(0)
    )

    return (
        1.0
        if standard_year == query_year
        else 0.0
    )


# ============================================================
# STANDARD NUMBER MATCH
# ============================================================

def standard_number_match_score(
    query,
    metadata
):

    q = normalize_text(
        query
    )

    standard_number = normalize_text(
        metadata.get(
            "standard_number",
            ""
        )
    )

    if not standard_number:
        return 0.0

    normalized_standard = re.sub(
        r"\s+",
        "",
        standard_number
    )

    normalized_query = re.sub(
        r"\s+",
        "",
        q
    )

    if normalized_standard in normalized_query:
        return 1.0

    return 0.0


# ============================================================
# RELATIONSHIP SCORE
# ============================================================

def relationship_score(
    metadata
):

    relationships = metadata.get(
        "related",
        {}
    )

    if not relationships:
        return 0.0

    score = 0.0

    if isinstance(
        relationships,
        dict
    ):

        if relationships.get(
            "related_indian"
        ):
            score += 0.35

        if relationships.get(
            "following_related_indian"
        ):
            score += 0.30

        if relationships.get(
            "related_international"
        ):
            score += 0.15

        if relationships.get(
            "amendments"
        ):
            score += 0.10

        if relationships.get(
            "corrigenda"
        ):
            score += 0.05

        if relationships.get(
            "product_manuals"
        ):
            score += 0.05

    return min(
        1.0,
        score
    )


# ============================================================
# SPECIFICITY PENALTY
# ============================================================

def calculate_specificity_penalty(
    query,
    metadata
):

    q = normalize_text(
        query
    )

    title = normalize_text(
        metadata.get(
            "standard_name",
            ""
        )
    )

    query_words = set(
        q.split()
    )

    application_specific_terms = {
        "floor",
        "roof",
        "wall",
        "masonry",
        "block",
        "lintel",
        "sill",
        "paving",
        "soil",
        "filler",
        "tile",
        "tiles",
    }

    specific_terms = (
        application_specific_terms
        & set(title.split())
    )

    if not specific_terms:
        return 0.0

    if len(query_words) <= 5:

        return min(
            1.0,
            len(specific_terms)
            * 0.20
        )

    return 0.0


# ============================================================
# PRIMARY PRODUCT MISMATCH
# ============================================================

def calculate_primary_product_mismatch(
    query,
    metadata
):

    query_products = detect_primary_products(
        query
    )

    if not query_products:
        return 0.0

    title = metadata.get(
        "standard_name",
        ""
    )

    text = " ".join(
        [
            str(title),
            str(
                metadata.get(
                    "short_title",
                    ""
                )
            ),
            str(
                metadata.get(
                    "search_text",
                    ""
                )
            ),
        ]
    )

    text_products = detect_primary_products(
        text
    )

    if not text_products:
        return 0.0

    if query_products & text_products:
        return 0.0

    return 1.0


# ============================================================
# APPLICATION MISMATCH
# ============================================================

def calculate_application_mismatch(
    query,
    metadata
):

    query_apps = detect_applications(
        query
    )

    if not query_apps:
        return 0.0

    title = normalize_text(
        metadata.get(
            "standard_name",
            ""
        )
    )

    if "construction" in query_apps:

        unrelated_terms = {
            "soil",
            "pen-injector",
            "medical",
            "oxygen",
            "automobile",
            "tyre",
            "tire",
            "electrical",
            "gas cylinder",
        }

        if any(
            term in title
            for term in unrelated_terms
        ):
            return 1.0

    return 0.0


# ============================================================
# CONSTRUCTION RELEVANCE
# ============================================================

def construction_relevance(
    query,
    metadata
):

    q = normalize_text(
        query
    )

    if (
        "construction" not in q
        and "building" not in q
        and "structural" not in q
    ):
        return 0.0

    title = normalize_text(
        metadata.get(
            "standard_name",
            ""
        )
    )

    standard_type = normalize_text(
        metadata.get(
            "standard_type",
            ""
        )
    )

    score = 0.0

    if (
        "code of practice" in title
        or "code of practice"
        in standard_type
    ):
        score += 0.7

    if (
        "construction" in title
        or "building" in title
        or "concrete" in title
        or "structural" in title
    ):
        score += 0.3

    return min(
        1.0,
        score
    )


# ============================================================
# SCORE NORMALIZATION
# ============================================================

def normalize_scores(
    values
):

    if not values:
        return []

    minimum = min(
        values
    )

    maximum = max(
        values
    )

    if maximum == minimum:

        return [
            0.5
            for _ in values
        ]

    return [
        (
            value - minimum
        )
        /
        (
            maximum - minimum
        )
        for value in values
    ]


# ============================================================
# HYBRID SCORE
# ============================================================

def calculate_hybrid_score(
    *,
    cross_encoder_score,
    title_score,
    product_score,
    phrase_score,
    keyword_score,
    type_score,
    status_score,
    relationship_score_value,
    publication_year_score_value,
    standard_number_score,
    application_score_value,
):

    return (

        CROSS_ENCODER_WEIGHT
        * cross_encoder_score

        + TITLE_WEIGHT
        * title_score

        + PRODUCT_WEIGHT
        * product_score

        + PHRASE_WEIGHT
        * phrase_score

        + KEYWORD_WEIGHT
        * keyword_score

        + TYPE_WEIGHT
        * type_score

        + STATUS_WEIGHT
        * status_score

        + RELATIONSHIP_WEIGHT
        * relationship_score_value

        + PUBLICATION_YEAR_WEIGHT
        * publication_year_score_value

        + STANDARD_NUMBER_WEIGHT
        * standard_number_score

        + APPLICATION_WEIGHT
        * application_score_value
    )


# ============================================================
# MAIN SEARCH
# ============================================================

def search_bis(
    query,
    retrieval_top_k=RETRIEVAL_TOP_K,
    final_top_k=FINAL_TOP_K
):

    query = query.strip()

    if not query:
        return []

    intent = detect_intent(
        query
    )

    query_compounds = detect_compound_products(
        query
    )

    # ========================================================
    # BGE RETRIEVAL
    # ========================================================

    query_embedding = embedding_model.encode(
        query,
        normalize_embeddings=True
    ).tolist()

    retrieval = collection.query(
        query_embeddings=[
            query_embedding
        ],
        n_results=retrieval_top_k,
        include=[
            "documents",
            "metadatas",
            "distances",
        ],
    )

    documents = retrieval.get(
        "documents",
        [[]]
    )[0]

    metadatas = retrieval.get(
        "metadatas",
        [[]]
    )[0]

    distances = retrieval.get(
        "distances",
        [[]]
    )[0]

    if not documents:
        return []

    # ========================================================
    # CROSS ENCODER
    # ========================================================

    pairs = [
        (
            query,
            document
        )
        for document in documents
    ]

    raw_cross_scores = reranker.predict(
        pairs
    )

    normalized_cross_scores = normalize_scores(
        [
            float(score)
            for score in raw_cross_scores
        ]
    )

    ranked_results = []

    # ========================================================
    # SCORE CANDIDATES
    # ========================================================

    for (
        document,
        metadata,
        distance,
        raw_ce,
        ce_score
    ) in zip(
        documents,
        metadatas,
        distances,
        raw_cross_scores,
        normalized_cross_scores,
    ):

        standard_name = metadata.get(
            "standard_name",
            ""
        )

        standard_number = metadata.get(
            "standard_number",
            ""
        )

        standard_type = metadata.get(
            "standard_type",
            ""
        )

        title_score = title_match_score(
            query,
            metadata
        )

        product_score = product_match_score(
            query,
            document
        )

        phrase_score = phrase_match_score(
            query,
            document
        )

        keyword_score = keyword_match_score(
            query,
            document
        )

        type_score = type_relevance_score(
            query,
            metadata
        )

        status_value = status_score(
            metadata
        )

        relationship_value = relationship_score(
            metadata
        )

        year_score = publication_year_score(
            query,
            metadata
        )

        standard_number_score = (
            standard_number_match_score(
                query,
                metadata
            )
        )

        application_value = application_score(
            query,
            document
        )

        family_score = product_family_score(
            query,
            document
        )

        compound_score = (
            compound_product_match_score(
                query,
                document
            )
        )

        compound_mismatch = (
            compound_product_mismatch_score(
                query,
                document
            )
        )

        specificity_penalty = (
            calculate_specificity_penalty(
                query,
                metadata
            )
        )

        primary_product_mismatch = (
            calculate_primary_product_mismatch(
                query,
                metadata
            )
        )

        application_mismatch = (
            calculate_application_mismatch(
                query,
                metadata
            )
        )

        construction_score = (
            construction_relevance(
                query,
                metadata
            )
        )

        # ====================================================
        # BASE HYBRID SCORE
        # ====================================================

        hybrid_score = calculate_hybrid_score(
            cross_encoder_score=ce_score,
            title_score=title_score,
            product_score=product_score,
            phrase_score=phrase_score,
            keyword_score=keyword_score,
            type_score=type_score,
            status_score=status_value,
            relationship_score_value=relationship_value,
            publication_year_score_value=year_score,
            standard_number_score=standard_number_score,
            application_score_value=application_value,
        )

        # ====================================================
        # PRODUCT FAMILY
        # ====================================================

        if family_score >= 1.0:

            hybrid_score += (
                PRODUCT_FAMILY_BONUS
            )

        # ====================================================
        # EXACT PRODUCT
        # ====================================================

        if product_score >= 1.0:

            hybrid_score += (
                EXACT_PRODUCT_BONUS
            )

        # ====================================================
        # COMPOUND PRODUCT
        # ====================================================

        if compound_score >= 1.0:

            hybrid_score += (
                COMPOUND_PRODUCT_BONUS
            )

        elif (
            query_compounds
            and compound_mismatch > 0
        ):

            hybrid_score -= (
                COMPOUND_PRODUCT_MISMATCH_PENALTY
            )

        # ====================================================
        # APPLICATION
        # ====================================================

        if application_value > 0:

            hybrid_score += (
                APPLICATION_BONUS
                * application_value
            )

        # ====================================================
        # CONSTRUCTION
        # ====================================================

        if construction_score > 0:

            hybrid_score += (
                0.08
                * construction_score
            )

        # ====================================================
        # PRODUCT MISMATCH
        # ====================================================

        if primary_product_mismatch > 0:

            hybrid_score -= (
                PRODUCT_MISMATCH_PENALTY
            )

        # ====================================================
        # APPLICATION MISMATCH
        # ====================================================

        if application_mismatch > 0:

            hybrid_score -= (
                APPLICATION_MISMATCH_PENALTY
            )

        # ====================================================
        # SPECIFICITY
        # ====================================================

        hybrid_score -= (
            SPECIFICITY_PENALTY
            * specificity_penalty
        )

        # ====================================================
        # EXACT STANDARD NUMBER
        # ====================================================

        if standard_number_score >= 1.0:

            hybrid_score += 0.30

        # ====================================================
        # TESTING INTENT
        # ====================================================

        if intent == "TESTING":

            title = normalize_text(
                standard_name
            )

            if (
                "test" in title
                or "method" in title
            ):

                hybrid_score += 0.10

        # ====================================================
        # SPECIFICATION INTENT
        # ====================================================

        if intent == "SPECIFICATION":

            title = normalize_text(
                standard_name
            )

            if "specification" in title:

                hybrid_score += 0.10

            if "glossary" in title:

                hybrid_score -= 0.12

        # ====================================================
        # CONSTRUCTION INTENT
        # ====================================================

        if intent == "CONSTRUCTION":

            title = normalize_text(
                standard_name
            )

            if "code of practice" in title:

                hybrid_score += 0.12

            if "glossary" in title:

                hybrid_score -= 0.10

            if "terminology" in title:

                hybrid_score -= 0.10

        # ====================================================
        # STATUS
        # ====================================================

        if status_value <= 0.0:

            hybrid_score -= 0.15

        # ====================================================
        # STORE RESULT
        # ====================================================

        ranked_results.append(
            {
                "id":
                    metadata.get(
                        "standard_id"
                    ),

                "standard_number":
                    standard_number,

                "standard_name":
                    standard_name,

                "standard_type":
                    standard_type,

                "metadata":
                    metadata,

                "document":
                    document,

                "bge_distance":
                    float(distance),

                "cross_encoder_raw":
                    float(raw_ce),

                "cross_encoder_score":
                    float(ce_score),

                "title_score":
                    float(title_score),

                "keyword_score":
                    float(keyword_score),

                "product_score":
                    float(product_score),

                "phrase_score":
                    float(phrase_score),

                "type_score":
                    float(type_score),

                "status_score":
                    float(status_value),

                "relationship_score":
                    float(relationship_value),

                "publication_year_score":
                    float(year_score),

                "standard_number_score":
                    float(
                        standard_number_score
                    ),

                "application_score":
                    float(application_value),

                "product_family_score":
                    float(family_score),

                "construction_score":
                    float(construction_score),

                "specificity_penalty":
                    float(
                        specificity_penalty
                    ),

                "primary_product_mismatch":
                    float(
                        primary_product_mismatch
                    ),

                "application_mismatch":
                    float(
                        application_mismatch
                    ),

                "compound_product_score":
                    float(
                        compound_score
                    ),

                "compound_product_mismatch":
                    float(
                        compound_mismatch
                    ),

                "hybrid_score":
                    float(
                        hybrid_score
                    ),
            }
        )

    # ========================================================
    # SORT
    # ========================================================

    ranked_results.sort(
        key=lambda item: item[
            "hybrid_score"
        ],
        reverse=True
    )

    # ========================================================
    # RELATIONSHIP EXPANSION
    # ========================================================

    ranked_results = expand_relationships(
        ranked_results
    )

    # ========================================================
    # RELATIONSHIP FILTERING
    #
    # IMPORTANT:
    # filter_all_relationships() in your existing
    # relationship_filter.py expects:
    #
    #     result, relationships
    #
    # It does NOT accept the complete result list.
    # ========================================================

    for result in ranked_results:

        relationships = result.get(
            "relationships",
            {}
        )

        result[
            "filtered_relationships"
        ] = filter_all_relationships(
            result,
            relationships
        )

    # ========================================================
    # NORMALIZE FILTERED RELATIONSHIPS
    # ========================================================

    for result in ranked_results:

        filtered = result.get(
            "filtered_relationships",
            {}
        )

        normalized_filtered = {}

        for (
            relationship_type,
            data
        ) in filtered.items():

            if isinstance(
                data,
                dict
            ):

                values = data.get(
                    "values",
                    []
                )

            else:

                values = data

            if values is None:

                values = []

            if not isinstance(
                values,
                list
            ):

                values = [
                    values
                ]

            normalized_filtered[
                relationship_type
            ] = values

        result[
            "filtered_relationships"
        ] = normalized_filtered

    # ========================================================
    # FINAL TOP K
    # ========================================================

    return ranked_results[
        :final_top_k
    ]


# ============================================================
# DEBUG PRINTER
# ============================================================

def print_results(
    query,
    results
):

    print(
        "\n"
        + "=" * 80
    )

    print(
        f"QUERY: {query}"
    )

    print(
        f"INTENT: "
        f"{detect_intent(query)}"
    )

    print(
        "=" * 80
    )

    for index, result in enumerate(
        results,
        start=1
    ):

        print(
            f"\n{index}. "
            f"{result['standard_number']}"
        )

        print(
            f"   "
            f"{result['standard_name']}"
        )

        print(
            f"   Hybrid: "
            f"{result['hybrid_score']:.4f}"
        )

        print(
            f"   CE: "
            f"{result['cross_encoder_score']:.4f}"
        )

        print(
            f"   Title: "
            f"{result['title_score']:.4f}"
        )

        print(
            f"   Product: "
            f"{result['product_score']:.4f}"
        )

        print(
            f"   Family: "
            f"{result['product_family_score']:.4f}"
        )

        print(
            f"   Application: "
            f"{result['application_score']:.4f}"
        )

        print(
            f"   Construction: "
            f"{result['construction_score']:.4f}"
        )

        print(
            f"   Type: "
            f"{result['type_score']:.4f}"
        )

        print(
            f"   Specificity Penalty: "
            f"{result['specificity_penalty']:.4f}"
        )

        print(
            f"   Product Mismatch: "
            f"{result['primary_product_mismatch']:.4f}"
        )

        print(
            f"   Application Mismatch: "
            f"{result['application_mismatch']:.4f}"
        )

        print(
            f"   Compound Product: "
            f"{result['compound_product_score']:.4f}"
        )

        print(
            f"   Compound Mismatch: "
            f"{result['compound_product_mismatch']:.4f}"
        )

        filtered = result.get(
            "filtered_relationships",
            {}
        )

        if not filtered:

            print(
                "   Filtered Relationships: "
                "None"
            )

            continue

        print(
            "   Filtered Relationships:"
        )

        for (
            relationship_type,
            values
        ) in filtered.items():

            if not values:
                continue

            print(
                f"      "
                f"{relationship_type}:"
            )

            for value in values:

                if isinstance(
                    value,
                    dict
                ):

                    number = value.get(
                        "standard_number",
                        ""
                    )

                    name = value.get(
                        "standard_name",
                        ""
                    )

                    score = value.get(
                        "score"
                    )

                    if score is not None:

                        print(
                            f"         - "
                            f"{number} - "
                            f"{name} "
                            f"(score: "
                            f"{float(score):.3f})"
                        )

                    else:

                        print(
                            f"         - "
                            f"{number} - "
                            f"{name}"
                        )

                else:

                    print(
                        f"         - "
                        f"{value}"
                    )


# ============================================================
# MANUAL TESTING
# ============================================================

if __name__ == "__main__":

    queries = [

        "requirements for automobile tyres",

        "automobile tyres",

        "testing of automobile tyres",

        "repair of automobile tyres",

        "500 KVA outdoor distribution transformer",

        "drinking water quality",

        "solar photovoltaic modules",

        "cement concrete for construction",

        "medical oxygen cylinders",

        "steel reinforcement bars for concrete",

        "plain and reinforced concrete",

        "concrete construction",

        "cement for concrete construction",

        "testing of concrete",

        "concrete blocks",

    ]

    for query in queries:

        results = search_bis(
            query
        )

        print_results(
            query,
            results
        )