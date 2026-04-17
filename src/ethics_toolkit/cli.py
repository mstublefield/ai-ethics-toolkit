"""ai-ethics-toolkit — CLI entry point."""

from __future__ import annotations

from enum import Enum
from pathlib import Path

import typer

from ethics_toolkit import __version__
from ethics_toolkit.commands import (
    crosswalk as cmd_crosswalk,
)
from ethics_toolkit.commands import (
    five_questions as cmd_five_questions,
)
from ethics_toolkit.commands import (
    impact_worksheet as cmd_impact_worksheet,
)
from ethics_toolkit.commands import (
    lint_disclosure as cmd_lint_disclosure,
)
from ethics_toolkit.commands import (
    render_policy as cmd_render_policy,
)
from ethics_toolkit.commands import (
    report as cmd_report,
)
from ethics_toolkit.commands import (
    scan_worksheet as cmd_scan_worksheet,
)

app = typer.Typer(
    name="ethics",
    help="Local CLI for AI ethics review. Does mechanical work; Claude does judgment.",
    no_args_is_help=True,
    add_completion=False,
)

worksheet_app = typer.Typer(help="Emit blank worksheets for the decision frameworks.")
app.add_typer(worksheet_app, name="worksheet")


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"ai-ethics-toolkit {__version__}")
        raise typer.Exit()


@app.callback()
def _root(
    version: bool = typer.Option(
        False, "--version", callback=_version_callback, is_eager=True, help="Print version and exit."
    ),
) -> None:
    """Ethics toolkit root command."""


# ---------------------------------------------------------------------------
# render-policy
# ---------------------------------------------------------------------------
@app.command("render-policy")
def render_policy(
    in_path: Path = typer.Option(..., "--in", help="YAML/JSON file with PolicyInputs."),
    out_path: Path = typer.Option(..., "--out", help="Destination path for the filled policy."),
    schema: bool = typer.Option(False, "--schema", help="Print the input JSON schema and exit."),
) -> None:
    """Fill the AI use policy template from your values."""
    if schema:
        cmd_render_policy.print_schema()
        return
    cmd_render_policy.run(in_path, out_path)


# ---------------------------------------------------------------------------
# worksheet impact / scan
# ---------------------------------------------------------------------------
@worksheet_app.command("impact")
def worksheet_impact(
    out_path: Path = typer.Option(..., "--out", help="Destination for the blank worksheet."),
) -> None:
    """Emit a blank Five-Layer Impact Analysis worksheet."""
    cmd_impact_worksheet.render_blank(out_path)


@worksheet_app.command("scan")
def worksheet_scan(
    out_path: Path = typer.Option(..., "--out", help="Destination for the blank worksheet."),
) -> None:
    """Emit a blank Consequence Scanning worksheet."""
    cmd_scan_worksheet.render_blank(out_path)


# ---------------------------------------------------------------------------
# lint-disclosure
# ---------------------------------------------------------------------------
@app.command("lint-disclosure")
def lint_disclosure(
    target: Path = typer.Argument(..., help="File to lint (markdown or plain text)."),
    as_json: bool = typer.Option(False, "--json", help="Emit findings as JSON on stdout."),
    schema: bool = typer.Option(False, "--schema", help="Print the output JSON schema and exit."),
) -> None:
    """Check a draft for disclosure gaps, PII-shaped strings, and risky claims."""
    if schema:
        cmd_lint_disclosure.print_schema()
        return
    findings = cmd_lint_disclosure.run(target)
    exit_code = cmd_lint_disclosure.report(findings, as_json=as_json)
    raise typer.Exit(code=exit_code)


# ---------------------------------------------------------------------------
# crosswalk
# ---------------------------------------------------------------------------
class CrosswalkTarget(str, Enum):
    nist_rmf = "nist_rmf"
    iso_42001 = "iso_42001"


@app.command("crosswalk")
def crosswalk(
    policy: Path = typer.Option(..., "--policy", help="Path to a rendered policy markdown file."),
    against: CrosswalkTarget = typer.Option(
        ..., "--against", help="Standards checklist to compare against."
    ),
    as_json: bool = typer.Option(False, "--json", help="Emit gaps as JSON on stdout."),
) -> None:
    """Diff a policy markdown file against a standards checklist."""
    result = cmd_crosswalk.run(policy, against.value)
    exit_code = cmd_crosswalk.report(result, as_json=as_json)
    raise typer.Exit(code=exit_code)


# ---------------------------------------------------------------------------
# report
# ---------------------------------------------------------------------------
@app.command("report")
def report(
    in_path: Path = typer.Option(..., "--inputs", help="JSON/YAML file with ReportBundle."),
    out_path: Path = typer.Option(..., "--out", help="Destination for the assembled report."),
    schema: bool = typer.Option(False, "--schema", help="Print the input JSON schema and exit."),
) -> None:
    """Assemble the 🛡️ AI Ethics Assessment Report from a filled-in bundle."""
    if schema:
        cmd_report.print_schema()
        return
    cmd_report.run(in_path, out_path)


# ---------------------------------------------------------------------------
# five-questions
# ---------------------------------------------------------------------------
@app.command("five-questions")
def five_questions(
    scaffold: bool = typer.Option(False, "--scaffold", help="Emit a blank input YAML."),
    in_path: Path = typer.Option(None, "--in", help="Path to filled FiveQAnswers YAML/JSON."),
    out_path: Path = typer.Option(None, "--out", help="Destination for scaffold or rendered output."),
    schema: bool = typer.Option(False, "--schema", help="Print the input JSON schema and exit."),
) -> None:
    """Five Questions scaffold + renderer for everyday AI decisions."""
    if schema:
        cmd_five_questions.print_schema()
        return
    if scaffold:
        if out_path is None:
            typer.echo("Error: --out is required with --scaffold", err=True)
            raise typer.Exit(code=1)
        cmd_five_questions.render_scaffold(out_path)
        return
    if in_path is None or out_path is None:
        typer.echo("Error: provide --scaffold --out, OR --in and --out.", err=True)
        raise typer.Exit(code=1)
    cmd_five_questions.render_filled(in_path, out_path)


# ---------------------------------------------------------------------------
# impact-analyze
# ---------------------------------------------------------------------------
@app.command("impact-analyze")
def impact_analyze(
    scaffold: bool = typer.Option(False, "--scaffold", help="Emit a blank input YAML."),
    in_path: Path = typer.Option(None, "--in", help="Path to filled ImpactAnswers YAML/JSON."),
    out_path: Path = typer.Option(None, "--out", help="Destination for scaffold or rendered output."),
    schema: bool = typer.Option(False, "--schema", help="Print the input JSON schema and exit."),
) -> None:
    """Five-Layer Impact Analysis scaffold + renderer for project-level decisions."""
    if schema:
        cmd_impact_worksheet.print_schema()
        return
    if scaffold:
        if out_path is None:
            typer.echo("Error: --out is required with --scaffold", err=True)
            raise typer.Exit(code=1)
        cmd_impact_worksheet.render_scaffold(out_path)
        return
    if in_path is None or out_path is None:
        typer.echo("Error: provide --scaffold --out, OR --in and --out.", err=True)
        raise typer.Exit(code=1)
    cmd_impact_worksheet.render_filled(in_path, out_path)


# ---------------------------------------------------------------------------
# fairness (lazy import — requires [fairness] extra)
# ---------------------------------------------------------------------------
@app.command("fairness")
def fairness(
    data: Path = typer.Option(..., "--data", help="Path to CSV dataset."),
    target: str = typer.Option(..., "--target", help="Outcome column name (0/1 or categorical)."),
    protected: str = typer.Option(
        ..., "--protected", help="Comma-separated protected attribute columns."
    ),
    out_path: Path = typer.Option(..., "--out", help="Destination for the fairness report."),
    score: str = typer.Option(
        None, "--score", help="Optional continuous score/probability column."
    ),
    positive_label: str = typer.Option(
        "1",
        "--positive-label",
        help="Value in target that represents the positive/favorable outcome.",
    ),
    schema: bool = typer.Option(False, "--schema", help="Print the input JSON schema and exit."),
) -> None:
    """Run fairness metrics on a CSV. Requires the [fairness] optional extra."""
    try:
        from ethics_toolkit.commands import fairness as cmd_fairness
    except ImportError as e:
        typer.echo(
            f"Error: fairness extras not installed. Run `uv sync --extra fairness`.\n({e})",
            err=True,
        )
        raise typer.Exit(code=1) from e

    if schema:
        cmd_fairness.print_schema()
        return
    protected_list = [c.strip() for c in protected.split(",") if c.strip()]
    # Coerce positive_label to int if it looks like one
    pl: object = positive_label
    if positive_label.lstrip("-").isdigit():
        pl = int(positive_label)
    cmd_fairness.run(
        data_path=data,
        target_column=target,
        protected_columns=protected_list,
        score_column=score,
        positive_label=pl,
        out_path=out_path,
    )


if __name__ == "__main__":
    app()
