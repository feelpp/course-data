#!/usr/bin/env python3
"""Validate curriculum, content metadata, snapshots, notebooks, privacy, and pins."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import tomllib
from pathlib import Path
from typing import Any

import nbformat
import yaml

ROOT = Path(__file__).resolve().parents[1]
UI_SHA256 = "d453b23caec62bfb33c05f2a661a2bf7303f996537ac206de95f176d9db9cd15"
PAGE_FIELDS = {
    "page-course-language",
    "page-course-concepts",
    "page-course-priority",
    "page-course-difficulty",
    "page-course-duration-minutes",
    "page-course-outcomes",
    "page-course-prerequisites",
    "page-course-assessed",
}
WORKED_EXAMPLE_PARTS = ["Context", "Method", "Implementation", "Results", "Conclusion"]
WORKED_EXAMPLE_IMPORTANCE = {
    "Context": "Essential (P0)",
    "Implementation": "Essential (P0)",
    "Results": "Essential (P0)",
    "Conclusion": "Essential (P0)",
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse_header(path: Path) -> dict[str, str]:
    attributes: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines()[1:]:
        match = re.match(r":([^:]+):\s*(.*)", line)
        if match:
            attributes[match.group(1)] = match.group(2)
        elif line.strip() and not line.startswith("//"):
            break
    return attributes


def split_values(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


def mapped_header_values(value: str, separator: str = "+") -> dict[str, list[str]]:
    mapping: dict[str, list[str]] = {}
    for item in value.split(";"):
        item = item.strip()
        if not item:
            continue
        key, marker, raw_values = item.partition("=")
        if not marker or not key.strip() or not raw_values.strip():
            raise ValueError(f"invalid mapped header entry: {item}")
        mapping[key.strip()] = [part.strip() for part in raw_values.split(separator)]
    return mapping


def validate_exercise_release(curriculum: dict[str, Any], errors: list[str]) -> None:
    release = curriculum["exercise_release"]
    assessments = {item["id"]: item for item in curriculum["assessments"]}
    rubric_ids = set(release["rubric"]["criteria"])
    specimens = release["public_specimens"]
    if release["implementation_status"] != "complete":
        errors.append("Public exercise implementation must be complete")
    if release["assessment_custodian_status"] != "pending_human_signoff":
        errors.append("Assessment-custodian sign-off must remain an explicit human gate")
    if {item["assessment_id"] for item in specimens} != set(assessments):
        errors.append("Every assessment must have exactly one public specimen contract")
    required_files = [
        release["conventions_page"],
        release["validation_record"],
        release["rubric"]["source"],
    ]
    for relative in required_files:
        if not (ROOT / relative).exists():
            errors.append(f"Public exercise artifact is missing: {relative}")
    if not release["forbidden_public_material"]:
        errors.append("Private assessment exclusions must be explicit")

    all_task_ids: list[str] = []
    for specimen in specimens:
        assessment_id = specimen["assessment_id"]
        assessment = assessments.get(assessment_id)
        if assessment is None:
            continue
        expected_source = "docs/course/modules/ROOT/pages/" + assessment["public_specification"]
        if specimen["source"] != expected_source:
            errors.append(f"{assessment_id}: specimen source disagrees with assessment inventory")
        if specimen["ai_mode"] != assessment["ai_mode"]:
            errors.append(f"{assessment_id}: specimen AI mode disagrees with assessment inventory")
        tasks = specimen["tasks"]
        task_ids = [task["id"] for task in tasks]
        all_task_ids.extend(task_ids)
        if len(task_ids) != len(set(task_ids)):
            errors.append(f"{assessment_id}: task identifiers are duplicated")
        if sum(task["points"] for task in tasks) != assessment["points"]:
            errors.append(f"{assessment_id}: task points do not equal assessment points")
        for task in tasks:
            if not set(task["priorities"]) <= set(assessment["required_priorities"]):
                errors.append(f"{task['id']}: optional content cannot be required")
            if not set(task["rubric_criteria"]) <= rubric_ids:
                errors.append(f"{task['id']}: unknown rubric criterion")

        source_path = ROOT / specimen["source"]
        if not source_path.exists():
            errors.append(f"{assessment_id}: public specimen source is missing")
            continue
        source = source_path.read_text(encoding="utf-8")
        attrs = parse_header(source_path)
        expected_attributes = {
            "page-course-assessment-id": assessment_id,
            "page-course-exercise-id": specimen["exercise_id"],
            "page-course-exercise-kind": specimen["kind"],
            "page-course-hint-policy": specimen["hint_policy"],
            "page-course-ai-mode": specimen["ai_mode"],
        }
        for name, expected in expected_attributes.items():
            if attrs.get(name) != expected:
                errors.append(f"{assessment_id}: {name} disagrees with curriculum")
        if "page-jupyter" not in attrs:
            errors.append(f"{assessment_id}: public specimen must generate a notebook")
        if split_values(attrs.get("page-course-task-ids", "")) != task_ids:
            errors.append(f"{assessment_id}: page task IDs disagree with curriculum")
        if (
            split_values(attrs.get("page-course-allowed-resources", ""))
            != specimen["allowed_resources"]
        ):
            errors.append(f"{assessment_id}: allowed resources disagree with curriculum")
        if (
            split_values(attrs.get("page-course-submission-evidence", ""))
            != specimen["submission_evidence"]
        ):
            errors.append(f"{assessment_id}: submission evidence disagrees with curriculum")
        declared_rubric = set(split_values(attrs.get("page-course-rubric-criteria", "")))
        expected_rubric = {criterion for task in tasks for criterion in task["rubric_criteria"]}
        if declared_rubric != expected_rubric:
            errors.append(f"{assessment_id}: rubric mapping disagrees with task contracts")
        try:
            priorities = mapped_header_values(attrs.get("page-course-task-priorities", ""))
            points = mapped_header_values(attrs.get("page-course-task-points", ""), separator=",")
        except ValueError as error:
            errors.append(f"{assessment_id}: {error}")
            continue
        expected_priorities = {task["id"]: task["priorities"] for task in tasks}
        expected_points = {task["id"]: [str(task["points"])] for task in tasks}
        if priorities != expected_priorities:
            errors.append(f"{assessment_id}: task importance mapping disagrees with curriculum")
        if points != expected_points:
            errors.append(f"{assessment_id}: task point mapping disagrees with curriculum")
        for task in tasks:
            if source.count(task["id"]) < 2:
                errors.append(f"{task['id']}: task ID must occur in metadata and visible prompt")
        private_markers = ("[solution]", ".Solution", "role=solution", "instructor-only")
        if any(marker in source for marker in private_markers):
            errors.append(f"{assessment_id}: public specimen contains a private-content marker")

    if len(all_task_ids) != len(set(all_task_ids)):
        errors.append("Public exercise task identifiers must be globally unique")


def validate_worked_example_release(curriculum: dict[str, Any], errors: list[str]) -> None:
    release = curriculum["worked_example_release"]
    expected_pages = {
        *curriculum["foundation_release"]["pages"],
        *curriculum["analytical_release"]["pages"],
    }
    expected_notebooks = {
        *curriculum["foundation_release"]["notebook_sources"],
        *curriculum["analytical_release"]["notebook_sources"],
    }
    pages = set(release["pages"])
    notebooks = set(release["notebook_sources"])
    page_only = set(release["page_only"])

    if release["implementation_status"] != "complete":
        errors.append("Worked-example implementation must be complete")
    if release["human_review_status"] != "pending_instructor_and_real_student_review":
        errors.append("Worked-example human review must remain an explicit release gate")
    if release["required_structure"] != WORKED_EXAMPLE_PARTS:
        errors.append(
            "Worked-example structure must be Context–Method–Implementation–Results–Conclusion"
        )
    if pages != expected_pages:
        errors.append("Worked-example inventory disagrees with foundation and analytical releases")
    if notebooks != expected_notebooks:
        errors.append("Worked-example notebook inventory disagrees with canonical notebook sources")
    if page_only != pages - notebooks:
        errors.append("Worked-example page-only inventory is inconsistent")
    for relative in [
        *release["pages"],
        release["authoring_contract"],
        release["validation_record"],
    ]:
        if not (ROOT / relative).exists():
            errors.append(f"Worked-example artifact is missing: {relative}")


def validate_blueprint(curriculum: dict[str, Any], errors: list[str]) -> None:
    concepts_by_id = {item["id"]: item for item in curriculum["concepts"]}
    outcomes_by_id = {item["id"]: item for item in curriculum["learning_outcomes"]}
    assessments_by_id = {item["id"]: item for item in curriculum["assessments"]}
    activities_by_id = {item["id"]: item for item in curriculum["learning_activities"]}
    dataset_ids = {item["id"] for item in curriculum["datasets"].values() if isinstance(item, dict)}

    if len(assessments_by_id) != len(curriculum["assessments"]):
        errors.append("Assessment identifiers are not unique")
    if len(activities_by_id) != len(curriculum["learning_activities"]):
        errors.append("Learning-activity identifiers are not unique")

    concept_ids = set(concepts_by_id)
    outcome_ids = set(outcomes_by_id)
    assessment_ids = set(assessments_by_id)
    activity_ids = set(activities_by_id)
    required_concepts = {
        item["id"] for item in curriculum["concepts"] if item["priority"] in {"P0", "P1"}
    }
    required_outcomes = {
        item["id"] for item in curriculum["learning_outcomes"] if item["priority"] in {"P0", "P1"}
    }

    scheduled_concepts: set[str] = set()
    scheduled_outcomes: set[str] = set()
    practised_concepts: set[str] = set()
    practised_outcomes: set[str] = set()
    first_taught: dict[str, int] = {}

    expected_blocks = list(range(1, curriculum["course"]["delivery_blocks"] + 1))
    actual_blocks = [item["block"] for item in curriculum["schedule"]]
    if actual_blocks != expected_blocks:
        errors.append(f"Schedule blocks must be sequential: expected {expected_blocks}")

    for block in curriculum["schedule"]:
        number = block["block"]
        block_concepts = set(block["concepts"])
        block_optional = set(block.get("optional_concepts", []))
        block_outcomes = set(block["outcomes"])
        unknown_concepts = (block_concepts | block_optional) - concept_ids
        unknown_outcomes = (block_outcomes | set(block.get("optional_outcomes", []))) - outcome_ids
        if unknown_concepts:
            errors.append(f"Block {number}: unknown concepts {sorted(unknown_concepts)}")
        if unknown_outcomes:
            errors.append(f"Block {number}: unknown outcomes {sorted(unknown_outcomes)}")
        if set(block["datasets"]) - dataset_ids:
            errors.append(
                f"Block {number}: unknown datasets {sorted(set(block['datasets']) - dataset_ids)}"
            )
        if set(block["activities"]) - activity_ids:
            unknown_activities = sorted(set(block["activities"]) - activity_ids)
            errors.append(f"Block {number}: unknown activities {unknown_activities}")
        if set(block["assessment_evidence"]) - assessment_ids:
            errors.append(f"Block {number}: unknown assessment evidence")
        for prerequisite in block["prerequisites"]:
            if prerequisite not in concept_ids:
                errors.append(f"Block {number}: unknown prerequisite {prerequisite}")
            elif first_taught.get(prerequisite, number) >= number:
                errors.append(f"Block {number}: prerequisite {prerequisite} is not taught earlier")
        declared_outcomes = {
            outcome
            for concept in block_concepts
            if concept in concepts_by_id
            for outcome in concepts_by_id[concept]["outcomes"]
        }
        if declared_outcomes - block_outcomes:
            missing_outcomes = sorted(declared_outcomes - block_outcomes)
            errors.append(f"Block {number}: missing concept outcomes {missing_outcomes}")
        for concept in block_concepts | block_optional:
            first_taught.setdefault(concept, number)
        scheduled_concepts.update(block_concepts)
        scheduled_outcomes.update(block_outcomes)

    for activity in curriculum["learning_activities"]:
        activity_concepts = set(activity["concepts"])
        activity_optional = set(activity.get("optional_concepts", []))
        activity_outcomes = set(activity["outcomes"])
        if (activity_concepts | activity_optional) - concept_ids:
            errors.append(f"{activity['id']}: unknown concept reference")
        if (activity_outcomes | set(activity.get("optional_outcomes", []))) - outcome_ids:
            errors.append(f"{activity['id']}: unknown outcome reference")
        if set(activity["datasets"]) - dataset_ids:
            errors.append(f"{activity['id']}: unknown dataset reference")
        if activity["duration_minutes"] <= 0 or not activity["acceptance_criteria"]:
            errors.append(f"{activity['id']}: duration and acceptance criteria are required")
        practised_concepts.update(activity_concepts)
        practised_outcomes.update(activity_outcomes)

    assessed_outcomes: set[str] = set()
    for assessment in curriculum["assessments"]:
        assessment_outcomes = set(assessment["outcomes"])
        assessed_outcomes.update(assessment_outcomes)
        if assessment_outcomes - outcome_ids:
            errors.append(f"{assessment['id']}: unknown outcome reference")
        if set(assessment["required_priorities"]) - {"P0", "P1"}:
            errors.append(f"{assessment['id']}: required content must be P0 or P1")
        specification = ROOT / "docs/course/modules/ROOT/pages" / assessment["public_specification"]
        if not specification.exists():
            errors.append(f"{assessment['id']}: public specification is missing")

    for concept in curriculum["concepts"]:
        concept_assessments = set(concept["assessed_in"])
        if concept_assessments - assessment_ids:
            errors.append(f"{concept['id']}: unknown assessment reference")
        if concept["priority"] in {"P2", "P3"} and concept_assessments:
            errors.append(f"{concept['id']}: optional or deferred content cannot be required")

    for assessment_id, assessment in assessments_by_id.items():
        mapped_outcomes = {
            outcome
            for concept in curriculum["concepts"]
            if assessment_id in concept["assessed_in"]
            for outcome in concept["outcomes"]
        }
        if mapped_outcomes != set(assessment["outcomes"]):
            errors.append(f"{assessment_id}: outcome list disagrees with concept assessment map")

    coverage = {
        "taught concepts": required_concepts - scheduled_concepts,
        "practised concepts": required_concepts - practised_concepts,
        "assessed concepts": {
            item["id"]
            for item in curriculum["concepts"]
            if item["priority"] in {"P0", "P1"} and not item["assessed_in"]
        },
        "taught outcomes": required_outcomes - scheduled_outcomes,
        "practised outcomes": required_outcomes - practised_outcomes,
        "assessed outcomes": required_outcomes - assessed_outcomes,
    }
    for label, missing in coverage.items():
        if missing:
            errors.append(f"Blueprint has uncovered {label}: {sorted(missing)}")

    diagnostic = curriculum["diagnostic"]
    routes = diagnostic["routes"]
    if not 0 < diagnostic["mastery_threshold_percent"] <= 100:
        errors.append("Diagnostic mastery threshold must be a percentage")
    for domain in diagnostic["domains"]:
        if set(domain["concepts"]) - concept_ids:
            errors.append(f"{domain['id']}: unknown diagnostic concept")
        if domain["route"] not in routes:
            errors.append(f"{domain['id']}: unknown remediation route")

    contract = curriculum["execution_contract"]
    if contract["reference_environment"]["memory_gib"] < contract["limits"]["peak_memory_gib"]:
        errors.append("Peak memory limit exceeds the reference environment")
    if any(value <= 0 for value in contract["limits"].values()):
        errors.append("Execution limits must be positive")

    validate_exercise_release(curriculum, errors)

    release = curriculum["foundation_release"]
    release_paths = [
        *release["pages"],
        *release["templates"],
        *release["teaching_data"],
        release["public_specimen"],
    ]
    if len(release_paths) != len(set(release_paths)):
        errors.append("Foundation release inventory contains duplicate paths")
    for relative in release_paths:
        if not (ROOT / relative).exists():
            errors.append(f"Foundation release artifact is missing: {relative}")
    for relative in release["pages"]:
        page = ROOT / relative
        if not page.exists():
            continue
        if parse_header(page).get("page-course-priority") != "P0":
            errors.append(f"Foundation page must be P0: {relative}")
        source = page.read_text(encoding="utf-8")
        if "stem:[" not in source and "[stem]" not in source:
            errors.append(f"Foundation page lacks mathematical notation: {relative}")
    mathematical_background = ROOT / release["pages"][0]
    if mathematical_background.exists():
        source = mathematical_background.read_text(encoding="utf-8")
        if source.count("stem:[") + source.count("[stem]") < 20:
            errors.append("Mathematical background lacks sufficient worked notation")
        for fragment in (".Definition:", ".Proposition:", "== Error estimation", ".Exercise:"):
            if fragment not in source:
                errors.append(f"Mathematical background lacks required element: {fragment}")
    for relative in release["notebook_sources"]:
        path = ROOT / relative
        if not path.exists():
            continue
        attrs = parse_header(path)
        if "page-jupyter" not in attrs:
            errors.append(f"Foundation notebook source must enable page-jupyter: {relative}")
        if (
            attrs.get("page-course-priority") != "P0"
            or attrs.get("page-course-execution-profile") != "fast"
        ):
            errors.append(f"Foundation notebook source must be P0 and fast: {relative}")

    analytical = curriculum["analytical_release"]
    analytical_paths = [
        *analytical["pages"],
        *analytical["notebooks"],
        *analytical["teaching_data"],
        analytical["project_specification"],
        analytical["final_specification"],
    ]
    for relative in analytical_paths:
        if not (ROOT / relative).exists():
            errors.append(f"Analytical release artifact is missing: {relative}")
    expected_p1 = {item["id"] for item in curriculum["concepts"] if item["priority"] == "P1"}
    declared_p1 = set(analytical["concepts"])
    if declared_p1 != expected_p1:
        errors.append(f"Analytical concept inventory mismatch: {sorted(expected_p1 ^ declared_p1)}")
    page_p1: set[str] = set()
    for relative in analytical["pages"]:
        path = ROOT / relative
        if not path.exists():
            continue
        attrs = parse_header(path)
        if attrs.get("page-course-priority") != "P1":
            errors.append(f"Analytical page must be P1: {relative}")
        source = path.read_text(encoding="utf-8")
        if "=== Implementation" not in source or "== Independent transfer" not in source:
            errors.append(f"Analytical page lacks solved executable/transfer evidence: {relative}")
        required_learning_elements = (
            ".Definition:",
            "[stem]",
            "== Error estimation",
            "== Worked example",
            "== Exercises",
            ".Exercise:",
        )
        missing_elements = [
            element for element in required_learning_elements if element not in source
        ]
        if missing_elements:
            errors.append(
                f"Analytical page lacks learn-from-page elements {missing_elements}: {relative}"
            )
        if source.count("stem:[") + source.count("[stem]") < 8:
            errors.append(f"Analytical page has insufficient mathematical development: {relative}")
        page_p1.update(set(split_values(attrs.get("page-course-concepts", ""))) & expected_p1)
    notebook_p1: set[str] = set()
    for relative in analytical["notebooks"]:
        path = ROOT / relative
        if not path.exists():
            continue
        course = nbformat.read(path, as_version=4).metadata.get("course", {})
        if course.get("priority") != "P1" or course.get("execution_profile") != "full":
            errors.append(f"Analytical notebook must be P1 and full: {relative}")
        notebook_p1.update(set(course.get("concept_ids", [])) & expected_p1)
    for relative in analytical["notebook_sources"]:
        path = ROOT / relative
        if not path.exists():
            continue
        attrs = parse_header(path)
        if "page-jupyter" not in attrs:
            errors.append(f"Analytical notebook source must enable page-jupyter: {relative}")
        if (
            attrs.get("page-course-priority") != "P1"
            or attrs.get("page-course-execution-profile") != "full"
        ):
            errors.append(f"Analytical notebook source must be P1 and full: {relative}")
        notebook_p1.update(set(split_values(attrs.get("page-course-concepts", ""))) & expected_p1)
    if page_p1 != expected_p1:
        errors.append(f"P1 page coverage gap: {sorted(expected_p1 - page_p1)}")
    if notebook_p1 != expected_p1:
        errors.append(f"P1 notebook coverage gap: {sorted(expected_p1 - notebook_p1)}")
    question_ids = analytical["question_bank_ids"]
    if len(question_ids) != len(set(question_ids)) or len(question_ids) < len(analytical["pages"]):
        errors.append("Analytical question-bank identifiers are incomplete or duplicated")

    enrichment = curriculum["enrichment_release"]
    enrichment_paths = [
        *enrichment["pages"],
        *enrichment["notebooks"],
        enrichment["validation_record"],
        enrichment["source_contract_record"],
        enrichment["review_record"],
        enrichment["downstream_record"],
    ]
    for relative in enrichment_paths:
        if not (ROOT / relative).exists():
            errors.append(f"Enrichment artifact is missing: {relative}")
    expected_p2 = {item["id"] for item in curriculum["concepts"] if item["priority"] == "P2"}
    if set(enrichment["concepts"]) != expected_p2:
        errors.append("Enrichment concept inventory must equal the complete P2 concept set")
    if (
        enrichment["required_contact_hours"] != 0
        or enrichment["assessment_eligible"]
        or not enrichment["removable_without_core_loss"]
    ):
        errors.append("Enrichment must remain optional and removable from the core contract")
    for relative in enrichment["pages"]:
        path = ROOT / relative
        if not path.exists():
            continue
        attrs = parse_header(path)
        if attrs.get("page-course-priority") != "P2":
            errors.append(f"Enrichment page must be P2: {relative}")
        if attrs.get("page-course-assessed") != "no":
            errors.append(f"Enrichment page cannot be assessed: {relative}")
    source_contract = enrichment["source_contract"]
    page_notebook_sources = set(enrichment["page_notebook_sources"])
    if page_notebook_sources != set(source_contract["asciidoc_notebook"]):
        errors.append("Enrichment AsciiDoc/notebook inventory disagrees with page sources")
    notebook_native = source_contract["notebook_native_exceptions"]
    page_only = source_contract["page_only_exceptions"]
    classified_pages = (
        page_notebook_sources
        | {item["page"] for item in notebook_native}
        | {item["page"] for item in page_only}
    )
    if classified_pages != set(enrichment["pages"]):
        errors.append("Every enrichment page must have exactly one declared source mode")
    classification_count = [
        *page_notebook_sources,
        *(item["page"] for item in notebook_native),
        *(item["page"] for item in page_only),
    ]
    if len(classification_count) != len(set(classification_count)):
        errors.append("Enrichment source-mode classifications overlap")
    exception_ids: list[str] = []
    for exception in [*notebook_native, *page_only]:
        required_fields = {
            "id",
            "page",
            "reason",
            "owner",
            "environment",
            "maintenance_policy",
        }
        if missing_fields := required_fields - set(exception):
            errors.append(
                f"Enrichment exception is missing fields {sorted(missing_fields)}: "
                f"{exception.get('id', '<unknown>')}"
            )
        exception_ids.append(exception.get("id", ""))
        if any(not str(exception.get(field, "")).strip() for field in required_fields):
            errors.append(
                f"Enrichment exception has an empty required field: "
                f"{exception.get('id', '<unknown>')}"
            )
        exception_page = ROOT / exception["page"]
        if exception_page.exists() and "page-jupyter" in parse_header(exception_page):
            errors.append(f"Enrichment exception cannot enable page-jupyter: {exception['page']}")
    if len(exception_ids) != len(set(exception_ids)) or "" in exception_ids:
        errors.append("Enrichment exception identifiers must be unique and non-empty")
    native_artifacts = {item.get("artifact") for item in notebook_native}
    if native_artifacts != set(enrichment["notebooks"]):
        errors.append("Notebook-native exception artifacts disagree with enrichment notebooks")
    for relative in page_notebook_sources:
        path = ROOT / relative
        if not path.exists():
            continue
        attrs = parse_header(path)
        required_jupyter_attrs = {
            "page-jupyter",
            "dynamic-blocks",
            "dynamic-blocks-strict",
        }
        if not required_jupyter_attrs <= set(attrs):
            errors.append(f"Generated enrichment page lacks strict Jupyter metadata: {relative}")
        if attrs.get("page-course-execution-profile") != "full":
            errors.append(f"Generated enrichment notebook must use the full profile: {relative}")
    for relative in enrichment["notebooks"]:
        path = ROOT / relative
        if not path.exists():
            continue
        course = nbformat.read(path, as_version=4).metadata.get("course", {})
        if (
            course.get("priority") != "P2"
            or course.get("assessed") is not False
            or course.get("execution_profile") != "full"
        ):
            errors.append(f"Enrichment notebook must be optional P2 and full CPU: {relative}")
    project = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    extra_name = enrichment["dependency_extra"]
    actual_extra = set(project["project"]["optional-dependencies"].get(extra_name, []))
    expected_extra = {
        f"{name}=={version}" for name, version in enrichment["pinned_optional_dependencies"].items()
    }
    if actual_extra != expected_extra:
        errors.append("Enrichment dependency extra disagrees with the canonical pin inventory")
    optional_policy = enrichment["optional_failure_policy"]
    if (
        optional_policy["required_notebook_profile"] != "fast"
        or optional_policy["extension_notebook_profile"] != "full"
        or not optional_policy["required_environment_excludes_optional_extra"]
    ):
        errors.append("Enrichment optional-failure policy no longer isolates required completion")
    optional_imports = tuple(optional_policy["optional_runtime_imports_forbidden_in_p0_p1"])
    core_sources = [
        *curriculum["foundation_release"]["notebook_sources"],
        *curriculum["analytical_release"]["notebook_sources"],
    ]
    for relative in core_sources:
        source = (ROOT / relative).read_text(encoding="utf-8")
        for package in optional_imports:
            if re.search(rf"(?m)^\s*(?:from|import)\s+{re.escape(package)}\b", source):
                errors.append(f"Optional runtime {package} imported by P0/P1 source: {relative}")

    operational = curriculum["operational_release"]
    operational_paths = [
        *operational["public_pages"],
        *operational["governance_records"],
        *operational["operational_templates"],
        operational["bundle_builder"],
        operational["bundle_validator"],
        operational["evidence_summariser"],
        operational["release_workflow"],
        operational["release_procedure"],
        operational["changelog"],
    ]
    for relative in operational_paths:
        if not (ROOT / relative).exists():
            errors.append(f"Operational release artifact is missing: {relative}")
    if operational["implementation_status"] != "complete":
        errors.append("Operational release tooling must be complete")
    if operational["candidate_status"] != "pending_human_pilot_and_signoff":
        errors.append("Candidate status must preserve the pending human gate")
    if operational["annual_release_status"] != "not_authorised":
        errors.append("Annual release cannot be authorised by repository automation")
    human_gates = operational["human_gates"]
    if human_gates["colleague_reviewers"] < 1:
        errors.append("At least one colleague reviewer is required")
    if human_gates["representative_students_or_alumni"] < 2:
        errors.append("At least two representative learners are required")
    if not all(
        human_gates[key]
        for key in (
            "academic_signoff_required",
            "accessibility_signoff_required",
            "data_steward_signoff_required",
            "assessment_custodian_signoff_required",
        )
    ):
        errors.append("Every named human release sign-off must remain required")

    qualification = curriculum["release_qualification"]
    qualification_paths = [
        qualification["qualification_tool"],
        qualification["governance_record"],
        qualification["walkthrough_record"],
    ]
    for relative in qualification_paths:
        if not (ROOT / relative).exists():
            errors.append(f"Release-qualification artifact is missing: {relative}")
    if (
        qualification["implementation_status"] != "complete"
        or qualification["source_of_truth_status"] != "unambiguous"
        or qualification["technical_candidate_status"] != "qualified"
    ):
        errors.append("Release qualification must preserve the completed technical contract")
    if qualification["human_release_status"] != "pending_pilot_and_named_signoff":
        errors.append("Release qualification cannot bypass the pending human gates")
    if qualification["repeated_clean_builds"] != 2:
        errors.append("Release qualification must compare exactly two clean builds")
    reviews = qualification["required_reviews"]
    automated_reviews = {
        "automated_accessibility",
        "automated_offline_runtime",
        "automated_english_contract",
        "automated_mathematics_contract",
        "technical_representative_walkthrough",
    }
    human_reviews = set(reviews) - automated_reviews
    if any(reviews[name] != "pass" for name in automated_reviews):
        errors.append("Every automated release review must pass")
    if any(reviews[name] != "pending" for name in human_reviews):
        errors.append("Human release reviews must remain pending until named sign-off")
    native_ids = {item["id"] for item in notebook_native}
    if set(qualification["retained_notebook_native_exceptions"]) != native_ids:
        errors.append("Residual notebook-native exception inventory disagrees with enrichment")
    for relative in qualification["retired_paths"]:
        if (ROOT / relative).exists():
            errors.append(f"Retired notebook path returned: {relative}")
    jax_exception = next(
        (item for item in notebook_native if item["id"] == "EXT-JAX-NB"),
        None,
    )
    if jax_exception is None or any(
        not str(jax_exception.get(field, "")).strip()
        for field in ("page_authority", "artifact_authority", "parity_contract")
    ):
        errors.append("JAX exception must divide page and artifact authority explicitly")
    package_json = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
    package_dependencies = package_json["dependencies"]
    expected_packages = {
        "asciidoctor-jupyter": "0.7.0",
        "katex": "0.18.4",
        "@feelpp/antora-extensions": (
            "file:vendor/npm/feelpp-antora-extensions-1.0.0-rc.7-dev.3.tgz"
        ),
        "@feelpp/asciidoctor-extensions": (
            "file:vendor/npm/feelpp-asciidoctor-extensions-1.0.0-rc.18-dev.2.tgz"
        ),
    }
    for name, version in expected_packages.items():
        if package_dependencies.get(name) != version:
            errors.append(f"Release dependency pin disagrees with qualification: {name}")
    scripts = package_json["scripts"]
    if scripts.get("notebooks:source") != "npm run notebooks:native-source":
        errors.append("Notebook source command must target only declared native exceptions")
    if scripts.get("release:qualify") != (
        "npm run setup:release && uv run python -m tools.qualify_release"
    ):
        errors.append("Release qualification command disagrees with curriculum")
    runtime_partials = [
        ROOT / "docs/course/supplemental-ui/partials/head-meta.hbs",
        ROOT / "docs/course/supplemental-ui/partials/head-styles.hbs",
    ]
    for path in runtime_partials:
        source = path.read_text(encoding="utf-8")
        if re.search(r"(?:src|href)=[\"'](?:https?:)?//", source):
            errors.append(f"External runtime asset is forbidden: {path.relative_to(ROOT)}")


def validate_contact_time(curriculum: dict[str, Any], errors: list[str]) -> None:
    """Count each classroom slot once, even when an activity is a control."""
    activity_minutes: dict[str, int] = {}
    assessment_slots: dict[str, list[tuple[int, int]]] = {}
    for block in curriculum["schedule"]:
        number = block["block"]
        plan = block.get("contact_plan", [])
        if not plan or any(
            type(slot.get("minutes")) is not int or slot["minutes"] <= 0 for slot in plan
        ):
            errors.append(f"Block {number}: positive contact-time allocations are required")
            continue
        if sum(slot["minutes"] for slot in plan) != 120:
            errors.append(f"Block {number}: contact-time allocation must total 120 minutes")
        used_activities = set()
        for slot in plan:
            if activity := slot.get("activity"):
                used_activities.add(activity)
                activity_minutes[activity] = activity_minutes.get(activity, 0) + slot["minutes"]
            if assessment := slot.get("assessment"):
                assessment_slots.setdefault(assessment, []).append((number, slot["minutes"]))
        if used_activities != set(block["activities"]):
            errors.append(f"Block {number}: activity inventory disagrees with contact slots")
    for activity in curriculum["learning_activities"]:
        if activity_minutes.get(activity["id"], 0) != activity["duration_minutes"]:
            errors.append(f"{activity['id']}: assigned minutes disagree with activity duration")
    for assessment in curriculum["assessments"]:
        if "contact_block" in assessment and "duration_minutes" in assessment:
            expected = [(assessment["contact_block"], assessment["duration_minutes"])]
            if assessment_slots.get(assessment["id"]) != expected:
                errors.append(
                    f"{assessment['id']}: timed control allocation disagrees with contract"
                )


def load_curriculum(errors: list[str]) -> tuple[dict[str, Any], set[str], set[str]]:
    curriculum = yaml.safe_load((ROOT / "curriculum.yml").read_text(encoding="utf-8"))
    weights = sum(item["weight_percent"] for item in curriculum["assessments"])
    if weights != 100:
        errors.append(f"Assessment weights total {weights}, expected 100")
    blocks = curriculum["schedule"]
    hours = len(blocks) * curriculum["course"]["block_duration_hours"]
    if hours != curriculum["course"]["contact_hours"]:
        errors.append(f"Schedule contains {hours} hours, expected contact-hour total")
    concepts = {item["id"] for item in curriculum["concepts"]}
    outcomes = {item["id"] for item in curriculum["learning_outcomes"]}
    if len(concepts) != len(curriculum["concepts"]):
        errors.append("Curriculum concept identifiers are not unique")
    validate_blueprint(curriculum, errors)
    validate_contact_time(curriculum, errors)
    validate_worked_example_release(curriculum, errors)
    return curriculum, concepts, outcomes


def validate_pages(concepts: set[str], outcomes: set[str], errors: list[str]) -> None:
    for path in sorted((ROOT / "docs/course/modules").rglob("*.adoc")):
        if path.name == "nav.adoc":
            continue
        attrs = parse_header(path)
        missing = sorted(PAGE_FIELDS - set(attrs))
        if missing:
            errors.append(f"{path.relative_to(ROOT)}: missing page metadata {missing}")
            continue
        if attrs["page-course-language"] != "en":
            errors.append(f"{path.relative_to(ROOT)}: language must be en")
        unknown_concepts = set(split_values(attrs["page-course-concepts"])) - concepts
        unknown_outcomes = set(split_values(attrs["page-course-outcomes"])) - outcomes
        if unknown_concepts:
            errors.append(f"{path.relative_to(ROOT)}: unknown concepts {sorted(unknown_concepts)}")
        if unknown_outcomes:
            errors.append(f"{path.relative_to(ROOT)}: unknown outcomes {sorted(unknown_outcomes)}")
        if attrs["page-course-priority"] not in {"P0", "P1", "P2", "P3"}:
            errors.append(f"{path.relative_to(ROOT)}: invalid priority")
        if attrs["page-course-difficulty"] not in {"D1", "D2", "D3"}:
            errors.append(f"{path.relative_to(ROOT)}: invalid difficulty")
        if attrs["page-course-assessed"] not in {"yes", "no"}:
            errors.append(f"{path.relative_to(ROOT)}: assessed must be yes or no")

        # Required teaching pages must contain a complete solved example, not a
        # labelled observation followed by evidence deferred to a laboratory.
        if attrs["page-course-priority"] in {"P0", "P1"} and path.parent.name in {
            "foundations",
            "analytical",
        }:
            source = path.read_text(encoding="utf-8")
            worked_match = re.search(r"(?ms)^== Worked example[^\n]*\n(.*?)(?=^== |\Z)", source)
            if not worked_match:
                errors.append(f"{path.relative_to(ROOT)}: required page lacks a worked example")
                continue
            worked = worked_match.group(1)
            headings = re.findall(r"(?m)^=== ([^\n]+)$", worked)
            if headings != WORKED_EXAMPLE_PARTS:
                errors.append(
                    f"{path.relative_to(ROOT)}: worked example stages must be exactly "
                    f"{'–'.join(WORKED_EXAMPLE_PARTS)}, found {headings}"
                )
            semantic_sections = re.findall(
                r"(?m)^\[\.worked-example-([a-z]+)#(worked-[a-z0-9-]+)\]\n"
                r"=== ([A-Za-z]+)$",
                worked,
            )
            expected_roles = [part.lower() for part in WORKED_EXAMPLE_PARTS]
            actual_roles = [role for role, _, _ in semantic_sections]
            if actual_roles != expected_roles:
                errors.append(
                    f"{path.relative_to(ROOT)}: worked example semantic roles are incomplete "
                    f"or out of order: {actual_roles}"
                )
            semantic_ids = [identifier for _, identifier, _ in semantic_sections]
            if len(semantic_ids) != len(set(semantic_ids)) or any(
                not identifier.endswith(f"-{role}") for role, identifier, _ in semantic_sections
            ):
                errors.append(f"{path.relative_to(ROOT)}: worked example IDs are unstable")

            section_bodies: dict[str, str] = {}
            for part in WORKED_EXAMPLE_PARTS:
                match = re.search(rf"(?ms)^=== {part}\n(.*?)(?=^=== |\Z)", worked)
                section_bodies[part] = match.group(1) if match else ""
            for part, required_importance in WORKED_EXAMPLE_IMPORTANCE.items():
                if f"*Importance:* {required_importance}" not in section_bodies[part]:
                    errors.append(
                        f"{path.relative_to(ROOT)}: {part} must be visibly {required_importance}"
                    )
            method = section_bodies["Method"]
            if not any(
                f"*Importance:* {importance}" in method
                for importance in ("Essential (P0)", "Core (P1)")
            ):
                errors.append(
                    f"{path.relative_to(ROOT)}: Method must have a visible P0/P1 importance"
                )
            if (
                ".Mathematical insight —" not in method
                or "[IMPORTANT]" not in method
                or not any(marker in method for marker in ("*Essential (P0).*", "*Core (P1).*"))
            ):
                errors.append(
                    f"{path.relative_to(ROOT)}: Method lacks a prioritised Mathematical insight"
                )
            if "stem:[" not in worked and "[stem]" not in worked:
                errors.append(
                    f"{path.relative_to(ROOT)}: worked example lacks a checkable calculation"
                )
            if "output=table" not in worked and 'options="header"' not in worked:
                errors.append(
                    f"{path.relative_to(ROOT)}: worked example lacks a bounded result table"
                )
            if "page-jupyter" in attrs and "[%dynamic" not in worked:
                errors.append(
                    f"{path.relative_to(ROOT)}: notebook-backed worked example lacks "
                    "executable evidence"
                )
            if attrs["page-course-priority"] == "P1" and (
                "output=table" not in worked or "output=matplotlib" not in worked
            ):
                errors.append(
                    f"{path.relative_to(ROOT)}: P1 worked example needs a result table "
                    "and diagnostic figure"
                )
            conclusion = section_bodies["Conclusion"].lower()
            if not any(
                marker in conclusion
                for marker in (
                    "limit",
                    "remain",
                    "does not",
                    "do not",
                    "outside",
                    "uncertainty",
                    "shift",
                )
            ):
                errors.append(
                    f"{path.relative_to(ROOT)}: Conclusion lacks residual error or limitation"
                )


def validate_executable_pages(errors: list[str]) -> None:
    required_attributes = {
        "dynamic-blocks",
        "dynamic-blocks-strict",
        "dynamic-blocks-timeout-seconds",
        "dynamic-blocks-max-output-bytes",
        "dynamic-python-interpreter",
        "dynamic-python-isolate-user-site",
        "page-jupyter",
    }
    pages_root = ROOT / "docs/course/modules"
    for path in sorted(pages_root.rglob("*.adoc")):
        source = path.read_text(encoding="utf-8")
        lines = source.splitlines()
        dynamic_lines = [
            (line_number, line)
            for line_number, line in enumerate(lines, start=1)
            if line.startswith("[") and "%dynamic" in line and ",python" in line
        ]
        if not dynamic_lines:
            continue
        if re.search(r"""Path\(["']xref:attachment\$datasets/""", source):
            errors.append(
                f"{path.relative_to(ROOT)}: executable code cannot depend on generated site data"
            )
        attrs = parse_header(path)
        missing = sorted(required_attributes - set(attrs))
        if missing:
            relative = path.relative_to(ROOT)
            errors.append(f"{relative}: executable page is missing contract attributes {missing}")
            continue
        if attrs["dynamic-python-interpreter"] != "python3":
            errors.append(f"{path.relative_to(ROOT)}: executable page must use python3")
        try:
            timeout = int(attrs["dynamic-blocks-timeout-seconds"])
            if not 1 <= timeout <= 120:
                raise ValueError
        except ValueError:
            errors.append(
                f"{path.relative_to(ROOT)}: dynamic timeout must be an integer from 1 to 120"
            )
        try:
            output_limit = int(attrs["dynamic-blocks-max-output-bytes"])
            if not 1024 <= output_limit <= 10 * 1024 * 1024:
                raise ValueError
        except ValueError:
            errors.append(
                f"{path.relative_to(ROOT)}: dynamic output limit must be from 1024 to 10485760"
            )
        for line_number, line in dynamic_lines:
            previous_line = lines[line_number - 2].strip() if line_number > 1 else ""
            has_explicit_id = "#" in line or bool(
                re.fullmatch(r"\[#[A-Za-z0-9_.:-]+\]", previous_line)
            )
            if "fail-on-error" not in line:
                relative = path.relative_to(ROOT)
                errors.append(
                    f"{relative}:{line_number}: required dynamic block must fail on error"
                )
            if "output=matplotlib" in line:
                required = {
                    "figure-alt=": "figure-alt",
                    "figure-caption=": "figure-caption",
                    "result-interpretation=": "result-interpretation",
                }
                if not has_explicit_id:
                    errors.append(
                        f"{path.relative_to(ROOT)}:{line_number}: "
                        "Matplotlib output requires an explicit block ID"
                    )
                for marker, meaning in required.items():
                    if marker not in line:
                        errors.append(
                            f"{path.relative_to(ROOT)}:{line_number}: "
                            f"Matplotlib output requires {meaning}"
                        )
            if "output=table" in line:
                required = {
                    "table-caption=": "table-caption",
                    "table-description=": "table-description",
                }
                if not has_explicit_id:
                    errors.append(
                        f"{path.relative_to(ROOT)}:{line_number}: "
                        "table output requires an explicit block ID"
                    )
                for marker, meaning in required.items():
                    if marker not in line:
                        errors.append(
                            f"{path.relative_to(ROOT)}:{line_number}: "
                            f"table output requires {meaning}"
                        )

    package = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
    site_command = package.get("scripts", {}).get("site", "")
    if site_command != (
        "uv run -- ./node_modules/.bin/antora --stacktrace site.yml && node tools/sanitise_site.mjs"
    ):
        errors.append(
            "The Antora site command must use locked dependencies and local font sanitisation"
        )


def validate_notebooks(concepts: set[str], outcomes: set[str], errors: list[str]) -> None:
    curriculum = yaml.safe_load((ROOT / "curriculum.yml").read_text(encoding="utf-8"))
    declared_sources = {
        item["artifact"]
        for item in curriculum["enrichment_release"]["source_contract"][
            "notebook_native_exceptions"
        ]
    }
    actual_sources = {
        path.relative_to(ROOT).as_posix()
        for path in (ROOT / "notebooks/instructor").rglob("*.ipynb")
    }
    if actual_sources != declared_sources:
        errors.append(
            "Notebook-native source inventory disagrees with curriculum: "
            f"declared={sorted(declared_sources)}, actual={sorted(actual_sources)}"
        )
    for path in sorted((ROOT / "notebooks/instructor").rglob("*.ipynb")):
        notebook = nbformat.read(path, as_version=4)
        try:
            nbformat.validate(notebook)
        except Exception as exc:
            errors.append(f"{path.relative_to(ROOT)}: {exc}")
            continue
        course = notebook.metadata.get("course", {})
        if course.get("language") != "en":
            errors.append(f"{path.relative_to(ROOT)}: language must be en")
        accessibility = course.get("accessibility", {})
        if accessibility.get("keyboard_only") is not True:
            errors.append(f"{path.relative_to(ROOT)}: keyboard-only completion is required")
        if accessibility.get("colour_alone_forbidden") is not True:
            errors.append(f"{path.relative_to(ROOT)}: colour-only meaning must be forbidden")
        if course.get("priority") == "P0" and course.get("execution_profile") != "fast":
            errors.append(f"{path.relative_to(ROOT)}: P0 notebooks must execute in fast CI")
        unknown_concepts = set(course.get("concept_ids", [])) - concepts
        unknown_outcomes = set(course.get("outcomes", [])) - outcomes
        if unknown_concepts:
            errors.append(f"{path.relative_to(ROOT)}: unknown concepts {sorted(unknown_concepts)}")
        if unknown_outcomes:
            errors.append(f"{path.relative_to(ROOT)}: unknown outcomes {sorted(unknown_outcomes)}")
        for index, cell in enumerate(notebook.cells):
            tags = set(cell.metadata.get("tags", []))
            if "solution" in tags and not cell.metadata.get("course", {}).get("student_source"):
                errors.append(
                    f"{path.relative_to(ROOT)}: solution cell {index} lacks student source"
                )
        combined_code = "\n".join(
            cell.source for cell in notebook.cells if cell.cell_type == "code"
        )
        if course.get("priority") in {"P0", "P1"} and "ipywidgets" in combined_code:
            errors.append(f"{path.relative_to(ROOT)}: required notebook depends on widgets")
        plotting_cells = [
            cell.source
            for cell in notebook.cells
            if cell.cell_type == "code" and "plt.show()" in cell.source
        ]
        for source in plotting_cells:
            required_figure_terms = ("title=", "xlabel=", "ylabel=", "linestyle=", "marker=")
            if any(term not in source for term in required_figure_terms):
                errors.append(
                    f"{path.relative_to(ROOT)}: figure lacks labels or non-colour encoding"
                )


def validate_datasets(errors: list[str]) -> None:
    for metadata_path in sorted((ROOT / "datasets/snapshots").glob("*/SOURCE.yml")):
        metadata = yaml.safe_load(metadata_path.read_text(encoding="utf-8"))
        snapshot = metadata_path.parent / metadata["snapshot_file"]
        if not snapshot.exists():
            errors.append(f"{snapshot.relative_to(ROOT)}: missing snapshot")
            continue
        if digest(snapshot) != metadata["snapshot_sha256"]:
            errors.append(f"{snapshot.relative_to(ROOT)}: checksum mismatch")
        if snapshot.stat().st_size != metadata["snapshot_size_bytes"]:
            errors.append(f"{snapshot.relative_to(ROOT)}: size mismatch")
        if metadata.get("licence") != "CC-BY-4.0":
            errors.append(f"{metadata_path.relative_to(ROOT)}: unexpected licence")
    for manifest_path in sorted((ROOT / "datasets/teaching").glob("*/MANIFEST.yml")):
        manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
        for record in manifest["files"]:
            data_path = manifest_path.parent / record["path"]
            if not data_path.exists():
                errors.append(f"{data_path.relative_to(ROOT)}: missing teaching table")
                continue
            if digest(data_path) != record["sha256"]:
                errors.append(f"{data_path.relative_to(ROOT)}: teaching-table checksum mismatch")
            if data_path.stat().st_size != record["size_bytes"]:
                errors.append(f"{data_path.relative_to(ROOT)}: teaching-table size mismatch")


def validate_naming_and_privacy(errors: list[str]) -> None:
    ignored_roots = {
        "archive/raw",
        ".audit-work",
        ".git",
        ".venv",
        "node_modules",
        "build",
        "public",
    }
    roadmap_plan_root = "docs/analysis/"
    reserved_roadmap_token = "pha" + "se"
    for path in ROOT.rglob("*"):
        relative = path.relative_to(ROOT).as_posix()
        if any(relative == root or relative.startswith(f"{root}/") for root in ignored_roots):
            continue
        if reserved_roadmap_token in path.name.lower():
            errors.append(f"{relative}: roadmap sequence naming is reserved")
        if path.is_file() and not relative.startswith(roadmap_plan_root):
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            if reserved_roadmap_token in text.lower():
                errors.append(f"{relative}: roadmap sequence terminology is reserved")
    forbidden = [ROOT / "docs/course/modules/PRIVATE", ROOT / "assessments", ROOT / "solutions"]
    for path in forbidden:
        if path.exists():
            errors.append(f"{path.relative_to(ROOT)}: private material in the public tree")
    if (ROOT / ".git").exists():
        tracked = subprocess.run(
            ["git", "ls-files", "archive/raw"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        if tracked:
            errors.append("Raw archive content is tracked by Git")
    required_templates = {
        "templates/dataset-datasheet.md",
        "templates/result-card.md",
        "templates/data-contract.yml",
        "templates/reproducibility-manifest.yml",
        "templates/ai-notes/README.md",
    }
    missing_templates = {path for path in required_templates if not (ROOT / path).exists()}
    if missing_templates:
        errors.append(f"Required delivery templates are missing: {sorted(missing_templates)}")


def validate_workflow_pins(errors: list[str]) -> None:
    for path in sorted((ROOT / ".github/workflows").glob("*.yml")):
        for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            match = re.search(r"\buses:\s*([^@\s]+)@([^\s#]+)", line)
            if not match or match.group(1).startswith("./"):
                continue
            if not re.fullmatch(r"[0-9a-f]{40}", match.group(2)):
                errors.append(
                    f"{path.relative_to(ROOT)}:{line_number}: action is not pinned to a commit"
                )


def validate_execution_job_permissions(errors: list[str]) -> None:
    execution_commands = (
        "npm run check",
        "npm run build",
        "npm run site",
        "npm run release:prepare",
        "npm run release:qualify",
    )
    for path in sorted((ROOT / ".github/workflows").glob("*.yml")):
        workflow = yaml.load(path.read_text(encoding="utf-8"), Loader=yaml.BaseLoader)
        global_permissions = workflow.get("permissions", {})
        for job_name, job in workflow.get("jobs", {}).items():
            steps = job.get("steps", [])
            run_commands = "\n".join(step.get("run", "") for step in steps)
            if not any(command in run_commands for command in execution_commands):
                continue
            permissions = job.get("permissions", global_permissions)
            if permissions.get("contents") != "read" or any(
                value != "read" for key, value in permissions.items() if key != "contents"
            ):
                relative = path.relative_to(ROOT)
                errors.append(
                    f"{relative}:{job_name}: executable-page job must have read-only permissions"
                )
            checkout_steps = [
                step for step in steps if step.get("uses", "").startswith("actions/checkout@")
            ]
            if not checkout_steps:
                relative = path.relative_to(ROOT)
                errors.append(
                    f"{relative}:{job_name}: executable-page job must check out explicitly"
                )
                continue
            for step in checkout_steps:
                if step.get("with", {}).get("persist-credentials") != "false":
                    relative = path.relative_to(ROOT)
                    errors.append(f"{relative}:{job_name}: checkout must not persist credentials")


def validate_priority_language(errors: list[str]) -> None:
    meanings = {"0": "essential", "1": "core", "2": "extension", "3": "deferred"}
    pages_root = ROOT / "docs/course/modules"
    for path in sorted(pages_root.rglob("*.adoc")):
        for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            if line.startswith(":page-course-"):
                continue
            lower_line = line.lower()
            for level in re.findall(r"\bP([0-3])\b", line):
                meaning = meanings[level]
                if meaning not in lower_line:
                    relative = path.relative_to(ROOT)
                    errors.append(
                        f"{relative}:{line_number}: P{level} must be explained as {meaning.title()}"
                    )


def main() -> None:
    errors: list[str] = []
    _, concepts, outcomes = load_curriculum(errors)
    validate_pages(concepts, outcomes, errors)
    validate_executable_pages(errors)
    validate_notebooks(concepts, outcomes, errors)
    validate_datasets(errors)
    validate_naming_and_privacy(errors)
    validate_priority_language(errors)
    validate_workflow_pins(errors)
    validate_execution_job_permissions(errors)
    ui_bundle = ROOT / "vendor/antora-ui/ui-bundle-v0.53.zip"
    if not ui_bundle.exists() or digest(ui_bundle) != UI_SHA256:
        errors.append("Pinned Antora UI bundle is missing or has the wrong checksum")
    source_validation = json.loads((ROOT / "audit/source-validation.json").read_text())
    if source_validation.get("status") != "pass":
        errors.append("Source-audit validation does not pass")
    if errors:
        print("Repository validation failed:")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)
    print(f"Repository validation passed: {len(concepts)} concepts, {len(outcomes)} outcomes")


if __name__ == "__main__":
    main()
