# Reproducible analysis package

Analysis code for *AI Readiness, Technology Acceptance, and Digital Health
Literacy Among Medical Trainees After an Interdisciplinary Health Datathon:
Single-Group Pre-Post Mixed Methods Evaluation*.

> **Data.** No participant data is in this repository. The analyses run off a
> single de-identified file, `data/datathon_dataset.xlsx`, which is
> participant-level data under an IRB-exempt protocol and is therefore shared
> on request rather than posted. Write to the corresponding author for it, drop
> it in `data/`, and everything below runs. `data/README.md` documents every
> column.

One command regenerates every number, table and figure in the paper and then
checks each one against what the manuscript reports:

```bash
pip install -r requirements.txt
./run_all.sh
```

```
59 checks: 59 reproduce, 0 mismatch, 0 not derivable
```

`src/verify.py` is the short answer to "does the shared code produce the
reported analyses?". It runs every analysis, compares the result with the value
printed in the manuscript, names each place that value appears, and exits
non-zero if anything disagrees. The audit that got it to 59/59 is available
from the corresponding author.

## One dataset, built once

Everything runs off a single de-identified file, **`data/datathon_dataset.xlsx`**
(64 KB, eleven sheets). It is the only input the analyses read.

```
raw exports  ──►  s00_build_dataset.py  ──►  datathon_dataset.xlsx  ──►  s01..s10, verify
  six files        all linkage done here           one file               arithmetic only
```

`s00_build_dataset.py` is the only script that opens a raw export. It resolves
every piece of record linkage **once** — matching a team across three spellings,
deciding which of a participant's two registrations counts, resolving a
free-text institution — and freezes the result. Downstream code does arithmetic
on clean columns and cannot silently disagree with itself. That split is the
point: nearly every discrepancy this package was built to find came from the
same fuzzy match being re-derived, slightly differently, in two places.

If someone asks for the data, `datathon_dataset.xlsx` is the file to send. It
carries no name, no email and no team name: participants are P001-P306, teams
are T01-T49, and the project and method sheets reference teams by label too. The
only free text in it is project titles, which Table 1 publishes, and the coders'
extracted codes. The crosswalk back to real identities is written separately to
`data/_crosswalk_private.csv`, which is gitignored and must never be shared.

**Running from the dataset alone works.** With the six raw exports absent,
`run_all.sh` skips the build step and still reproduces all 59 values and all six
figures. A reviewer needs one file and the code, nothing else.

The dataset's own `meta` and `dictionary` sheets document every column and where
it came from, so it is readable without reference to this README.

## Layout

```
data/
  datathon_dataset.xlsx    the built dataset — the only thing analyses read
  _crosswalk_private.csv   ids -> names and emails; never share
  <six raw exports>        build inputs only (see data/README.md)
  coding/                  qualitative coding tables, build inputs only
src/                       s00 builds; s01-s10 analyse; verify.py reconciles
outputs/                   JSON results + the generated Multimedia Appendix 7
figures/                   full-resolution figures, plus figures/1200px
run_all.sh                 runs everything in order
```

## Scripts

| script | produces |
|---|---|
| `src/s00_build_dataset.py` | **the dataset**; the only script that reads a raw export |
| `src/common.py` | the loaders and coding rules the build uses, and `load_dataset()` / `cohorts()` for everything else |
| `src/s01_participant_flow.py` | Figure 1 counts, CHERRIES completion stages, Ethics paragraph |
| `src/s02_demographics.py` | Figure 2 panels; the Results paragraph on participants and teams |
| `src/s03_survey.py` | Table 3 and Multimedia Appendix 6 |
| `src/s04_appendix7.py` | Multimedia Appendix 7 (`--docx` writes the file) |
| `src/s05_projects.py` | Table 1, Table 2, Multimedia Appendix 4A |
| `src/s06_freetext.py` | Multimedia Appendix 5; `--figures` draws Figures 4-5 and S1 |
| `src/s07_figure3_survey.py` | Figure 3 |
| `src/s08_figure1_flow.py` | Figure 1 |
| `src/s09_figure2_demographics.py` | Figure 2 |
| `src/s10_resize_figures.py` | 1200-px copies, named as the manuscript numbers them |
| `src/verify.py` | the reconciliation table above |

Scripts are independent apart from `s08_figure1_flow.py`, which reads
`outputs/flow.json`, so run `s01` before it (or just use `run_all.sh`).

## Decisions the build freezes

**Pre-event survey de-duplication.** 306 form rows, 292 unique registrants.
Consent comes from each registrant's *latest* submission; item responses and
characteristics come from the *earliest* submission that actually contains
answers. Both failure modes exist in this dataset — one registrant re-registered
with a blank item block, another abandoned a first submission and finished it
three days later — so neither latest-wins nor earliest-wins alone is correct.
This split rule is why the consented denominator is **264**, not 263.

**The post-event survey was gated on project submission.** It went only to
members of the 31 teams that submitted a project, so post-event completion is
reported against **149**, not against all registrants. That single design fact
determines the Appendix 7 groups and the CHERRIES completion stages.

**Team counts come from two forms, each authoritative for one thing.** The team
registration form gives **220** named members across **48** teams, after dropping
DataSuture's earlier of two filings. One further team, Artificially Intelligent,
submitted a project without ever registering, which is why the paper reports
**49** teams while 220 covers only 48 of them. The submission form names every
member of every submitting team and gives **149** exactly. Ten teams registered
under a different name from the one they submitted under; the map is
`TEAM_ALIASES` in `common.py`.

**Two different partitions of participants into teams, both numbering 49.**
`team_label` is the canonical team. `registration_team_group` is the distinct
team-name *string* a participant typed at registration, which is what Figure 2E
groups by. They are not the same partition — two strings are variant spellings of
one team, and one team is missing entirely — and that both come to 49 is a
coincidence. The dataset carries both so neither analysis has to guess.

**Counting institutions is not the same as bucketing them for a chart.**
`institution_display` is the coarse bucketing Figure 2C plots, which sweeps
unrecognised answers into `Other`. `institution_canonical` and
`institution_kind` are the census behind "292 registrants from 84 institutions",
which opens those buckets up and classifies every answer as an academic
institution, a teaching hospital, or not an institution at all.

**Effect size** is r = Z / sqrt(N) with N = 69 paired respondents, not the number
of non-tied pairs.

**Table 1 and Table 2 are derived, not transcribed.** `s05_projects.py` counts
the `projects` sheet for Table 1, and for Table 2 checks each stated % against
N/31 and derives the 50 assignments and the 1.6 mean from the N column rather
than storing them.

**Clusters, not themes.** The free-text clustering is an exploratory
organisational aid, not a validated thematic solution, and the labels are
identical in the Abstract, Results, Discussion, figure captions and Multimedia
Appendix 5.

## What is not recomputed here

The consensus clustering itself (five methods, k = 3 to 12, over a hybrid
TF-IDF / co-occurrence feature space) ran once in the original notebook. Its
outputs are carried in the dataset's three `freetext_*` sheets;
`s06_freetext.py` recomputes the *inputs* (21 usable responses, 140 unique codes,
195 code assignments) from the coder columns and checks the recorded outputs for
internal consistency against them — sentiment must sum to each cluster's response
count, the co-occurrence matrix must be symmetric with a zero diagonal, and no
pair may co-occur more often than the smaller of the two clusters.
