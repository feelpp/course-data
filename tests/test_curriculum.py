from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def test_curriculum_totals_and_references() -> None:
    curriculum = yaml.safe_load((ROOT / "curriculum.yml").read_text(encoding="utf-8"))
    assert sum(item["weight_percent"] for item in curriculum["assessments"]) == 100
    assert len(curriculum["schedule"]) == curriculum["course"]["delivery_blocks"] == 14
    assert (
        len(curriculum["schedule"]) * curriculum["course"]["block_duration_hours"]
        == curriculum["course"]["contact_hours"]
        == 28
    )
    concept_ids = {item["id"] for item in curriculum["concepts"]}
    assert len(concept_ids) == len(curriculum["concepts"])
    for block in curriculum["schedule"]:
        assert set(block["concepts"]) <= concept_ids


def test_every_essential_or_core_concept_is_scheduled_and_assessed() -> None:
    curriculum = yaml.safe_load((ROOT / "curriculum.yml").read_text(encoding="utf-8"))
    scheduled = {concept for block in curriculum["schedule"] for concept in block["concepts"]}
    practised = {
        concept
        for activity in curriculum["learning_activities"]
        for concept in activity["concepts"]
    }
    for concept in curriculum["concepts"]:
        if concept["priority"] in {"P0", "P1"}:
            assert concept["id"] in scheduled
            assert concept["id"] in practised
            assert concept["assessed_in"]


def test_every_essential_or_core_outcome_is_taught_practised_and_assessed() -> None:
    curriculum = yaml.safe_load((ROOT / "curriculum.yml").read_text(encoding="utf-8"))
    required = {
        outcome["id"]
        for outcome in curriculum["learning_outcomes"]
        if outcome["priority"] in {"P0", "P1"}
    }
    taught = {outcome for block in curriculum["schedule"] for outcome in block["outcomes"]}
    practised = {
        outcome
        for activity in curriculum["learning_activities"]
        for outcome in activity["outcomes"]
    }
    assessed = {
        outcome for assessment in curriculum["assessments"] for outcome in assessment["outcomes"]
    }
    assert required <= taught
    assert required <= practised
    assert required <= assessed


def test_assessments_do_not_require_optional_or_deferred_content() -> None:
    curriculum = yaml.safe_load((ROOT / "curriculum.yml").read_text(encoding="utf-8"))
    assessment_ids = {assessment["id"] for assessment in curriculum["assessments"]}
    for assessment in curriculum["assessments"]:
        assert set(assessment["required_priorities"]) <= {"P0", "P1"}
    for concept in curriculum["concepts"]:
        assert set(concept["assessed_in"]) <= assessment_ids
        if concept["priority"] in {"P2", "P3"}:
            assert not concept["assessed_in"]


def test_schedule_prerequisites_are_taught_earlier() -> None:
    curriculum = yaml.safe_load((ROOT / "curriculum.yml").read_text(encoding="utf-8"))
    first_taught: dict[str, int] = {}
    for block in curriculum["schedule"]:
        for prerequisite in block["prerequisites"]:
            assert first_taught[prerequisite] < block["block"]
        for concept in [*block["concepts"], *block.get("optional_concepts", [])]:
            first_taught.setdefault(concept, block["block"])


def test_foundation_release_inventory_is_complete() -> None:
    curriculum = yaml.safe_load((ROOT / "curriculum.yml").read_text(encoding="utf-8"))
    release = curriculum["foundation_release"]
    assert release["implementation_status"] == "complete"
    assert release["external_academic_review"] == "pending"
    assert len(release["pages"]) == 8
    assert len(release["notebooks"]) == 7
    assert len(release["templates"]) == 5
    for group in ("pages", "notebooks", "templates", "teaching_data"):
        assert all((ROOT / path).exists() for path in release[group])
    assert (ROOT / release["public_specimen"]).exists()
