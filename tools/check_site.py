#!/usr/bin/env python3
"""Check that the generated site and its local links are complete."""

from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "public"
DEPLOYMENT_PREFIX = "/course-data"


class LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.targets: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        for name, value in attrs:
            if value and ((tag == "a" and name == "href") or name == "src"):
                self.targets.append(value)


def target_path(page: Path, target: str) -> Path | None:
    parsed = urlsplit(target)
    if parsed.scheme or parsed.netloc or target.startswith(("mailto:", "data:", "#")):
        return None
    clean = unquote(parsed.path)
    if not clean:
        return None
    if clean.startswith("/"):
        if clean == DEPLOYMENT_PREFIX:
            clean = "/"
        elif clean.startswith(f"{DEPLOYMENT_PREFIX}/"):
            clean = clean[len(DEPLOYMENT_PREFIX) :]
        return SITE / clean.lstrip("/")
    return (page.parent / clean).resolve()


def main() -> None:
    pages = sorted((SITE / "course-data").rglob("*.html"))
    if not pages:
        raise SystemExit("Generated site contains no HTML pages")
    errors: list[str] = []
    for page in pages:
        parser = LinkParser()
        parser.feed(page.read_text(encoding="utf-8"))
        for target in parser.targets:
            destination = target_path(page, target)
            if destination is None:
                continue
            candidates = [destination]
            if destination.suffix == "":
                candidates.extend([destination / "index.html", destination.with_suffix(".html")])
            if not any(candidate.exists() for candidate in candidates):
                errors.append(f"{page.relative_to(SITE)} -> {target}")
    notebook = SITE / "course-data/_attachments/notebooks/foundations/data-lifecycle.ipynb"
    if not notebook.exists():
        errors.append("Generated student notebook attachment is missing")
    if errors:
        print("Generated-site validation failed:")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)
    print(f"Generated-site validation passed: {len(pages)} HTML pages")


if __name__ == "__main__":
    main()
