"""Print every rendered review sheet to PDF via headless Chrome/Edge.

Why this exists: Quarto's built-in `format: pdf` renders through LaTeX, which
ignores the site's CSS entirely — no red trap bands, no code-block
backgrounds, different fonts, images stretched to full page width. Printing
the *rendered HTML* through a real browser engine produces a PDF that looks
identical to the website (custom.scss's @media print block controls the
details).

Usage (from the project root):

    quarto render
    python tools/make_pdfs.py

The source .qmd files are the source of truth: one PDF is produced per
weekXX/*.qmd, written next to the .qmd AND into _site/. Anything stale —
HTML or PDF in _site, or PDF in the source tree, with no matching .qmd
(renamed/deleted pages) — is removed, so `quarto render`'s habit of never
purging old outputs can't leave dead pages or dead download links around.

The source-tree PDFs are committed to git and published by the `resources:`
entry in _quarto.yml — that way Posit Connect Cloud can serve them without
needing a browser at deploy time.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SITE_DIR = PROJECT_ROOT / "_site"

BROWSER_CANDIDATES = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    "/usr/bin/google-chrome",
    "/usr/bin/chromium",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
]


def find_browser() -> str:
    for candidate in BROWSER_CANDIDATES:
        if Path(candidate).exists():
            return candidate
    for name in ("chrome", "google-chrome", "chromium", "msedge"):
        found = shutil.which(name)
        if found:
            return found
    sys.exit("No Chrome/Edge found; install one or add its path to BROWSER_CANDIDATES.")


def print_to_pdf(browser: str, html: Path, pdf: Path) -> bool:
    result = subprocess.run(
        [
            browser,
            "--headless=new",
            "--disable-gpu",
            "--no-pdf-header-footer",
            f"--print-to-pdf={pdf}",
            str(html),
        ],
        capture_output=True,
        text=True,
        timeout=120,
    )
    return result.returncode == 0 and pdf.exists()


def clean_orphans(qmd_rels: set[Path]) -> None:
    """Remove _site html/pdf and source-tree pdfs whose .qmd is gone."""
    for html in SITE_DIR.glob("week*/*.html"):
        rel = html.relative_to(SITE_DIR)
        if rel.with_suffix(".qmd") not in qmd_rels:
            html.unlink()
            html.with_suffix(".pdf").unlink(missing_ok=True)
            print(f"  rm  _site/{rel} (+.pdf) — no matching .qmd")
    for pdf in list(SITE_DIR.glob("week*/*.pdf")) + list(PROJECT_ROOT.glob("week*/*.pdf")):
        rel = pdf.relative_to(SITE_DIR if pdf.is_relative_to(SITE_DIR) else PROJECT_ROOT)
        if rel.with_suffix(".qmd") not in qmd_rels:
            pdf.unlink()
            print(f"  rm  {pdf.relative_to(PROJECT_ROOT)} — no matching .qmd")


def main() -> None:
    if not SITE_DIR.exists():
        sys.exit("_site/ not found - run `quarto render` first.")

    qmds = sorted(PROJECT_ROOT.glob("week*/*.qmd"))
    if not qmds:
        sys.exit("No weekXX/*.qmd files found.")
    qmd_rels = {q.relative_to(PROJECT_ROOT) for q in qmds}

    clean_orphans(qmd_rels)

    browser = find_browser()
    failures: list[Path] = []
    stale: list[Path] = []
    for qmd in qmds:
        rel = qmd.relative_to(PROJECT_ROOT)          # week01/01_foo.qmd
        html = SITE_DIR / rel.with_suffix(".html")
        if not html.exists():
            stale.append(rel)
            print(f"SKIP  {rel}: not rendered yet — run `quarto render` first")
            continue

        site_pdf = html.with_suffix(".pdf")          # served next to the page
        source_pdf = qmd.with_suffix(".pdf")         # committed to git

        if print_to_pdf(browser, html, site_pdf):
            shutil.copyfile(site_pdf, source_pdf)
            print(f"  ok  {rel.with_suffix('.pdf')}")
        else:
            failures.append(rel)
            print(f"FAIL  {rel}")

    done = len(qmds) - len(failures) - len(stale)
    print(f"\n{done}/{len(qmds)} PDFs written.")
    if failures or stale:
        sys.exit(1)


if __name__ == "__main__":
    main()
