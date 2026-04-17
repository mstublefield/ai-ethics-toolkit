"""Schema for fairness-audit inputs."""

from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, Field


class FairnessInputs(BaseModel):
    """Inputs for a fairness metric run against a CSV."""

    data_path: Path = Field(..., description="Path to CSV file.")
    target_column: str = Field(
        ..., description="Name of the outcome/prediction column (0/1 or categorical)."
    )
    protected_columns: list[str] = Field(
        ..., description="Names of protected-attribute columns (e.g., ['gender', 'race'])."
    )
    score_column: str | None = Field(
        None,
        description=(
            "Optional continuous score column (probabilities). If provided, calibration "
            "and score-based metrics are computed."
        ),
    )
    positive_label: object = Field(
        1, description="Value in target_column that represents the positive/favorable outcome."
    )
    proxy_correlation_threshold: float = Field(
        0.3,
        description="Pearson |r| threshold above which a non-protected feature is flagged as a proxy.",
    )
