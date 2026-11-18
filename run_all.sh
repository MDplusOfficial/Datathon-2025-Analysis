#!/usr/bin/env bash
# Regenerate every number, table and figure in the paper, then check them all
# against what the manuscript reports.
#
#   ./run_all.sh
#   DATATHON_DATA=/path/to/data ./run_all.sh
set -euo pipefail
cd "$(dirname "$0")"
PY="${PYTHON:-python3}"

# The build step needs the raw exports. Anyone working from the de-identified
# dataset alone can skip it: the dataset is the input to everything below.
if [ -f data/presurvey.xlsx ]; then
  echo "### build the dataset"
  "$PY" src/s00_build_dataset.py
else
  echo "### build skipped — no raw exports; using the dataset as shipped"
fi

echo
echo "### analyses"
"$PY" src/s01_participant_flow.py
"$PY" src/s02_demographics.py
"$PY" src/s03_survey.py
"$PY" src/s04_appendix7.py --docx
"$PY" src/s05_projects.py
"$PY" src/s06_freetext.py

echo
echo "### figures"
"$PY" src/s08_figure1_flow.py
"$PY" src/s09_figure2_demographics.py
"$PY" src/s07_figure3_survey.py
"$PY" src/s06_freetext.py --figures >/dev/null
"$PY" src/s10_resize_figures.py

echo
echo "### verification"
"$PY" src/verify.py
