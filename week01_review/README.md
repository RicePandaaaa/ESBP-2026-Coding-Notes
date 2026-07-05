# Week 1 Review Sheets (Quarto project)

Scaffold for the student cheat/review sheets planned in
[`../PersonalNotes/week01_cheat_sheet_plan.md`](../PersonalNotes/week01_cheat_sheet_plan.md).

**Status:** outlines only. Each `.qmd` has section headings, band placeholders,
and table stubs marked with `<!-- TODO -->`. No finished review prose yet, and
**no secure quiz content** — author with generic examples.

## Files

| File | Sheet |
|---|---|
| `index.qmd` | Start-here / orientation |
| `00_glossary.qmd` | Terms & symbols (optional) |
| `01_output_vs_state.qmd` | Day 1 |
| `02_variables_expressions_state.qmd` | Day 2 |
| `03_types_casting_truthiness.qmd` | Day 3 |
| `04_comparisons_boundaries.qmd` | Day 4 |
| `05_boolean_combinations.qmd` | Day 5 |
| `06_traps_and_evidence.qmd` | Cross-cutting traps |
| `07_synthesis.qmd` | Week 1 synthesis / exam practice |
| `_includes/band-legend.qmd` | Shared band snippet |
| `custom.scss` | Shared theme + band styling |
| `_quarto.yml` | Project + HTML/PDF formats |

## Render

```bash
quarto preview           # live HTML while editing
quarto render            # build all sheets (HTML site in _site/)
quarto render --to pdf   # print-ready one-page PDFs
```

## Authoring rules (from the plan)

- Generic examples only — never the graded `flow_lpm` / `speed_mps` data.
- Scope: **no** `if/else`, loops, lists, or functions.
- Every sheet keeps the three bands: ⚠️ Watch out · ✅ Non-mutating check · 🔎 Show your evidence.
- Keep each sheet to ~one printed page.
