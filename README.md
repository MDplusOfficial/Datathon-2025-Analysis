# Datathon 2025 analysis

Analysis code for *AI Readiness, Technology Acceptance, and Digital Health
Literacy Among Medical Trainees After an Interdisciplinary Health Datathon:
Single-Group Pre-Post Mixed Methods Evaluation*.

Participant-level data are not included in this repository (see
`data/README.md`). The de-identified analysis dataset is available from the
corresponding author on reasonable request.

## Running

```
pip install -r requirements.txt
./run_all.sh
```

Results are written to `outputs/` and figures to `figures/`. Set
`DATATHON_DATA` to read the data from another folder.

## Contents

| | |
|---|---|
| `src/s00_build_dataset.py` | builds the de-identified dataset from the raw exports |
| `src/s01_participant_flow.py` | participant flow (Figure 1) and staged survey counts |
| `src/s02_demographics.py` | participant and team characteristics |
| `src/s03_survey.py` | pre-post survey analysis (Table 3, Multimedia Appendix 6) |
| `src/s04_appendix7.py` | selection into the paired analysis (Multimedia Appendix 7) |
| `src/s05_projects.py` | project characterization (Tables 1 and 2, Multimedia Appendix 4) |
| `src/s06_freetext.py` | free-text reflections (Multimedia Appendix 5, Figures 4 and 5) |
| `src/s07_figure2_demographics.py` | Figure 2 |
| `src/s08_figure3_survey.py` | Figure 3 |
| `src/common.py` | shared loaders and definitions |
| `notebooks/Diversity_and_Thematic_Analysis.ipynb` | team diversity analysis and free-text clustering |
| `data/coding/` | codebook coding of projects and the free-text clustering outputs |

The free-text clustering was run in the notebook in Google Colab; its outputs
are recorded in `data/coding/free_text_clusters.md`. The notebook also requires
scikit-learn and networkx.
