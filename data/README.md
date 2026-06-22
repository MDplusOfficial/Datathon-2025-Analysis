# Data

The raw survey exports are not included in this repository because they contain
participant names and email addresses (PII) collected under an IRB-exempt protocol.

**To request access**, contact the corresponding author. Collaborators should place
the files listed below in this folder (or set `DATATHON_DATA=/path/to/data`).

---

## Expected files

| File | Used by | Description |
|------|---------|-------------|
| `presurvey.xlsx` | `survey/survey_analysis.py`, `survey/figure2.py` | Signup + pre-survey (306 rows). Col 1: email; col 5: consent; cols 6–18: 13 Likert items (1–5). |
| `postsurvey.xlsx` | `survey/survey_analysis.py`, `survey/figure2.py` | Post-survey (92 rows). Col 1: email; col 2: consent; cols 3–15: same 13 items. |
| `Manuscript Data (Combined).xlsx` | `diversity/demographics_and_diversity.ipynb` | Combined registration + survey export. The `Group Dynamic Analysis` sheet (participant demographics + team names) drives Figure 1. |
| `Thematic_Data_2.csv` | `thematic/thematic_analysis.ipynb` | Two-coder coded free-text reflections; input to the clustering pipeline (Figures 3–4, Supp. Fig. S1). |
| `Manuscript_Teams.csv` | `thematic/thematic_analysis.ipynb` | Team roster (contains names). |
| `prepostresults.R` | `original/` | Authors' original R survey pipeline. |

---

## Likert items (column order in both exports)

| # | Short label | Construct |
|---|-------------|-----------|
| 0 | Explain core AI concepts | Medical AI Readiness (MAIRS-MS) |
| 1 | Identify AI-appropriate problems | Medical AI Readiness |
| 2 | Interpret AI outputs | Medical AI Readiness |
| 3 | Ethical responsibilities | Medical AI Readiness |
| 4 | Collaborate with non-clinical | Medical AI Readiness |
| 5 | Vision for AI empowerment | Medical AI Readiness |
| 6 | AI tools useful for patients | AI Technology Acceptance (TAM) |
| 7 | AI improves care effectiveness | AI Technology Acceptance (TAM) |
| 8 | Intend to recommend AI | AI Technology Acceptance (TAM) |
| 9 | Confident addressing AI questions | AI Technology Acceptance (TAM) |
| 10 | Find digital health resources | Digital Health Literacy |
| 11 | Judge digital health quality | Digital Health Literacy |
| 12 | Use digital tools for self-mgmt | Digital Health Literacy |
