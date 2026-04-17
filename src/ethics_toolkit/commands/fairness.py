"""`ethics fairness` — local fairness-metric audit against a CSV.

Requires the `[fairness]` optional extra: pandas, scikit-learn, scipy, fairlearn.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

import numpy as np
import pandas as pd

from ethics_toolkit.commands._template_engine import render
from ethics_toolkit.io import print_schema as _print, write_text
from ethics_toolkit.schemas import FairnessInputs


def print_schema() -> None:
    _print(FairnessInputs)


# ---------------------------------------------------------------------------
# Severity classification (adapted from jeremylongshore/claude-code-plugins-plus-skills, MIT)
# ---------------------------------------------------------------------------
def _classify(ratio: float) -> str:
    """Four-fifths rule severity classification."""
    if ratio >= 0.90:
        return "low"
    if ratio >= 0.80:
        return "medium"
    if ratio >= 0.70:
        return "high"
    return "critical"


_SEVERITY_ORDER = {"low": 0, "medium": 1, "high": 2, "critical": 3}


@dataclass
class GroupStat:
    label: str
    n: int
    rate: float
    ratio_vs_max: float
    severity: str


@dataclass
class AttributeReport:
    name: str
    groups: list[GroupStat]
    dpd: float  # demographic parity difference (max - min selection rate)
    dpr: float  # demographic parity ratio (min / max)
    eo_diff: float | None  # equalized odds difference (TPR gap), if score available
    four_fifths_violations: list[dict] = field(default_factory=list)


@dataclass
class ProxyHit:
    feature: str
    protected: str
    r: float


def _compute_attribute(
    df: pd.DataFrame,
    protected_col: str,
    target_col: str,
    positive_label: object,
    score_col: str | None,
) -> AttributeReport:
    """Compute metrics for one protected attribute."""
    groups = []
    rates_by_group = {}

    for label, group_df in df.groupby(protected_col, dropna=False):
        n = len(group_df)
        if n == 0:
            continue
        positives = (group_df[target_col] == positive_label).sum()
        rate = float(positives) / n if n else 0.0
        rates_by_group[str(label)] = rate
        groups.append((str(label), n, rate))

    if not groups:
        return AttributeReport(
            name=protected_col, groups=[], dpd=0.0, dpr=1.0, eo_diff=None
        )

    max_rate = max(rates_by_group.values()) or 1e-12
    min_rate = min(rates_by_group.values())
    dpd = max_rate - min_rate
    dpr = min_rate / max_rate if max_rate else 1.0

    group_stats = []
    violations = []
    for label, n, rate in groups:
        ratio_vs_max = rate / max_rate if max_rate else 1.0
        severity = _classify(ratio_vs_max)
        group_stats.append(
            GroupStat(label=label, n=n, rate=rate, ratio_vs_max=ratio_vs_max, severity=severity)
        )
        if ratio_vs_max < 0.80:
            violations.append({"label": label, "ratio": ratio_vs_max})

    # Equalized odds (TPR) gap if a continuous score is provided and we can threshold
    eo_diff: float | None = None
    if score_col is not None and score_col in df.columns:
        # Use positive_label to identify true positives; simple 0.5 threshold on score.
        tprs = []
        for label, group_df in df.groupby(protected_col, dropna=False):
            positives_mask = group_df[target_col] == positive_label
            if positives_mask.sum() == 0:
                continue
            pred_positive = group_df[score_col].astype(float) >= 0.5
            tpr = float((pred_positive & positives_mask).sum()) / float(positives_mask.sum())
            tprs.append(tpr)
        if len(tprs) >= 2:
            eo_diff = max(tprs) - min(tprs)

    return AttributeReport(
        name=protected_col,
        groups=group_stats,
        dpd=dpd,
        dpr=dpr,
        eo_diff=eo_diff,
        four_fifths_violations=violations,
    )


def _find_proxies(
    df: pd.DataFrame,
    protected_cols: list[str],
    threshold: float,
) -> list[ProxyHit]:
    """Find non-protected numeric columns correlated with protected attributes."""
    hits: list[ProxyHit] = []
    numeric_df = df.select_dtypes(include=[np.number])
    for protected in protected_cols:
        if protected not in df.columns:
            continue
        # Convert protected column to numeric codes for correlation.
        codes = pd.Categorical(df[protected]).codes.astype(float)
        if pd.isna(codes).all():
            continue
        for feature in numeric_df.columns:
            if feature in protected_cols:
                continue
            series = numeric_df[feature].astype(float)
            if series.std() == 0 or codes.std() == 0:
                continue
            # Pearson correlation on aligned, non-null pairs.
            mask = series.notna() & ~np.isnan(codes)
            if mask.sum() < 10:
                continue
            r = float(np.corrcoef(series[mask], codes[mask.values])[0, 1])
            if abs(r) >= threshold:
                hits.append(ProxyHit(feature=feature, protected=protected, r=r))
    return hits


def _build_mitigations(
    attributes: list[AttributeReport], worst_severity: str
) -> list[str]:
    """Return text-only mitigation suggestions."""
    suggestions = []
    if worst_severity in {"high", "critical"}:
        suggestions.append(
            "Treat this as a potential adverse-impact finding. Document whether the protected attribute "
            "is a permissible factor for the decision being made, and under what legal/ethical basis."
        )
        suggestions.append(
            "Before deploying, apply a mitigation technique: threshold adjustment per group, "
            "reweighing during training (fairlearn.reductions.ExponentiatedGradient), or post-hoc "
            "calibration. Measure the trade-off with overall accuracy."
        )
    suggestions.append(
        "Monitor these metrics on an ongoing basis — one audit is a snapshot, not a guarantee."
    )
    suggestions.append(
        "Engage affected groups when possible. Statistical parity isn't the same as fairness to the "
        "people affected; domain expertise and stakeholder input matter."
    )
    if any(a.four_fifths_violations for a in attributes):
        suggestions.append(
            "Four-fifths rule violations detected — these are a well-established disparate-impact signal "
            "in US employment context and a useful alarm elsewhere."
        )
    return suggestions


def _worst_severity(attributes: list[AttributeReport]) -> str:
    worst = "low"
    for a in attributes:
        for g in a.groups:
            if _SEVERITY_ORDER[g.severity] > _SEVERITY_ORDER[worst]:
                worst = g.severity
    return worst


def run(
    data_path: Path,
    target_column: str,
    protected_columns: list[str],
    score_column: str | None,
    positive_label: object,
    out_path: Path,
    proxy_threshold: float = 0.3,
) -> None:
    df = pd.read_csv(data_path)

    for col in [target_column, *protected_columns]:
        if col not in df.columns:
            raise ValueError(f"Column not in CSV: {col}. Available: {list(df.columns)}")
    if score_column is not None and score_column not in df.columns:
        raise ValueError(f"Score column not in CSV: {score_column}")

    attributes: list[AttributeReport] = []
    for protected in protected_columns:
        attributes.append(
            _compute_attribute(df, protected, target_column, positive_label, score_column)
        )

    proxies = _find_proxies(df, protected_columns, proxy_threshold)
    worst = _worst_severity(attributes)
    mitigations = _build_mitigations(attributes, worst)

    context = {
        "data_path": str(data_path),
        "target_column": target_column,
        "protected_columns": protected_columns,
        "score_column": score_column,
        "positive_label": str(positive_label),
        "n_rows": len(df),
        "date_of_review": date.today().isoformat(),
        "overall_rate": float((df[target_column] == positive_label).mean()),
        "worst_severity": worst,
        "attributes": [
            {
                "name": a.name,
                "groups": [g.__dict__ for g in a.groups],
                "dpd": a.dpd,
                "dpr": a.dpr,
                "eo_diff": a.eo_diff,
                "four_fifths_violations": a.four_fifths_violations,
            }
            for a in attributes
        ],
        "proxies": [p.__dict__ for p in proxies],
        "proxy_threshold": proxy_threshold,
        "mitigations": mitigations,
    }

    output = render("fairness_report.md.j2", **context)
    write_text(out_path, output)

    # Print a one-line summary + JSON stats for Claude to reason over
    print(
        json.dumps(
            {
                "out": str(out_path),
                "n_rows": len(df),
                "worst_severity": worst,
                "attributes": [
                    {
                        "name": a.name,
                        "dpr": a.dpr,
                        "dpd": a.dpd,
                        "violations": len(a.four_fifths_violations),
                    }
                    for a in attributes
                ],
                "proxies_found": len(proxies),
            },
            indent=2,
        )
    )
