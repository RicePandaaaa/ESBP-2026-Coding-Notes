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

Output: one PDF per week-page, written next to the source .qmd (e.g.
week01/01_output_vs_state.pdf) AND into _site/ so a local preview works
immediately. The source-tree copies are committed to git and published by the
`resources:` entry in _quarto.yml — that way Posit Connect Cloud can serve
them without needing a browser at deploy time.
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


def main() -> None:
    if not SITE_DIR.exists():
        sys.exit("_site/ not found - run `quarto render` first.")

    browser = find_browser()
    pages = sorted(SITE_DIR.glob("week*/*.html"))
    if not pages:
        sys.exit("No rendered week pages found in _site/.")

    failures = []
    for html in pages:
        rel = html.relative_to(SITE_DIR)          # e.g. week01/01_output_vs_state.html
        site_pdf = html.with_suffix(".pdf")       # served next to the page
        source_pdf = PROJECT_ROOT / rel.with_suffix(".pdf")  # committed to git

        if print_to_pdf(browser, html, site_pdf):
            source_pdf.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(site_pdf, source_pdf)
            print(f"  ok  {rel.with_suffix('.pdf')}")
        else:
            failures.append(rel)
            print(f"FAIL  {rel}")

    print(f"\n{len(pages) - len(failures)}/{len(pages)} PDFs written.")
    if failures:
        sys.exit(1)


if __name__ == "__main__":
    main()
