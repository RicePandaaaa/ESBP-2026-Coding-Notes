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
| `custom.scss` | Shared theme + band styling |
| `_quarto.yml` | Project config, navbar, HTML/PDF formats |
| `_site/` | Build output (git-ignored) |

## Render

Run from the repo root. Prefix with `uv run` so the project `.venv` (Jupyter
kernel) is on `PATH`:

```bash
uv run quarto preview           # live HTML while editing
uv run quarto render            # build the whole site into _site/
uv run quarto render --to pdf   # print-ready PDFs (needs TinyTeX)
```

## Authoring rules

- Generic examples only — no secure/graded quiz content.
- Week 1 scope: **no** `if/else`, loops, lists, or functions.
- Every sheet keeps the three bands: ⚠️ Watch out · ✅ Non-mutating check · 🔎 Show your evidence.
- Keep each sheet to ~one printed page.
