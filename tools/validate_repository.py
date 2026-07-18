#!/usr/bin/env python3
"""Validate curriculum, content metadata, snapshots, notebooks, privacy, and pins."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
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

    release = curriculum["foundation_release"]
    release_paths = [
        *release["pages"],
        *release["notebooks"],
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
        if page.exists() and parse_header(page).get("page-course-priority") != "P0":
            errors.append(f"Foundation page must be P0: {relative}")
    for relative in release["notebooks"]:
        path = ROOT / relative
        if not path.exists():
            continue
        course = nbformat.read(path, as_version=4).metadata.get("course", {})
        if course.get("priority") != "P0" or course.get("execution_profile") != "fast":
            errors.append(f"Foundation notebook must be P0 and fast: {relative}")


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


def validate_notebooks(concepts: set[str], outcomes: set[str], errors: list[str]) -> None:
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
    exclusions = {"docs/analysis/20260718_starter.md"}
    ignored_roots = {"archive/raw", ".git", ".venv", "node_modules", "build", "public"}
    reserved_roadmap_token = "pha" + "se"
    for path in ROOT.rglob("*"):
        relative = path.relative_to(ROOT).as_posix()
        if any(relative == root or relative.startswith(f"{root}/") for root in ignored_roots):
            continue
        if reserved_roadmap_token in path.name.lower():
            errors.append(f"{relative}: roadmap sequence naming is reserved")
        if path.is_file() and relative not in exclusions:
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


def main() -> None:
    errors: list[str] = []
    _, concepts, outcomes = load_curriculum(errors)
    validate_pages(concepts, outcomes, errors)
    validate_notebooks(concepts, outcomes, errors)
    validate_datasets(errors)
    validate_naming_and_privacy(errors)
    validate_workflow_pins(errors)
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
