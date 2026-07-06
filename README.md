# ESBP-2026-Coding-Notes

Review sheets for students in Texas A&M's Engineering Summer Bridge Program
(2026 cohort). Built as a single [Quarto](https://quarto.org) website:
**ENGR 102 Bridge — Review Sheets**, covering four weeks of five daily sheets each.

## Structure

One project, one root `_quarto.yml`; each week is a subfolder.

| Path | Contents |
|---|---|
| `index.qmd` | Start-here / orientation landing page |
| `week01/` | Day 1–5 sheets (real content) |
| `week02/`–`week04/` | Day 1–5 stubs (placeholders) |
| `_includes/band-legend.qmd` | Shared band snippet |
| `custom.scss` | Shared theme + band styling (incl. `@media print` = PDF look) |
| `pdf-link.html` | Injects the per-sheet "Download PDF" link |
| `tools/make_pdfs.py` | Prints rendered HTML to PDF via headless Chrome/Edge |
| `_quarto.yml` | Project config, navbar, HTML format, published resources |
| `requirements.txt` | Python deps for Posit Connect Cloud (mirror of pyproject) |
| `_site/` | Build output (git-ignored) |

## Render

Run from the repo root. Prefix with `uv run` so the project `.venv` (Jupyter
kernel) is on `PATH`:

```bash
uv run quarto preview           # live HTML while editing
uv run quarto render            # build the whole site into _site/
uv run python tools/make_pdfs.py  # regenerate the per-sheet PDFs
```

### PDFs

Quarto's LaTeX PDF format is intentionally **not** used — it ignores the site
CSS (no red trap bands, no code backgrounds, wrong fonts, stretched images).
Instead, `tools/make_pdfs.py` prints each rendered HTML page through headless
Chrome, so the PDF is pixel-faithful to the website. The resulting
`weekXX/*.pdf` files are **committed to git** and published as static
resources (see `resources:` in `_quarto.yml`), because the deployment
environment has no browser. Re-run the script (and commit) whenever sheet
content changes.

## Publish (Posit Connect Cloud, free tier)

1. Push this repo to **GitHub — public** (the free tier only deploys public
   repos, and all published content is public).
2. At [connect.posit.cloud](https://connect.posit.cloud): **Publish → Quarto**,
   pick this repo/branch, confirm `_quarto.yml` as the project file.
3. Connect Cloud installs `requirements.txt`, runs `quarto render`, and hosts
   `_site/`. The committed `weekXX/*.pdf` files ride along as resources.
4. After content changes: re-render + re-run `make_pdfs.py` locally, commit,
   push, then hit **republish** on the Connect Cloud content page.

Free-tier limits to keep in mind: public content only, one concurrent build,
and the render must finish within the build timeout — this site is small, so
that is not a concern.

## Authoring rules

- Generic examples only — no secure/graded quiz content.
- Week 1 scope: **no** `if/else`, loops, lists, or functions.
- Every sheet keeps the three bands: ⚠️ Watch out · ✅ Non-mutating check · 🔎 Show your evidence.
- Keep each sheet to ~one printed page.
