---
name: whimsical-diagrams
description: Create Whimsical diagrams for the review sheets. Use whenever asked to visualize a concept, draw a diagram, or illustrate how something works (variables, memory, control flow, data structures). Encodes the project's diagram-type decision rule, the Okabe-Ito colorblind-safe palette, and the verify-with-image loop.
---

# Whimsical diagrams for review sheets

Diagrams here teach intro-programming concepts to students. The goal is always
to show **the actual thing** (a memory box with a value in it, a list with
indexed slots, before/after states) — not an abstract process chart about it.

## 1. Pick the diagram type — boards are the default

**Default to `create(type:'board')`.** Concept visualization means drawing the
concept directly: labeled boxes, values inside them, before → after snapshots.
Flowcharts force everything into node-arrow-node grammar, which turns "a value
sitting in a box" into bureaucracy.

| Use | When |
| --- | --- |
| `board` (default) | Representing state: variables, memory, values changing, indexes, comparisons of before/after. Absolute positioning, shapes + free text. |
| `flowchart` | The concept genuinely IS a process with decisions/branches (loop execution, if/elif dispatch). |
| `mindmap` | Pure hierarchy/taxonomy (types of errors, categories of operators). |
| `sequence_diagram` | Actors exchanging messages over time. |

Required reading before creating: `how_to('board')` for boards,
`how_to('flowchart')` for flowcharts. (Mindmaps/sequence diagrams need no
how_to.)

## 2. Show change as adjacent snapshots

Re-assignment, mutation, evaluation order — show them as **two (or three)
concrete states side by side**, connected by a short labeled step, e.g.:

```
name (before)          name (after)
[ "Tony" ]  ──run──▶   [ "Adolin" ]
     └╌╌╌▶ [ "Tony" → thrown away ]
```

Never a single node "value gets overwritten". The student must SEE the old
value leave and the new value sitting in the same labeled box.

## 3. Colors: Okabe-Ito hex values (colorblind-safe)

Whimsical's `color` field accepts raw CSS hex — use these exact values, with
consistent meaning across all diagrams in the project:

| Hex | Okabe-Ito name | Meaning in our diagrams |
| --- | --- | --- |
| `#0072B2` | blue | a value currently in memory |
| `#999999` | gray | old / superseded state |
| `#D55E00` | vermillion | discarded / garbage / error |
| `#CC79A7` | reddish-purple (use `deco:'outline'`) | expression — not a value yet |
| `#E69F00` | orange | highlight / "look here" |
| `#009E73` | bluish-green | success / valid (never pair against vermillion as the ONLY cue) |

Rules:
- **Never** encode meaning in a red-vs-green contrast alone.
- Every colored shape also carries a **text label** — meaning must survive
  grayscale.
- Multi-panel boards get a small color key at the top.

## 4. Layout conventions for boards

- Left column: numbered section headers + the code line (`` `name = "Tony"` ``)
  + 2–3 lines of explanation text, all at `x: 0`.
- Visuals start around `x: 380`, one section per horizontal band, ~250px of
  vertical gap between sections.
- Keep explanation text in `text` items **short and pre-wrapped with `\n`** —
  long lines wrap unpredictably and collide with shapes.
- Variable names go as a small text label ABOVE the box, value inside the box.
- Straight connectors (`connector_type: 'straight'`) between snapshots;
  `deco: 'dashes'` for "discarded/implicit" relationships.

## 5. Verify — never ship unseen

After every create/edit:

```
fetch({ id: <board_id>, image: true })
```

Look at the PNG. Check: no overlapping text, headers not colliding with
shapes, connectors attached sensibly. If layout is broken, `delete` the file
and re-create with fixed coordinates (usually faster than incremental edits).

## 6. Getting diagrams into the Quarto site

Pages embed diagrams as **local PNGs** in `weekXX/images/` (e.g.
`![caption](./images/variable_diagram.png)`), NOT hotlinked Whimsical URLs —
the site and its PDFs must render offline. After the user approves a diagram,
remind them to export it as PNG into the right `images/` folder (the
`imageURL` thumbnail in the create response is low-res; use Whimsical's
export). Whimsical files live in the "Tamu" workspace, folder
"Week 1 — Variables & Assignment Diagrams" (or a sibling per-week folder).
