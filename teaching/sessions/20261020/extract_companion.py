"""Stage the exported offline Plotly HTML for Antora, without authoring dependencies.

The versioned ZIP is a generated third-party JavaScript bundle, like other vendor
archives in this repository. Only the fixed HTML entry is read; no archive paths
are extracted. Recreate it with build.py --publish.
"""

from pathlib import Path
from zipfile import ZipFile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
NAME = "20261020-interactive.html"
OUT = ROOT / "build/teaching/20261020/site-companion"
with ZipFile(HERE / "exports/interactive.zip") as archive:
    assert archive.namelist() == [NAME]
    html = archive.read(NAME)
OUT.mkdir(parents=True, exist_ok=True)
(OUT / NAME).write_bytes(html)
print("Staged the offline Plotly companion for Antora")
