"""Regression tests for the pii-phone rule.

FIE-2026: the phone regex matched numeric Facebook page/post IDs in URLs
(e.g. facebook.com/101676962734559), firing false-positive pii-phone findings.
The fix adds a (?<![/=]) lookbehind so digit runs that are URL path or
query-parameter components are not treated as phone numbers, while real phone
numbers (which appear after whitespace/words, not after / or =) still match.
"""

from __future__ import annotations

from pathlib import Path

from ethics_toolkit.commands.lint_disclosure import run


def _phone_findings(tmp_path: Path, text: str) -> list:
    target = tmp_path / "doc.md"
    target.write_text(text, encoding="utf-8")
    report = run(target)
    return [f for f in report.findings if f.rule_id == "pii-phone"]


# --- false positives that must NOT fire (URL path / query digit runs) ---


def test_facebook_page_id_in_path_not_flagged(tmp_path: Path) -> None:
    text = "Profile: https://www.facebook.com/101676962734559"
    assert _phone_findings(tmp_path, text) == []


def test_facebook_fbid_query_param_not_flagged(tmp_path: Path) -> None:
    text = "See https://www.facebook.com/photo?fbid=101676962734559&type=3"
    assert _phone_findings(tmp_path, text) == []


def test_post_id_in_path_not_flagged(tmp_path: Path) -> None:
    text = "Source: facebook.com/acme/posts/100089476962734/"
    assert _phone_findings(tmp_path, text) == []


# --- real phone numbers that MUST still fire ---


def test_phone_with_dashes_still_flagged(tmp_path: Path) -> None:
    text = "Call us at 417-555-0123 during business hours."
    assert len(_phone_findings(tmp_path, text)) >= 1


def test_intl_phone_still_flagged(tmp_path: Path) -> None:
    text = "Reach +1 (202) 555-0147 anytime."
    assert len(_phone_findings(tmp_path, text)) >= 1


def test_dotted_phone_still_flagged(tmp_path: Path) -> None:
    text = "Fax: 212.555.7890"
    assert len(_phone_findings(tmp_path, text)) >= 1


def test_bare_ten_digit_phone_still_flagged(tmp_path: Path) -> None:
    text = "Text 2025550147 to opt in."
    assert len(_phone_findings(tmp_path, text)) >= 1
