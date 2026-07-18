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
    for concept in curriculum["concepts"]:
        if concept["priority"] in {"P0", "P1"}:
            assert concept["id"] in scheduled
            assert concept["assessed_in"]
