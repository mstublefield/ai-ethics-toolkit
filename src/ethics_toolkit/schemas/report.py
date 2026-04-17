"""Schema for the 🛡️ AI Ethics Assessment Report bundle."""

from __future__ import annotations

from datetime import date

from pydantic import BaseModel, Field


class ReportFinding(BaseModel):
    """A single finding in the report."""

    area: str = Field(..., description="Principle or category (e.g., 'transparency').")
    severity: str = Field("medium", description="low / medium / high / critical.")
    description: str = Field(..., description="What was found.")
    recommendation: str = Field("", description="What to do about it.")


class ReportBundle(BaseModel):
    """Inputs for assembling the 🛡️ AI Ethics Assessment Report."""

    subject: str = Field(..., description="What is being reviewed (a feature, a draft, a dataset).")
    reviewer: str = Field(..., description="Who is producing the report.")
    date_of_review: date = Field(default_factory=date.today)
    executive_summary: str = Field(..., description="2–4 sentence summary for a busy reader.")
    context: str = Field("", description="Relevant background.")
    findings: list[ReportFinding] = Field(default_factory=list)
    regulatory_notes: str = Field(
        "", description="EU AI Act / NIST RMF / ISO 42001 relevance, if any."
    )
    mitigations: list[str] = Field(default_factory=list, description="Recommended mitigations.")
    monitoring_plan: str = Field("", description="How this will be monitored over time.")
    residual_risk: str = Field("", description="What remains unresolved.")
