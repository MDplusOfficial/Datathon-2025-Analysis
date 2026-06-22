# Datathon 2025 — Analysis Code

Code for the quantitative and qualitative analyses in:

> *Bridging the AI Readiness Gap Among Clinicians: Results from a National, Interdisciplinary Health Datathon for Trainees*

---

## Repository structure

```
survey/
  survey_analysis.py       participant funnel, composite constructs, item-level statistics
  figure2.py               generates Figure 2 (panels A–E)

thematic/
  thematic_analysis.ipynb  theme prevalence, sentiment, co-occurrence → Figures 3–4, Supp. Fig. S1

diversity/
  demographics_and_diversity.ipynb   participant demographics + team composition → Figure 1

original/
  prepostresults.R         original R survey pipeline (available with data package)

data/
  README.md                expected data files, column schemas, de-identified dataset info
```

---

## Quickstart

```bash
pip install -r requirements.txt
export DATATHON_DATA=/path/to/data

python survey/survey_analysis.py   # prints funnel + composite + item-level tables
python survey/figure2.py           # writes figures/Figure2_revised.png
```

The notebooks in `thematic/` and `diversity/` are self-contained once the data package
is in place — open them in Jupyter and run all cells.

---

## Data availability

The data are not included in this repository. The datasets generated and analyzed during
the study are available from the corresponding author upon reasonable request. Raw survey
exports contain participant names and email addresses (PII) collected under an IRB-exempt
protocol and are not shared publicly.

See [`data/README.md`](data/README.md) for the file list and column schemas the analysis
code expects.

---

## Reproduced results

| Result | Script | Value |
|--------|--------|-------|
| Matched pre/post pairs | `survey_analysis.py` | n = 69 |
| Medical AI Readiness (MAIRS-MS, 6 items) | `survey_analysis.py` | Δ = +0.63, p < 0.001 |
| AI Technology Acceptance (TAM, 4 items) | `survey_analysis.py` | Δ = +0.43, p < 0.001 |
| Digital Health Literacy (3 items) | `survey_analysis.py` | Δ = +0.56, p < 0.001 |
| Largest item gain | `survey_analysis.py` | Identify AI-appropriate problems (+0.87) |
| Thematic clusters | `thematic_analysis.ipynb` | 7 themes, 140 codes, 21 reflections |
| Teams / matched members | `demographics_and_diversity.ipynb` | 49 teams, 190 members |

All p-values are Wilcoxon signed-rank with Benjamini–Hochberg correction.
