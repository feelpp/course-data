from pathlib import Path

import nbformat
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
    assert len(release["pages"]) == 9
    assert len(release["notebooks"]) == 7
    assert len(release["templates"]) == 5
    for group in ("pages", "notebooks", "templates", "teaching_data"):
        assert all((ROOT / path).exists() for path in release[group])
    assert (ROOT / release["public_specimen"]).exists()


def test_analytical_release_covers_every_core_concept() -> None:
    curriculum = yaml.safe_load((ROOT / "curriculum.yml").read_text(encoding="utf-8"))
    release = curriculum["analytical_release"]
    expected = {concept["id"] for concept in curriculum["concepts"] if concept["priority"] == "P1"}
    assert release["implementation_status"] == "complete"
    assert set(release["concepts"]) == expected
    assert len(release["pages"]) == len(release["notebooks"]) == 7
    assert len(set(release["question_bank_ids"])) == 7
    for group in ("pages", "notebooks", "teaching_data"):
        assert all((ROOT / path).exists() for path in release[group])
    assert (ROOT / release["project_specification"]).exists()
    assert (ROOT / release["final_specification"]).exists()


def test_assessment_hardening_contract_is_complete() -> None:
    curriculum = yaml.safe_load((ROOT / "curriculum.yml").read_text(encoding="utf-8"))
    record = curriculum["assessment_hardening"]
    assert record["implementation_status"] == "complete"
    assert record["live_release_status"] == "pending_human_signoff_and_physical_pilot"
    assert record["variant_counts"] == {"control_1": 2, "control_2": 2, "final": 3}
    assert record["final_roles"] == ["main", "retake", "reserve"]
    assert set(record["required_priorities"]) == {"P0", "P1"}
    assert record["network_required"] is False
    assert record["personal_account_required"] is False
    assert record["accelerator_required"] is False
    assert record["runtime_used_for_marks"] is False
    assert len(record["private_controls"]) == 7
    assert (ROOT / record["public_delivery_page"]).exists()
    assert (ROOT / record["validation_record"]).exists()


def test_enrichment_is_complete_optional_and_removable() -> None:
    curriculum = yaml.safe_load((ROOT / "curriculum.yml").read_text(encoding="utf-8"))
    release = curriculum["enrichment_release"]
    expected_p2 = {
        concept["id"] for concept in curriculum["concepts"] if concept["priority"] == "P2"
    }
    assert release["implementation_status"] == "complete"
    assert release["required_contact_hours"] == 0
    assert release["assessment_eligible"] is False
    assert release["removable_without_core_loss"] is True
    assert set(release["concepts"]) == expected_p2
    assert len(release["pages"]) == 7
    assert len(release["notebooks"]) == 1
    for relative in release["pages"]:
        source = (ROOT / relative).read_text(encoding="utf-8")
        assert ":page-course-priority: P2" in source
        assert ":page-course-assessed: no" in source
    notebook = nbformat.read(ROOT / release["notebooks"][0], as_version=4)
    assert notebook.metadata["course"]["priority"] == "P2"
    assert notebook.metadata["course"]["assessed"] is False
    assert notebook.metadata["course"]["execution_profile"] == "full"
    for key in ("validation_record", "downstream_record"):
        assert (ROOT / release[key]).exists()
    core_paths = [
        *curriculum["foundation_release"]["pages"],
        *curriculum["foundation_release"]["notebooks"],
        *curriculum["analytical_release"]["pages"],
        *curriculum["analytical_release"]["notebooks"],
    ]
    assert all("/extensions/" not in path for path in core_paths)
