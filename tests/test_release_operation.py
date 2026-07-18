import csv
import zipfile
from pathlib import Path

from tools.build_student_bundle import build_bundle
from tools.summarise_course_evidence import summarise_feedback, summarise_items
from tools.validate_student_bundle import validate_bundle


def test_student_bundle_is_complete_and_public(tmp_path: Path) -> None:
    bundle = build_bundle(tmp_path / "student.zip")
    assert validate_bundle(bundle) == []
    with zipfile.ZipFile(bundle) as archive:
        names = set(archive.namelist())
    assert "templates/block-feedback.csv" in names
    assert "templates/release-approval.md" not in names
    assert "templates/assessment-item-statistics.csv" not in names
    first = bundle.read_bytes()
    assert build_bundle(bundle).read_bytes() == first


def write_csv(path: Path, fieldnames: list[str], rows: list[dict]) -> None:
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def test_anonymous_feedback_and_item_summaries(tmp_path: Path) -> None:
    feedback = tmp_path / "feedback.csv"
    write_csv(
        feedback,
        ["clarity_score", "confidence_score", "task_minutes", "blocked_surface"],
        [
            {
                "clarity_score": "3",
                "confidence_score": "2",
                "task_minutes": "40",
                "blocked_surface": "notebook",
            },
            {
                "clarity_score": "5",
                "confidence_score": "4",
                "task_minutes": "20",
                "blocked_surface": "",
            },
        ],
    )
    assert summarise_feedback(feedback) == {
        "response_count": 2,
        "median_clarity": 4.0,
        "median_confidence": 3.0,
        "median_task_minutes": 30.0,
        "blocked_surfaces": {"notebook": 1},
    }

    items = tmp_path / "items.csv"
    write_csv(
        items,
        ["item_id", "candidate_count", "review_flag"],
        [
            {"item_id": "Q1", "candidate_count": "20", "review_flag": ""},
            {"item_id": "Q2", "candidate_count": "20", "review_flag": "difficulty"},
        ],
    )
    assert summarise_items(items) == {
        "item_count": 2,
        "candidate_count": 20,
        "review_items": ["Q2"],
    }
