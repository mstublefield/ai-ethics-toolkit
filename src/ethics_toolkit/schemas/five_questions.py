"""Schema for the Five Questions everyday-decision framework."""

from __future__ import annotations

from pydantic import BaseModel, Field


class FiveQAnswers(BaseModel):
    """Answers to the Five Questions for an everyday AI tool/task decision."""

    task_description: str = Field(..., description="What task are you considering using AI for?")
    why_ai: str = Field(..., description="Q1: Why are you using AI for this task?")
    can_explain: str = Field(
        ..., description="Q2: Can you explain your process clearly and honestly?"
    )
    automation_oversight_balance: str = Field(
        ..., description="Q3: Where is the balance between automation and oversight?"
    )
    fairness_confidence: str = Field(
        ...,
        description=(
            "Q4: Are you confident your AI system doesn't unfairly disadvantage anyone? "
            "On what basis?"
        ),
    )
    pii_disclosure: str = Field(
        ...,
        description=(
            "Q5: Are you sharing personally identifiable information or confidential data "
            "with the AI tool? If so, what anonymisation do you apply?"
        ),
    )
    decision: str = Field("", description="Your resulting decision and any conditions.")
