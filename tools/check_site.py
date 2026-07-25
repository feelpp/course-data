#!/usr/bin/env python3
"""Check that the generated site and its local links are complete."""

from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

import jsonschema
import nbformat
import yaml
from nbclient import NotebookClient
from nbclient.exceptions import CellExecutionError, CellTimeoutError, DeadKernelError

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "public"
PRIVATE_CELL_TAGS = {"solution", "instructor-only", "remove-cell"}
WORKED_EXAMPLE_PARTS = ["Context", "Method", "Implementation", "Results", "Conclusion"]


class LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.targets: list[str] = []
        self.jupyter_targets: list[str] = []
        self.external_runtime_targets: list[str] = []
        self.images_without_alt: list[str] = []
        self.ids: list[str] = []
        self.has_main_landmark = False
        self.has_skip_link = False
        self.language: str | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        if tag == "html":
            self.language = attributes.get("lang")
        if attributes.get("id"):
            self.ids.append(attributes["id"])
        if tag == "img" and "alt" not in attributes:
            self.images_without_alt.append(attributes.get("src") or "<unknown image>")
        if tag == "main" and attributes.get("id") == "main-content":
            self.has_main_landmark = True
        if tag == "a" and attributes.get("href") == "#main-content":
            self.has_skip_link = True
        if tag == "a" and "jupyter-download" in (attributes.get("class") or "").split():
            self.jupyter_targets.append(attributes.get("href") or "")
        runtime_target = None
        if tag in {"script", "img", "source", "video", "audio"}:
            runtime_target = attributes.get("src")
        elif tag == "link" and "stylesheet" in (attributes.get("rel") or "").split():
            runtime_target = attributes.get("href")
        if runtime_target:
            parsed_runtime = urlsplit(runtime_target)
            if parsed_runtime.scheme in {"http", "https"} or parsed_runtime.netloc:
                self.external_runtime_targets.append(runtime_target)
        for name, value in attrs:
            if value and ((tag == "a" and name == "href") or name == "src"):
                self.targets.append(value)


def target_path(page: Path, target: str, site: Path = SITE) -> Path | None:
    parsed = urlsplit(target)
    if parsed.scheme or parsed.netloc or target.startswith(("mailto:", "data:", "#")):
        return None
    clean = unquote(parsed.path)
    if not clean:
        return None
    if clean.startswith("/"):
        return site / clean.lstrip("/")
    return (page.parent / clean).resolve()


def validate_jupyter_target(page: Path, target: str, site: Path = SITE) -> list[str]:
    errors: list[str] = []
    parsed = urlsplit(target)
    if not target or target == "#":
        return ["Jupyter link is empty or unresolved"]
    if parsed.scheme or parsed.netloc:
        return [f"Jupyter link must be a local generated attachment: {target}"]
    if not unquote(parsed.path).endswith(".ipynb"):
        errors.append(f"Jupyter link does not target an .ipynb attachment: {target}")
    destination = target_path(page, target, site)
    if destination is None:
        errors.append(f"Jupyter link cannot be resolved: {target}")
        return errors
    destination = destination.resolve()
    if not destination.is_relative_to(site.resolve()):
        errors.append(f"Jupyter link escapes the generated site: {target}")
    elif not destination.is_file():
        errors.append(f"Jupyter attachment is missing: {target}")
    return errors


def expected_notebook_contracts() -> tuple[list[Path], dict[str, dict], set[str]]:
    curriculum = yaml.safe_load((ROOT / "curriculum.yml").read_text(encoding="utf-8"))
    lesson_sources = [
        *curriculum["foundation_release"]["notebook_sources"],
        *curriculum["analytical_release"]["notebook_sources"],
        *curriculum["enrichment_release"]["page_notebook_sources"],
    ]
    exercise_by_source: dict[str, dict] = {}
    for specimen in curriculum["exercise_release"]["public_specimens"]:
        source_path = Path(specimen["source"])
        source_relative = source_path.relative_to("docs/course/modules/ROOT/pages").as_posix()
        rubric_criteria = [
            criterion
            for criterion in curriculum["exercise_release"]["rubric"]["criteria"]
            if any(criterion in task["rubric_criteria"] for task in specimen["tasks"])
        ]
        exercise_by_source[source_relative] = {
            "assessment_id": specimen["assessment_id"],
            "exercise_id": specimen["exercise_id"],
            "kind": specimen["kind"],
            "task_ids": [task["id"] for task in specimen["tasks"]],
            "task_priorities": {task["id"]: task["priorities"] for task in specimen["tasks"]},
            "task_points": {task["id"]: task["points"] for task in specimen["tasks"]},
            "hint_policy": specimen["hint_policy"],
            "ai_mode": specimen["ai_mode"],
            "allowed_resources": specimen["allowed_resources"],
            "submission_evidence": specimen["submission_evidence"],
            "rubric_criteria": rubric_criteria,
        }
    source_relatives = [
        Path(source).relative_to("docs/course/modules/ROOT/pages").as_posix()
        for source in lesson_sources
    ] + list(exercise_by_source)
    notebooks = [
        SITE / "course-data/_attachments" / Path(relative).with_suffix(".ipynb")
        for relative in source_relatives
    ]
    worked_sources = {
        Path(source).relative_to("docs/course/modules/ROOT/pages").as_posix()
        for source in curriculum["worked_example_release"]["notebook_sources"]
    }
    return notebooks, exercise_by_source, worked_sources


def validate_exercise_notebook(notebook, expected: dict, label: str) -> list[str]:
    errors: list[str] = []
    course = notebook.metadata.get("course", {})
    if course.get("artifact_variant") != "student" or course.get("solutions_included") is not False:
        errors.append(f"{label}: notebook is not a declared solution-free student artifact")
    if course.get("exercise") != expected:
        errors.append(f"{label}: notebook exercise metadata disagrees with curriculum")
    prompt_task_ids: list[str] = []
    for cell in notebook.cells:
        tags = set(cell.metadata.get("tags", []))
        if tags & PRIVATE_CELL_TAGS:
            errors.append(f"{label}: private notebook cell tag is present")
        if "exercise-prompt" in tags:
            prompt_task_ids.extend(cell.metadata.get("course", {}).get("task_ids", []))
    if set(prompt_task_ids) != set(expected["task_ids"]) or len(prompt_task_ids) != len(
        expected["task_ids"]
    ):
        errors.append(f"{label}: prompt-cell task IDs disagree with curriculum")
    markdown = "\n".join(cell.source for cell in notebook.cells if cell.cell_type == "markdown")
    for task_id in expected["task_ids"]:
        if task_id not in markdown:
            errors.append(f"{label}: task is absent from notebook narrative: {task_id}")
    return errors


def validate_worked_example_notebook(notebook, label: str) -> list[str]:
    errors: list[str] = []
    markdown = "\n".join(cell.source for cell in notebook.cells if cell.cell_type == "markdown")
    positions: list[int] = []
    heading_matches: dict[str, re.Match[str]] = {}
    for part in WORKED_EXAMPLE_PARTS:
        matches = list(re.finditer(rf"(?m)^#+\s+{part}\s*$", markdown))
        if len(matches) != 1:
            errors.append(
                f"{label}: notebook must contain exactly one worked-example {part} heading"
            )
            continue
        positions.append(matches[0].start())
        heading_matches[part] = matches[0]
    if len(positions) == len(WORKED_EXAMPLE_PARTS) and positions != sorted(positions):
        errors.append(f"{label}: worked-example headings are out of order")
    if "Mathematical insight" not in markdown:
        errors.append(f"{label}: notebook is missing the Mathematical insight")
    if "Essential (P0)" not in markdown:
        errors.append(f"{label}: notebook is missing visible importance meaning Essential (P0)")
    if {"Method", "Implementation"} <= set(heading_matches):
        method_text = markdown[
            heading_matches["Method"].end() : heading_matches["Implementation"].start()
        ]
        if not any(meaning in method_text for meaning in ("Essential (P0)", "Core (P1)")):
            errors.append(f"{label}: notebook Method lacks a visible P0/P1 importance")
    return errors


def validate_worked_example_html(page_html: str, label: str) -> list[str]:
    errors: list[str] = []
    positions: list[int] = []
    for part in WORKED_EXAMPLE_PARTS:
        role = f"worked-example-{part.lower()}"
        if page_html.count(role) != 1:
            errors.append(f"{label}: rendered worked example must contain one {role} section")
            continue
        heading = re.search(
            rf'<h3 id="worked-[a-z0-9-]+-{part.lower()}">{part}</h3>',
            page_html,
        )
        if heading is None:
            errors.append(f"{label}: rendered {part} heading lacks its stable semantic ID")
            continue
        positions.append(heading.start())
    if len(positions) == len(WORKED_EXAMPLE_PARTS) and positions != sorted(positions):
        errors.append(f"{label}: rendered worked-example sections are out of order")
    if "Mathematical insight —" not in page_html:
        errors.append(f"{label}: rendered page is missing the titled Mathematical insight")
    if "<strong>Mathematical insight.</strong>" not in page_html:
        errors.append(f"{label}: rendered insight lacks its notebook-portable label")
    return errors


def main() -> None:
    pages = sorted((SITE / "course-data").rglob("*.html"))
    if not pages:
        raise SystemExit("Generated site contains no HTML pages")
    errors: list[str] = []
    sitemap = SITE / "sitemap.xml"
    expected_last_modified = "<lastmod>2026-01-01T00:00:00.000Z</lastmod>"
    if not sitemap.exists():
        errors.append("Generated sitemap is missing")
    else:
        sitemap_source = sitemap.read_text(encoding="utf-8")
        last_modified = re.findall(r"<lastmod>[^<]+</lastmod>", sitemap_source)
        if not last_modified or set(last_modified) != {expected_last_modified}:
            errors.append("Generated sitemap timestamps are not pinned to the release epoch")
    jupyter_links = 0
    for page in pages:
        parser = LinkParser()
        page_html = page.read_text(encoding="utf-8")
        parser.feed(page_html)
        if parser.language != "en":
            errors.append(f"{page.relative_to(SITE)}: rendered document language must be en")
        if "fontawesome-icon-defs.js" not in page_html or "fontawesome.js" not in page_html:
            errors.append(
                f"{page.relative_to(SITE)}: local icon definitions and runtime must both load"
            )
        for target in parser.external_runtime_targets:
            errors.append(
                f"{page.relative_to(SITE)}: external runtime asset breaks offline use: {target}"
            )
        duplicate_ids = [
            identifier for identifier, count in Counter(parser.ids).items() if count > 1
        ]
        for identifier in duplicate_ids:
            errors.append(f"{page.relative_to(SITE)}: duplicate HTML ID: {identifier}")
        if 'scope="col"ead' in page_html:
            errors.append(f"{page.relative_to(SITE)}: malformed table header markup")
        for source in parser.images_without_alt:
            errors.append(f"{page.relative_to(SITE)}: image lacks alt attribute: {source}")
        if not parser.has_main_landmark:
            errors.append(f"{page.relative_to(SITE)}: main content landmark is missing")
        if not parser.has_skip_link:
            errors.append(f"{page.relative_to(SITE)}: skip-to-content link is missing")
        for target in parser.jupyter_targets:
            jupyter_links += 1
            for error in validate_jupyter_target(page, target):
                errors.append(f"{page.relative_to(SITE)}: {error}")
        for target in parser.targets:
            destination = target_path(page, target)
            if destination is None:
                continue
            candidates = [destination]
            if destination.suffix == "":
                candidates.extend([destination / "index.html", destination.with_suffix(".html")])
            if not any(candidate.exists() for candidate in candidates):
                errors.append(f"{page.relative_to(SITE)} -> {target}")
    generated_notebooks, exercise_by_source, worked_sources = expected_notebook_contracts()
    for generated_notebook in generated_notebooks:
        if not generated_notebook.exists():
            errors.append(
                f"AsciiDoc-generated notebook attachment is missing: {generated_notebook.name}"
            )
            continue
        notebook = nbformat.read(generated_notebook, as_version=4)
        try:
            nbformat.validate(notebook)
            metadata_schema = json.loads(
                (ROOT / "schemas/asciidoc-notebook-metadata.schema.json").read_text(
                    encoding="utf-8"
                )
            )
            jsonschema.validate(notebook.metadata["course"], metadata_schema)
            source_path = notebook.metadata["course"]["source_path"]
            if source_path in exercise_by_source:
                errors.extend(
                    validate_exercise_notebook(
                        notebook, exercise_by_source[source_path], generated_notebook.name
                    )
                )
            if source_path in worked_sources:
                errors.extend(validate_worked_example_notebook(notebook, generated_notebook.name))
            for cell in notebook.cells:
                if cell.cell_type == "code" and (cell.outputs or cell.execution_count is not None):
                    errors.append(
                        "AsciiDoc-generated student notebook contains execution state: "
                        f"{generated_notebook.name}"
                    )
            if notebook.metadata["course"].get("priority") != "P2":
                client = NotebookClient(
                    notebook,
                    timeout=120,
                    kernel_name="python3",
                    resources={"metadata": {"path": str(generated_notebook.parent)}},
                )
                client.execute(cwd=str(generated_notebook.parent))
        except (nbformat.ValidationError, jsonschema.ValidationError, KeyError) as error:
            errors.append(f"AsciiDoc-generated notebook contract failed: {error}")
        except (CellExecutionError, CellTimeoutError, DeadKernelError) as error:
            errors.append(f"AsciiDoc-generated notebook execution failed: {error}")
    retired_notebooks = [
        *(SITE / "course-data/_attachments/notebooks/foundations").glob("*.ipynb"),
        *(SITE / "course-data/_attachments/notebooks/analytical").glob("*.ipynb"),
    ]
    for retired_notebook in retired_notebooks:
        if retired_notebook.exists():
            errors.append(
                f"Retired notebook-native artifact was published: {retired_notebook.name}"
            )
    manifest_path = SITE / "course-data/_attachments/generated/asciidoc-notebook-manifest.json"
    if not manifest_path.exists():
        errors.append("AsciiDoc notebook manifest is missing")
    else:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest_schema = json.loads(
            (ROOT / "schemas/asciidoc-notebook-manifest.schema.json").read_text(encoding="utf-8")
        )
        try:
            jsonschema.validate(manifest, manifest_schema)
        except jsonschema.ValidationError as error:
            errors.append(f"AsciiDoc notebook manifest contract failed: {error.message}")
        if "generated_at" in manifest:
            errors.append("AsciiDoc notebook manifest contains a nondeterministic timestamp")
        entries = manifest.get("entries", [])
        resource_ids = [entry.get("source_resource_id", "") for entry in entries]
        if resource_ids != sorted(resource_ids):
            errors.append("AsciiDoc notebook manifest entries are not deterministically sorted")
        for entry in entries:
            target = target_path(manifest_path, entry.get("notebook_url", ""))
            if target is None or not target.is_file():
                errors.append(f"Manifest notebook is missing: {entry.get('notebook_url', '')}")
                continue
            actual = hashlib.sha256(target.read_bytes()).hexdigest()
            if actual != entry.get("notebook_sha256"):
                notebook_url = entry.get("notebook_url", "")
                errors.append(f"Manifest notebook checksum mismatch: {notebook_url}")
            source_path = entry.get("source_path", "")
            expected_exercise = exercise_by_source.get(source_path)
            if expected_exercise is not None and entry.get("exercise") != expected_exercise:
                errors.append(f"Manifest exercise contract mismatch: {source_path}")
            page_target = target_path(manifest_path, entry.get("page_url", ""))
            if expected_exercise is not None and page_target is not None and page_target.is_file():
                page_html = page_target.read_text(encoding="utf-8")
                for task_id in expected_exercise["task_ids"]:
                    if task_id not in page_html:
                        errors.append(f"Generated exercise page is missing task {task_id}")
        expected_sources = {
            notebook.relative_to(SITE / "course-data/_attachments").with_suffix(".adoc").as_posix()
            for notebook in generated_notebooks
        }
        actual_sources = {entry.get("source_path", "") for entry in entries}
        if actual_sources != expected_sources:
            errors.append("AsciiDoc notebook manifest inventory disagrees with curriculum")
    if jupyter_links == 0:
        errors.append("No confirmed Jupyter toolbar link was rendered")
    curriculum = yaml.safe_load((ROOT / "curriculum.yml").read_text(encoding="utf-8"))
    for source in curriculum["worked_example_release"]["pages"]:
        relative = Path(source).relative_to("docs/course/modules/ROOT/pages").with_suffix(".html")
        page = SITE / "course-data" / relative
        if not page.exists():
            errors.append(f"Generated worked-example page is missing: {relative}")
            continue
        errors.extend(
            validate_worked_example_html(
                page.read_text(encoding="utf-8"),
                relative.as_posix(),
            )
        )
    mathematics_page = SITE / "course-data/foundations/mathematical-background.html"
    if not mathematics_page.exists():
        errors.append("Generated mathematical-background page is missing")
    else:
        mathematics_html = mathematics_page.read_text(encoding="utf-8")
        if 'class="stemblock"' not in mathematics_html:
            errors.append("Displayed stem mathematics is absent from the generated page")
        if not re.search(r"<p>.*?\\\(.*?\\\)", mathematics_html, re.DOTALL):
            errors.append("Inline stem mathematics is absent from the generated page")
        if "_attachments/vendor/katex/katex.min.js" not in mathematics_html:
            errors.append("Local KaTeX runtime is not loaded on the generated mathematical page")
        if "_attachments/vendor/katex/katex.min.css" not in mathematics_html:
            errors.append("Local KaTeX styles are not loaded on the generated mathematical page")
    lesson_contracts = {
        "data-lifecycle.html": {
            "stem_blocks": 1,
            "table_results": 1,
            "terms": ("Estimand and estimate", "First error ledger", "blocks analysis"),
        },
        "tabular-data.html": {
            "stem_blocks": 3,
            "table_results": 1,
            "terms": ("Join multiplicity", "many-to-one", "unit of analysis"),
        },
        "data-quality.html": {
            "stem_blocks": 2,
            "table_results": 1,
            "terms": ("MCAR", "median absolute deviation", "Sensitivity analysis"),
        },
        "eda-sampling.html": {
            "stem_blocks": 3,
            "matplotlib_results": 1,
            "svg_results": 1,
            "terms": ("Empirical covariance and correlation", "Sampling and representativeness"),
        },
        "probability-distributions-moments.html": {
            "stem_blocks": 5,
            "matplotlib_results": 1,
            "table_results": 1,
            "terms": ("Probability distribution zoo", "Excess kurtosis", "failed Poisson"),
        },
        "quantiles-exceedance-risk.html": {
            "stem_blocks": 8,
            "matplotlib_results": 1,
            "svg_results": 1,
            "terms": ("Generalized quantile", "strict exceedance", "classifier decision threshold"),
        },
        "mean-uncertainty.html": {
            "stem_blocks": 10,
            "matplotlib_results": 1,
            "terms": ("Classical central limit theorem", "square-root law", "long-run coverage"),
        },
        "safe-pipelines.html": {
            "stem_blocks": 3,
            "table_results": 1,
            "terms": (
                "Feature-time boundary",
                "Training-fitted transformation",
                "paired difference",
            ),
        },
        "metrics-errors.html": {
            "stem_blocks": 6,
            "table_results": 1,
            "terms": (
                "Common regression losses",
                "empirical decision cost",
                "binomial standard error",
            ),
        },
        "baseline-synthesis.html": {
            "stem_blocks": 1,
            "table_results": 1,
            "terms": ("evidence chain", "paired losses", "real factory"),
        },
    }
    for filename, contract in lesson_contracts.items():
        lesson_page = SITE / "course-data/foundations" / filename
        if not lesson_page.exists():
            errors.append(f"Generated mathematics lesson is missing: {filename}")
            continue
        lesson_html = lesson_page.read_text(encoding="utf-8")
        if lesson_html.count('class="stemblock"') < contract["stem_blocks"]:
            errors.append(f"{filename} is missing displayed STEM mathematics")
        if lesson_html.count("dynamic-py-result-matplotlib") < contract.get(
            "matplotlib_results", 0
        ):
            errors.append(f"{filename} is missing its Matplotlib result")
        if lesson_html.count("dynamic-py-result-table") < contract.get("table_results", 0):
            errors.append(f"{filename} is missing its semantic table result")
        if lesson_html.count("data:image/svg+xml;base64,") < contract.get("svg_results", 0):
            errors.append(f"{filename} is missing its deterministic SVG result")
        for term in contract["terms"]:
            if term not in lesson_html:
                errors.append(f"{filename} is missing required learning content: {term}")
    linear_page = SITE / "course-data/analytical/linear-probabilistic.html"
    if not linear_page.exists():
        errors.append("Generated linear-probabilistic lesson is missing")
    else:
        linear_html = linear_page.read_text(encoding="utf-8")
        if linear_html.count('class="stemblock"') < 8:
            errors.append("linear-probabilistic.html is missing displayed STEM mathematics")
        if linear_html.count("dynamic-py-result-matplotlib") < 1:
            errors.append("linear-probabilistic.html is missing its residual diagnostic")
        if linear_html.count("dynamic-py-result-table") < 1:
            errors.append("linear-probabilistic.html is missing its conditioning table")
    analytical_contracts = {
        "classification-losses.html": {
            "stem_blocks": 6,
            "terms": ("Binary cross-entropy", "Stable computation", "log loss"),
        },
        "regularisation-generalisation.html": {
            "stem_blocks": 6,
            "terms": ("Ridge estimator", "Bias–variance mathematics", "selection frequency"),
        },
        "model-selection.html": {
            "stem_blocks": 2,
            "terms": (
                "K-fold cross-validation estimate",
                "Nested evaluation",
                "Selection optimism",
            ),
        },
        "tree-ensembles.html": {
            "stem_blocks": 7,
            "terms": ("Gini impurity", "Ensemble correlation", "Permutation importance"),
        },
        "pca-clustering.html": {
            "stem_blocks": 5,
            "terms": (
                "Principal directions and scores",
                "K-means objective",
                "Error estimation and stability",
            ),
        },
        "performance-columnar.html": {
            "stem_blocks": 5,
            "terms": ("Peak-memory budget", "Columnar execution", "query pushdown"),
        },
    }
    for filename, contract in analytical_contracts.items():
        page = SITE / "course-data/analytical" / filename
        if not page.exists():
            errors.append(f"Generated analytical lesson is missing: {filename}")
            continue
        html = page.read_text(encoding="utf-8")
        if html.count('class="stemblock"') < contract["stem_blocks"]:
            errors.append(f"{filename} is missing displayed STEM mathematics")
        if html.count("dynamic-py-result-table") < 1:
            errors.append(f"{filename} is missing its diagnostic table")
        if html.count("dynamic-py-result-matplotlib") < 1:
            errors.append(f"{filename} is missing its accessible diagnostic figure")
        if html.count("data:image/svg+xml;base64,") < 1:
            errors.append(f"{filename} is missing its deterministic SVG result")
        for term in contract["terms"]:
            if term not in html:
                errors.append(f"{filename} is missing required learning content: {term}")
    extension_contracts = {
        "jax-transformations.html": {
            "stem_blocks": 4,
            "table_results": 0,
            "matplotlib_results": 0,
            "terms": (
                "Mathematical background",
                "central finite-difference challenge",
                "Source and environment exception",
            ),
        },
        "kernel-methods.html": {
            "stem_blocks": 7,
            "table_results": 1,
            "matplotlib_results": 1,
            "terms": (
                "Positive-semidefinite kernel",
                "regularisation bounds spectral amplification",
                "Error estimation",
            ),
        },
        "probability-calibration.html": {
            "stem_blocks": 5,
            "table_results": 1,
            "matplotlib_results": 1,
            "terms": (
                "Population calibration",
                "calibration can change probabilities without changing ranking",
                "reliability evidence and uncertainty",
            ),
        },
        "experiment-tracking.html": {
            "stem_blocks": 2,
            "table_results": 1,
            "matplotlib_results": 0,
            "terms": (
                "Identity, integrity, and limitations",
                "selection evidence and final evidence are different random variables",
                "Error estimation",
            ),
        },
        "drift-monitoring.html": {
            "stem_blocks": 3,
            "table_results": 1,
            "matplotlib_results": 1,
            "terms": (
                "Statistics answer narrow questions",
                "input stability and predictive validity are logically distinct",
                "multiple signals",
            ),
        },
        "dataframe-engines.html": {
            "stem_blocks": 2,
            "table_results": 0,
            "matplotlib_results": 0,
            "terms": (
                "Source and environment exception",
                "Mathematical limits",
                "physical lower bound",
            ),
        },
        "downstream-paths.html": {
            "stem_blocks": 0,
            "table_results": 0,
            "matplotlib_results": 0,
            "terms": (
                "Source exception",
                "ownership and prerequisite map",
                "Deferred archive map",
            ),
        },
    }
    for filename, contract in extension_contracts.items():
        page = SITE / "course-data/extensions" / filename
        if not page.exists():
            errors.append(f"Generated optional lesson is missing: {filename}")
            continue
        html = page.read_text(encoding="utf-8")
        if html.count('class="stemblock"') < contract["stem_blocks"]:
            errors.append(f"{filename} is missing displayed STEM mathematics")
        if html.count("dynamic-py-result-table") < contract["table_results"]:
            errors.append(f"{filename} is missing its semantic result table")
        if html.count("dynamic-py-result-matplotlib") < contract["matplotlib_results"]:
            errors.append(f"{filename} is missing its accessible result figure")
        if contract["matplotlib_results"] and html.count("data:image/svg+xml;base64,") < 1:
            errors.append(f"{filename} is missing its deterministic SVG result")
        for term in contract["terms"]:
            if term not in html:
                errors.append(f"{filename} is missing required extension content: {term}")
    for filename in (
        "jax-transformations.html",
        "dataframe-engines.html",
        "downstream-paths.html",
    ):
        page = SITE / "course-data/extensions" / filename
        if page.exists() and "jupyter-download" in page.read_text(encoding="utf-8"):
            errors.append(f"{filename} must not expose an AsciiDoc-generated notebook toolbar")
    for stylesheet in sorted(SITE.rglob("*.css")):
        source = stylesheet.read_text(encoding="utf-8", errors="ignore")
        if re.search(r"url\(\s*['\"]?(?:https?:)?//", source):
            errors.append(
                f"{stylesheet.relative_to(SITE)}: stylesheet contains an external runtime asset"
            )
    if errors:
        print("Generated-site validation failed:")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)
    print(f"Generated-site validation passed: {len(pages)} HTML pages")


if __name__ == "__main__":
    main()
