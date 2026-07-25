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
    assert len(release["pages"]) == 12
    assert len(release["notebook_sources"]) == 10
    assert len(release["templates"]) == 5
    for group in ("pages", "notebook_sources", "templates", "teaching_data"):
        assert all((ROOT / path).exists() for path in release[group])
    assert (ROOT / release["public_specimen"]).exists()


def test_foundation_navigation_follows_the_student_sequence() -> None:
    nav = (ROOT / "docs/course/modules/ROOT/nav.adoc").read_text(encoding="utf-8")
    sequence = [
        "foundations/data-lifecycle.adoc",
        "foundations/tabular-data.adoc",
        "foundations/data-quality.adoc",
        "foundations/mathematical-background.adoc",
        "foundations/probability-distributions-moments.adoc",
        "foundations/quantiles-exceedance-risk.adoc",
        "foundations/mean-uncertainty.adoc",
        "foundations/eda-sampling.adoc",
        "foundations/safe-pipelines.adoc",
        "foundations/metrics-errors.adoc",
        "foundations/reproducible-delivery.adoc",
        "foundations/baseline-synthesis.adoc",
    ]
    positions = [nav.index(item) for item in sequence]
    assert positions == sorted(positions)


def test_analytical_release_covers_every_core_concept() -> None:
    curriculum = yaml.safe_load((ROOT / "curriculum.yml").read_text(encoding="utf-8"))
    release = curriculum["analytical_release"]
    expected = {concept["id"] for concept in curriculum["concepts"] if concept["priority"] == "P1"}
    assert release["implementation_status"] == "complete"
    assert set(release["concepts"]) == expected
    assert len(release["pages"]) == 7
    assert len(release["notebooks"]) == 0
    assert len(release["notebook_sources"]) == 7
    assert len(set(release["question_bank_ids"])) == 7
    for group in ("pages", "notebooks", "notebook_sources", "teaching_data"):
        assert all((ROOT / path).exists() for path in release[group])
    assert (ROOT / release["project_specification"]).exists()
    assert (ROOT / release["final_specification"]).exists()


def test_worked_example_release_has_complete_learning_contract() -> None:
    curriculum = yaml.safe_load((ROOT / "curriculum.yml").read_text(encoding="utf-8"))
    release = curriculum["worked_example_release"]
    foundation_pages = set(curriculum["foundation_release"]["pages"])
    analytical_pages = set(curriculum["analytical_release"]["pages"])
    notebook_sources = {
        *curriculum["foundation_release"]["notebook_sources"],
        *curriculum["analytical_release"]["notebook_sources"],
    }

    assert release["implementation_status"] == "complete"
    assert release["human_review_status"] == "pending_instructor_and_real_student_review"
    assert release["required_structure"] == [
        "Context",
        "Method",
        "Implementation",
        "Results",
        "Conclusion",
    ]
    assert set(release["pages"]) == foundation_pages | analytical_pages
    assert set(release["notebook_sources"]) == notebook_sources
    assert set(release["page_only"]) == (foundation_pages | analytical_pages) - notebook_sources
    assert len(release["pages"]) == 19
    assert len(release["notebook_sources"]) == 17
    for relative in [
        *release["pages"],
        release["authoring_contract"],
        release["validation_record"],
    ]:
        assert (ROOT / relative).exists()


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


def test_public_exercise_contracts_match_assessments_and_pages() -> None:
    curriculum = yaml.safe_load((ROOT / "curriculum.yml").read_text(encoding="utf-8"))
    release = curriculum["exercise_release"]
    assessments = {item["id"]: item for item in curriculum["assessments"]}
    rubric_ids = set(release["rubric"]["criteria"])
    assert release["implementation_status"] == "complete"
    assert release["assessment_custodian_status"] == "pending_human_signoff"
    assert {item["assessment_id"] for item in release["public_specimens"]} == set(assessments)
    assert all((ROOT / release[key]).exists() for key in ("conventions_page", "validation_record"))
    assert (ROOT / release["rubric"]["source"]).exists()

    task_ids: list[str] = []
    for specimen in release["public_specimens"]:
        assessment = assessments[specimen["assessment_id"]]
        source = (ROOT / specimen["source"]).read_text(encoding="utf-8")
        tasks = specimen["tasks"]
        task_ids.extend(task["id"] for task in tasks)
        assert sum(task["points"] for task in tasks) == assessment["points"]
        assert specimen["ai_mode"] == assessment["ai_mode"]
        assert ":page-jupyter:" in source
        assert f":page-course-exercise-id: {specimen['exercise_id']}" in source
        assert f":page-course-ai-mode: {specimen['ai_mode']}" in source
        for task in tasks:
            assert set(task["priorities"]) <= {"P0", "P1"}
            assert set(task["rubric_criteria"]) <= rubric_ids
            assert source.count(task["id"]) >= 2
    assert len(task_ids) == len(set(task_ids))


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
    assert len(release["page_notebook_sources"]) == 4
    assert len(release["notebooks"]) == 1
    for relative in release["pages"]:
        source = (ROOT / relative).read_text(encoding="utf-8")
        assert ":page-course-priority: P2" in source
        assert ":page-course-assessed: no" in source
    contract = release["source_contract"]
    assert set(contract["asciidoc_notebook"]) == set(release["page_notebook_sources"])
    assert len(contract["notebook_native_exceptions"]) == 1
    assert len(contract["page_only_exceptions"]) == 2
    classified_pages = [
        *contract["asciidoc_notebook"],
        *(item["page"] for item in contract["notebook_native_exceptions"]),
        *(item["page"] for item in contract["page_only_exceptions"]),
    ]
    assert set(classified_pages) == set(release["pages"])
    assert len(classified_pages) == len(set(classified_pages))
    for relative in release["page_notebook_sources"]:
        source = (ROOT / relative).read_text(encoding="utf-8")
        assert ":page-jupyter: true" in source
        assert ":page-course-execution-profile: full" in source
        assert ":dynamic-blocks-strict:" in source
        assert "== Error estimation" in source
        assert "Mathematical insight" in source
    exception_ids = []
    for exception in [
        *contract["notebook_native_exceptions"],
        *contract["page_only_exceptions"],
    ]:
        exception_ids.append(exception["id"])
        assert all(
            str(exception[field]).strip()
            for field in ("reason", "owner", "environment", "maintenance_policy")
        )
        assert ":page-jupyter:" not in (ROOT / exception["page"]).read_text(encoding="utf-8")
    assert len(exception_ids) == len(set(exception_ids))
    assert {item["artifact"] for item in contract["notebook_native_exceptions"]} == set(
        release["notebooks"]
    )
    notebook = nbformat.read(ROOT / release["notebooks"][0], as_version=4)
    assert notebook.metadata["course"]["priority"] == "P2"
    assert notebook.metadata["course"]["assessed"] is False
    assert notebook.metadata["course"]["execution_profile"] == "full"
    for key in (
        "validation_record",
        "source_contract_record",
        "review_record",
        "downstream_record",
    ):
        assert (ROOT / release[key]).exists()
    policy = release["optional_failure_policy"]
    assert policy["required_notebook_profile"] == "fast"
    assert policy["extension_notebook_profile"] == "full"
    assert policy["required_environment_excludes_optional_extra"] is True
    core_paths = [
        *curriculum["foundation_release"]["pages"],
        *curriculum["foundation_release"]["notebook_sources"],
        *curriculum["analytical_release"]["pages"],
        *curriculum["analytical_release"]["notebooks"],
        *curriculum["analytical_release"]["notebook_sources"],
    ]
    assert all("/extensions/" not in path for path in core_paths)


def test_operational_release_preserves_human_approval_gates() -> None:
    curriculum = yaml.safe_load((ROOT / "curriculum.yml").read_text(encoding="utf-8"))
    release = curriculum["operational_release"]
    assert release["implementation_status"] == "complete"
    assert release["candidate_status"] == "pending_human_pilot_and_signoff"
    assert release["annual_release_status"] == "not_authorised"
    assert release["candidate_tag_pattern"] == "v0.9-pilot.N"
    assert release["annual_tag"] == "v1.0-2026"
    assert release["human_gates"]["colleague_reviewers"] >= 1
    assert release["human_gates"]["representative_students_or_alumni"] >= 2
    for group in ("public_pages", "governance_records", "operational_templates"):
        assert all((ROOT / path).exists() for path in release[group])
    for key in (
        "bundle_builder",
        "bundle_validator",
        "evidence_summariser",
        "release_workflow",
        "release_procedure",
        "changelog",
    ):
        assert (ROOT / release[key]).exists()


def test_release_qualification_is_deterministic_and_preserves_human_gates() -> None:
    curriculum = yaml.safe_load((ROOT / "curriculum.yml").read_text(encoding="utf-8"))
    release = curriculum["release_qualification"]
    assert release["implementation_status"] == "complete"
    assert release["source_of_truth_status"] == "unambiguous"
    assert release["technical_candidate_status"] == "qualified"
    assert release["human_release_status"] == "pending_pilot_and_named_signoff"
    assert release["repeated_clean_builds"] == 2
    assert release["retained_notebook_native_exceptions"] == ["EXT-JAX-NB"]
    for key in ("qualification_tool", "governance_record", "walkthrough_record"):
        assert (ROOT / release[key]).exists()
    automated = {
        key: value
        for key, value in release["required_reviews"].items()
        if key.startswith("automated_") or key == "technical_representative_walkthrough"
    }
    human = {
        key: value for key, value in release["required_reviews"].items() if key not in automated
    }
    assert automated and set(automated.values()) == {"pass"}
    assert human and set(human.values()) == {"pending"}
    assert all(not (ROOT / path).exists() for path in release["retired_paths"])
