"""Schema for the Five-Layer AI Impact Analysis."""

from __future__ import annotations

from pydantic import BaseModel, Field


class Layer(BaseModel):
    """One impact layer — three question-answer pairs."""

    q1: str = Field("", description="Answer to the first question at this layer.")
    q2: str = Field("", description="Answer to the second question at this layer.")
    q3: str = Field("", description="Answer to the third question at this layer.")
    additional_notes: str = Field("", description="Anything else surfaced at this layer.")


class ImpactAnswers(BaseModel):
    """Filled-in Five-Layer Impact Analysis for a medium-scale AI decision."""

    decision_description: str = Field(
        ..., description="The AI use / workflow change / project decision under analysis."
    )
    personal: Layer = Field(default_factory=Layer, description="Impact on you.")
    relational: Layer = Field(
        default_factory=Layer, description="Impact on clients, collaborators, end users."
    )
    business: Layer = Field(default_factory=Layer, description="Impact on your business.")
    industry: Layer = Field(default_factory=Layer, description="Impact on your field.")
    society: Layer = Field(default_factory=Layer, description="Impact on the world.")
    compounding_risks: str = Field(
        "", description="Risks that show up across multiple layers."
    )
    compounding_benefits: str = Field(
        "", description="Benefits that show up across multiple layers."
    )
    proceed: str = Field(
        "", description="Your recommended posture: proceed / proceed with conditions / stop."
    )
