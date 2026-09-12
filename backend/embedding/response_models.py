
from typing import Optional

from pydantic import BaseModel, Field


# ============================================================
# Retrieved BIS Standard
# ============================================================

class RetrievedStandard(BaseModel):
    """
    Sanitized BIS standard information exposed to the frontend.

    Internal retrieval information such as embedding distances,
    reranker scores, hybrid scores, and vector IDs is intentionally
    excluded.
    """

    standard_number: str
    standard_name: str

    standard_type: Optional[str] = None

    department: Optional[str] = None
    department_code: Optional[str] = None

    committee: Optional[str] = None
    technical_committee: Optional[str] = None

    ics_code: Optional[str] = None

    status: Optional[str] = None
    is_active: Optional[bool] = None

    published_on: Optional[str] = None
    review_on: Optional[str] = None
    reaffirmation_year: Optional[str] = None

    revision_count: Optional[int] = None

    equivalence: Optional[str] = None
    equivalent_is: Optional[str] = None
    identical_is: Optional[str] = None

    supersedes: Optional[str] = None
    superseded_by: Optional[str] = None

    certification_requirement: Optional[str] = None

    bis_detail_url: Optional[str] = None

    relationships: dict = Field(
        default_factory=dict
    )


# ============================================================
# Recommendation
# ============================================================

class Recommendation(BaseModel):
    """
    A single BIS standard recommendation.
    """

    standard_number: str = Field(
        ...,
        description="Exact BIS standard number."
    )

    standard_name: str = Field(
        ...,
        description="Exact BIS standard title."
    )

    relevance: str = Field(
        ...,
        description=(
            "Relevance classification: "
            "direct, specialized, supporting, testing, or related."
        )
    )

    explanation: str = Field(
        ...,
        description="Grounded explanation of why the standard is relevant."
    )

    certification: Optional[str] = Field(
        default=None,
        description=(
            "Certification requirement if explicitly available "
            "in the BIS context."
        )
    )

    testing: list[str] = Field(
        default_factory=list,
        description="Explicit testing information from BIS context."
    )

    amendments: list[str] = Field(
        default_factory=list,
        description="Explicit amendments from BIS context."
    )

    relationships: list[str] = Field(
        default_factory=list,
        description="Explicit BIS relationship information."
    )


# ============================================================
# Pramaan Response
# ============================================================

class PramaanResponse(BaseModel):
    """
    Complete response returned by the Pramaan API.
    """

    query: str = Field(
        ...,
        description="Original user query."
    )

    requirement_understanding: str = Field(
        ...,
        description="Pramaan's understanding of the procurement requirement."
    )

    recommendations: list[Recommendation] = Field(
        default_factory=list,
        description="Final recommended BIS standards."
    )

    retrieved_standards: list[RetrievedStandard] = Field(
        default_factory=list,
        description=(
            "Sanitized BIS standards retrieved by the search and "
            "reranking pipeline."
        )
    )

    notes: list[str] = Field(
        default_factory=list,
        description="Limitations or important notes."
    )

