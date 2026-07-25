#!/usr/bin/env python3
"""Summarise anonymous block feedback and aggregate assessment-item statistics."""

from __future__ import annotations

import argparse
import csv
import json
import statistics
from collections import Counter
from pathlib import Path


def number(value: str) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def median(values: list[float]) -> float | None:
    return statistics.median(values) if values else None


def summarise_feedback(path: Path) -> dict:
    with path.open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream))
    clarity = [value for row in rows if (value := number(row.get("clarity_score", ""))) is not None]
    confidence = [
        value for row in rows if (value := number(row.get("confidence_score", ""))) is not None
    ]
    minutes = [value for row in rows if (value := number(row.get("task_minutes", ""))) is not None]
    blocked = Counter(row.get("blocked_surface", "").strip() for row in rows)
    blocked.pop("", None)
    return {
        "response_count": len(rows),
        "median_clarity": median(clarity),
        "median_confidence": median(confidence),
        "median_task_minutes": median(minutes),
        "blocked_surfaces": dict(sorted(blocked.items())),
    }


def summarise_items(path: Path) -> dict:
    with path.open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream))
    flags = [row["item_id"] for row in rows if row.get("review_flag", "").strip()]
    return {
        "item_count": len(rows),
        "candidate_count": max((int(row["candidate_count"]) for row in rows), default=0),
        "review_items": flags,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--feedback", type=Path, required=True)
    parser.add_argument("--items", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    payload = {
        "privacy": "aggregate-only; no direct identifiers or student-level assessment rows",
        "feedback": summarise_feedback(args.feedback),
        "assessment_items": summarise_items(args.items),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(f"Wrote aggregate evidence to {args.output}")


if __name__ == "__main__":
    main()
