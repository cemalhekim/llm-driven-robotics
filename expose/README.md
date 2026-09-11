# Bachelor thesis exposé

The exposé submitted for this thesis at TU Berlin, Fachgebiet Industrielle
Automatisierungstechnik. Source files exactly as exported from Overleaf.

| File | What it is |
|---|---|
| `main.tex` | The exposé itself — `article`, a4paper, 11pt |
| `references.bib` | Present in the export but unused; the bibliography is inline via `thebibliography` |
| `images/flow.drawio*.png` | System architecture flow diagram (drawio export) |
| `images/Online Gantt 20250428*.png` | Timeline Gantt chart |

Build with `pdflatex main.tex` (no bibtex pass needed).

> The preamble loads `\usepackage[ddmmyyyy]{isodate}`. `ddmmyyyy` is not an
> isodate option — the package treats an unknown option as a language name and
> aborts looking for `ddmmyyyy.idf` — so this **fails on a stock TeX Live**
> install. Overleaf tolerated it. The package also does not affect `\today`, so
> the line was inert even when it did load. Left as submitted; the master thesis
> template drops it.

Sections: Motivation and Problem Statement · State of Research · Objectives ·
Methodology · Strengths and Deliverables · Work Plan and Timeline · Bibliography.
