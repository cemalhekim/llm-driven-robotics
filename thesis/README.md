# Bachelor thesis, LaTeX source

The thesis document itself, as exported from Overleaf: *LLM-Guided Robot Control
System for On-Demand Task Planning and Execution in Self-Driving Environments*,
TU Berlin, Chair of Industrial Automation, written at BAM.

It is built on the chair's own thesis class, `Styles/Dokument/iat.cls`. Build with

```
pdflatex latex_am_iat && bibtex latex_am_iat && pdflatex latex_am_iat && pdflatex latex_am_iat
```

## Layout

| Path | What it is |
|---|---|
| `latex_am_iat.tex` | Main file. Pulls in the setup, the prolog, six chapters and the epilog |
| `Styles/Dokument/iat.cls` | The chair's document class: title page, headings, chapter numbering |
| `Styles/Literatur/*.bst` | Bibliography styles shipped with the class |
| `Setup/` | `header.tex` holds author, title, matriculation number and examiners; then packages, hyperref, headings, hyphenation and custom commands |
| `Prolog/` | Abstract, German summary, table of contents, lists of figures and tables, abbreviations, declaration of independent work, task description |
| `Kapitel_1` … `Kapitel_6` | Introduction, state of the art (eight included sections), and the remaining chapters |
| `Epilog/` | Appendix, bibliography, CV stub |
| `Images/` | Figures, mostly drawio exports |
| `Literatur/latex_am_iat.bib` | The bibliography |
| `appendix/userguide.pdf` | The user guide included as an appendix |

## Two things that were changed in the chair's class

Both were done for this thesis and are not part of the original template:

- `iat.cls` prints **"Bachelor's Thesis"** for the `ma` document-class option. In
  the unmodified class `ma` means *Masterarbeit* and `ba` means *Bachelorarbeit*;
  `latex_am_iat.tex` here passes `[ma]`, so the label was edited rather than the
  option.
- The BAM logo is hardcoded into the title page of `iat.cls`
  (`Prolog/Logos/BAM-Logo-2015.png`), alongside the chair's own logo.
