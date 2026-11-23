#!/usr/bin/env bash
# Runs every analysis and draws the code-generated figures.
#
#   ./run_all.sh
#   DATATHON_DATA=/path/to/data ./run_all.sh
set -euo pipefail
cd "$(dirname "$0")"
PY="${PYTHON:-python3}"

# Building the dataset needs the raw exports, which are not shared.
if [ -f data/presurvey.xlsx ]; then
  "$PY" src/s00_build_dataset.py
fi

"$PY" src/s01_participant_flow.py
"$PY" src/s02_demographics.py
"$PY" src/s03_survey.py
"$PY" src/s04_appendix7.py
"$PY" src/s05_projects.py
"$PY" src/s06_freetext.py --figures
"$PY" src/s07_figure2_demographics.py
"$PY" src/s08_figure3_survey.py
