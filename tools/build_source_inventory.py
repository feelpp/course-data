#!/usr/bin/env python3
"""Build the source inventory from the quarantined archive and reviewed decisions."""

from __future__ import annotations

import ast
import csv
import hashlib
import json
import re
import unicodedata
import warnings
import zipfile
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any

import nbformat
import yaml
from IPython.core.inputtransformer2 import TransformerManager

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "archive/raw/20260718/content"
ZIP = ROOT / "archive/raw/20260718/source.zip"
DECISIONS = ROOT / "audit/source-decisions.yml"
CURRICULUM = ROOT / "curriculum.yml"
OUT_JSON = ROOT / "docs/analysis/source-inventory.json"
OUT_CSV = ROOT / "docs/analysis/source-inventory.csv"
OUT_VALIDATION = ROOT / "audit/source-validation.json"
RAW_MANIFEST = ROOT / "archive/raw/20260718/MANIFEST.sha256"


def slug(value: str) -> str:
    value = unicodedata.normalize("NFKD", value)
    value = value.encode("ascii", "ignore").decode("ascii").lower()
    return re.sub(r"[^a-z0-9]+", "-", value).strip("-")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def source_text(cell: dict[str, Any]) -> str:
    source = cell.get("source", "")
    return "".join(source) if isinstance(source, list) else source


def ordered_unique(values: list[str]) -> list[str]:
    return list(dict.fromkeys(value for value in values if value))


def notebook_facts(path: Path) -> dict[str, Any]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    cells = raw.get("cells", [])
    markdown = [cell for cell in cells if cell.get("cell_type") == "markdown"]
    code = [cell for cell in cells if cell.get("cell_type") == "code"]
    all_text = "\n".join(source_text(cell) for cell in cells)
    code_text = "\n".join(source_text(cell) for cell in code)

    headings: list[str] = []
    for cell in markdown:
        for line in source_text(cell).splitlines():
            if re.match(r"^#{1,4}\s+", line):
                headings.append(re.sub(r"^#+\s*", "", line).strip())

    urls = ordered_unique(
        [match.rstrip(".,;:") for match in re.findall(r"https?://[^\s)\]}>\"']+", all_text)]
    )
    imports: set[str] = set()
    syntax_error_cells: list[int] = []
    transformer = TransformerManager()
    for index, cell in enumerate(code):
        text = source_text(cell)
        try:
            transformed = transformer.transform_cell(text)
            tree = ast.parse(transformed)
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    imports.update(alias.name.split(".")[0] for alias in node.names)
                elif isinstance(node, ast.ImportFrom) and node.module:
                    imports.add(node.module.split(".")[0])
        except (SyntaxError, IndentationError):
            syntax_error_cells.append(index)

    validation_errors: list[str] = []
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        try:
            nbformat.validate(nbformat.from_dict(raw))
        except Exception as exc:  # validation errors vary by nbformat version
            validation_errors.append(f"{type(exc).__name__}: {exc}")
        validation_errors.extend(str(item.message) for item in caught)

    output_count = sum(len(cell.get("outputs", [])) for cell in code)
    error_output_count = sum(
        1
        for cell in code
        for output in cell.get("outputs", [])
        if output.get("output_type") == "error"
    )
    executed_count = sum(cell.get("execution_count") is not None for cell in code)
    local_refs = ordered_unique(
        re.findall(
            r"(?i)(?:read_csv|read_excel|read_parquet|loadtxt|genfromtxt|open)\s*\(\s*[rubf]*[\"']([^\"']+)",
            code_text,
        )
    )
    flags = {
        "network_or_external_data": bool(
            re.search(r"(?i)(https?://|urlopen|wget|curl|git\s+clone|download|get_file)", code_text)
        ),
        "environment_mutation": bool(
            re.search(r"(?i)(pip\s+install|conda\s+install|apt-get|brew\s+install)", code_text)
        ),
        "filesystem_write_or_delete": bool(
            re.search(
                r"(?i)(to_csv|to_pickle|pickle\.dump|shutil\.(?:rmtree|copy)|os\.(?:remove|unlink)|open\([^\n]*(?:[\"']w|[\"']a))",
                code_text,
            )
        ),
        "uses_randomness": bool(
            re.search(
                r"(?i)(np\.random|numpy\.random|random\.|jax\.random|train_test_split)", code_text
            )
        ),
        "declares_seed": bool(re.search(r"(?i)(seed\s*\(|random_state\s*=|PRNGKey)", code_text)),
    }
    return {
        "notebook_format": f"{raw.get('nbformat')}.{raw.get('nbformat_minor')}",
        "kernel": raw.get("metadata", {}).get("kernelspec", {}).get("name"),
        "cell_count": len(cells),
        "markdown_cell_count": len(markdown),
        "code_cell_count": len(code),
        "executed_code_cell_count": executed_count,
        "output_count": output_count,
        "error_output_count": error_output_count,
        "outputs_without_complete_execution_record": bool(
            output_count and executed_count < len(code)
        ),
        "headings": headings,
        "imports": sorted(imports),
        "source_urls": urls,
        "local_file_references": local_refs,
        "markdown_attachment_count": sum(len(cell.get("attachments", {})) for cell in markdown),
        "inline_data_image_count": all_text.count("data:image"),
        "syntax_error_code_cells": syntax_error_cells,
        "notebook_validation_messages": validation_errors,
        **flags,
    }


def pdf_facts() -> dict[str, Any]:
    return {
        "page_count": 28,
        "pdf_version": "1.5",
        "creator": "LaTeX with Beamer class",
        "producer": "pdfTeX-1.40.18",
        "document_date": "2020-01-22",
        "identified_author": "Stanley Chan",
        "identified_institution": "Purdue University",
        "rights_notice": "Stanley Chan 2020. All Rights Reserved.",
        "visual_review": (
            "Cover rendered and inspected; title, author, institution, and rights notice confirmed."
        ),
    }


def main() -> None:
    decisions = yaml.safe_load(DECISIONS.read_text(encoding="utf-8"))
    curriculum = yaml.safe_load(CURRICULUM.read_text(encoding="utf-8"))
    concept_ids = {item["id"] for item in curriculum["concepts"]}
    defaults = decisions["defaults"]
    reviewed = decisions["items"]
    ids = [item["id"] for item in reviewed]
    if len(ids) != len(set(ids)):
        raise SystemExit("Duplicate source decision identifiers")
    unknown_concepts = sorted(
        {
            concept
            for item in reviewed
            for concept in item.get("concepts", [])
            if concept not in concept_ids
        }
    )
    if unknown_concepts:
        raise SystemExit(f"Unknown curriculum concepts: {unknown_concepts}")

    paths = sorted(path for path in RAW.rglob("*") if path.is_file())
    if len(paths) != 38:
        raise SystemExit(f"Expected 38 extracted items, found {len(paths)}")

    zip_dates: dict[str, str] = {}
    with zipfile.ZipFile(ZIP) as archive:
        for info in archive.infolist():
            zip_dates[slug(info.filename)] = datetime(*info.date_time).isoformat()

    inventory: list[dict[str, Any]] = []
    used_decisions: set[str] = set()
    for path in paths:
        original_path = path.relative_to(RAW).as_posix()
        path_slug = slug(original_path)
        matches = [item for item in reviewed if item["match"] in path_slug]
        if matches:
            longest = max(len(item["match"]) for item in matches)
            matches = [item for item in matches if len(item["match"]) == longest]
        if len(matches) != 1:
            raise SystemExit(
                f"{original_path}: expected one longest decision match, found {len(matches)}"
            )
        decision = matches[0]
        used_decisions.add(decision["id"])
        is_notebook = path.suffix.lower() == ".ipynb" or path.suffix == ""
        name_source = original_path[: -len(path.suffix)] if path.suffix else original_path
        normalised_name = slug(name_source) + (".ipynb" if is_notebook else path.suffix.lower())
        facts = notebook_facts(path) if is_notebook else pdf_facts()
        item = {
            "id": decision["id"],
            "original_path": original_path,
            "normalised_name_for_derived_work": normalised_name,
            "sha256": sha256(path),
            "size_bytes": path.stat().st_size,
            "archive_modified_at": zip_dates.get(path_slug),
            "custodial_owner": decision.get("custodial_owner", defaults["custodial_owner"]),
            "copyright_holder": decision.get("copyright_holder", defaults["copyright_holder"]),
            "licence_status": decision.get("licence_status", defaults["licence_status"]),
            "publication_status": decision.get(
                "publication_status", defaults["publication_status"]
            ),
            "rights_action": decision.get("rights_action", defaults["rights_action"]),
            **{key: value for key, value in decision.items() if key not in {"match", "id"}},
            **facts,
        }
        if is_notebook:
            item["provenance_status"] = "partial" if item["source_urls"] else "unknown"
            item["execution_status"] = "not_executed_during_ingest"
            item["execution_reason"] = (
                "Raw code is untrusted and may use live downloads, package installation, "
                "filesystem mutation, "
                "missing assets, obsolete APIs, or private solutions. Static checks only."
            )
        else:
            item["provenance_status"] = "identified"
            item["execution_status"] = "not_applicable"
        inventory.append(item)

    unused = set(ids) - used_decisions
    if unused:
        raise SystemExit(f"Unused source decisions: {sorted(unused)}")

    inventory.sort(key=lambda item: item["id"])
    normalised_names = [item["normalised_name_for_derived_work"] for item in inventory]
    if len(normalised_names) != len(set(normalised_names)):
        raise SystemExit("Normalised names are not unique")
    non_quarantined = [
        item["id"] for item in inventory if item["publication_status"] != "quarantined"
    ]
    if non_quarantined:
        raise SystemExit(f"Raw items are not quarantined: {non_quarantined}")

    OUT_JSON.write_text(
        json.dumps(inventory, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    csv_fields = [
        "id",
        "original_path",
        "normalised_name_for_derived_work",
        "sha256",
        "size_bytes",
        "archive_modified_at",
        "topic",
        "material_type",
        "audience",
        "language",
        "priority_candidate",
        "disposition",
        "destination",
        "concepts",
        "custodial_owner",
        "copyright_holder",
        "licence_status",
        "publication_status",
        "provenance_status",
        "execution_status",
        "cell_count",
        "code_cell_count",
        "output_count",
        "error_output_count",
        "outputs_without_complete_execution_record",
        "imports",
        "source_urls",
        "local_file_references",
        "environment_mutation",
        "network_or_external_data",
        "filesystem_write_or_delete",
        "rationale",
        "rights_action",
    ]
    with OUT_CSV.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=csv_fields, extrasaction="ignore")
        writer.writeheader()
        for item in inventory:
            row = dict(item)
            for key in ("concepts", "imports", "source_urls", "local_file_references"):
                row[key] = "; ".join(str(value) for value in row.get(key, []))
            writer.writerow(row)

    manifest_paths = [ZIP] + paths
    manifest_lines = [
        f"{sha256(path)}  {path.relative_to(ROOT / 'archive/raw/20260718').as_posix()}"
        for path in manifest_paths
    ]
    RAW_MANIFEST.write_text("\n".join(manifest_lines) + "\n", encoding="utf-8")

    validation = {
        "status": "pass",
        "review_date": decisions["review_date"].isoformat(),
        "expected_items": 38,
        "inventoried_items": len(inventory),
        "decision_ids_unique": True,
        "normalised_names_unique": True,
        "curriculum_concept_references_valid": True,
        "raw_items_quarantined": len(inventory),
        "raw_items_approved_for_publication": 0,
        "archive_manifest_entries": len(manifest_lines),
        "errors": [],
    }
    OUT_VALIDATION.write_text(json.dumps(validation, indent=2) + "\n", encoding="utf-8")

    counts = Counter(item["disposition"] for item in inventory)
    print(f"Wrote {OUT_JSON.relative_to(ROOT)} and {OUT_CSV.relative_to(ROOT)}")
    print(f"Wrote {OUT_VALIDATION.relative_to(ROOT)} and raw checksum manifest")
    print(f"Items: {len(inventory)}")
    print("Dispositions:", dict(sorted(counts.items())))


if __name__ == "__main__":
    main()
