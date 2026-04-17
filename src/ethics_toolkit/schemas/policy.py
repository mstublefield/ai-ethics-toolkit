"""Schema for the AI use policy inputs."""

from __future__ import annotations

from datetime import date

from pydantic import BaseModel, Field


class PrincipleStatement(BaseModel):
    """What a principle means to you, and why it matters."""

    meaning: str = Field(..., description="What this principle means in your practice.")
    why_it_matters: str = Field(..., description="Why this principle matters in your work.")


class AccountabilityStatement(PrincipleStatement):
    review_process: list[str] = Field(default_factory=list, description="Your review steps.")
    checkpoints: list[str] = Field(default_factory=list, description="Your quality checkpoints.")
    documentation: list[str] = Field(
        default_factory=list, description="What you document for traceability."
    )
    ownership: list[str] = Field(default_factory=list, description="Ownership and IP clarifications.")


class Phase(BaseModel):
    """One phase of your project workflow."""

    name: str = Field(..., description="Phase name (e.g., 'Research', 'Drafting').")
    use_ai_for: list[str] = Field(default_factory=list, description="Specific tasks where AI is used.")
    never_use_ai_for: list[str] = Field(
        default_factory=list, description="Specific exclusions — AI must not touch these."
    )
    non_negotiables: list[str] = Field(
        default_factory=list, description="Safeguards and hard boundaries for this phase."
    )
    why_this_matters: str = Field("", description="Why these choices matter for this phase.")


class ApprovedTool(BaseModel):
    """An AI tool you've approved for specific use."""

    name: str = Field(..., description="Tool name (e.g., 'ChatGPT', 'Claude', 'Grammarly').")
    purpose: str = Field(..., description="What you use it for.")
    rationale: str = Field("", description="Optional: why this tool over alternatives.")


class PolicyInputs(BaseModel):
    """Everything needed to render a full AI use policy."""

    owner_name: str = Field(..., description="Your name or business name.")
    approach: str = Field(
        ...,
        description=(
            "2–3 paragraphs on your philosophy: why you use AI (or don't), "
            "what you believe it should/shouldn't do, how it fits your value proposition, "
            "and your commitment to clients."
        ),
    )
    principles: dict[str, PrincipleStatement | AccountabilityStatement] = Field(
        ...,
        description=(
            "Keyed by principle: privacy, fairness, transparency, accountability, quality. "
            "accountability uses AccountabilityStatement."
        ),
    )
    phases: list[Phase] = Field(
        ..., description="Ordered list of project phases with AI usage rules for each."
    )
    approved_tools: list[ApprovedTool] = Field(
        default_factory=list, description="Your approved AI tool set."
    )
    client_permission_note: str = Field(
        "", description="How and when you ask clients for permission."
    )
    tool_selection_criteria: str = Field(
        "", description="How you evaluate new AI tools before adopting them."
    )
    review_frequency: str = Field("quarterly", description="How often you review this policy.")
    subcontractor_clause: str = Field(
        "",
        description=(
            "Optional: text for subcontractors/collaborators (e.g., 'anyone working with me "
            "is required to follow these guidelines')."
        ),
    )
    last_updated: date = Field(default_factory=date.today, description="Last-updated date.")
    version: str = Field("0.1.0", description="Policy version.")
