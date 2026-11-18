# Data

## The file to send

**`datathon_dataset.xlsx`** is the single analysis dataset. It is built once by
`src/s00_build_dataset.py` from the raw exports below, and it is the only input
every analysis script reads. If someone asks for the data, this is the file.

It is de-identified: participants are P001-P306, teams are T01-T49, and it holds
no name, email or team name anywhere, including in the project-level sheets. The
only free text it carries is project titles, which Table 1 publishes, and the
coders' extracted codes. What it does hold is participant-level survey
responses and characteristics collected under an IRB-exempt protocol, so it is
shared on request rather than posted. `_crosswalk_private.csv` maps the ids back
to names and emails and must never leave the study team.

Its `dictionary` sheet defines every column and names the source it came from;
its `meta` sheet records the counts that are properties of the source forms
rather than of any row (306 registration submissions, 92 post-event submissions,
225 raw member-name cells, and so on).

Eleven sheets: `meta`, `dictionary`, `participants` (306), `teams` (49),
`projects` (31), `empowerment_mechanisms` (6), `technical_methods` (31),
`freetext_responses` (34), `freetext_clusters` (7), `freetext_cooccurrence` (7),
`freetext_silhouette` (10).

Running the pipeline with the raw exports absent still reproduces all 59 reported
values and all six figures from this file alone.

---

## Build inputs

These are read **only** by `s00_build_dataset.py`. They contain participant names,
email addresses and institutions collected under an IRB-exempt protocol
(Rutgers New Jersey Medical School, Pro2025002209).

**Before this package is published, remove the files marked PII below** and
leave this README in their place; the manuscript's data-availability statement
offers them from the corresponding author on reasonable request. `.gitignore`
already excludes them. The code reads `$DATATHON_DATA` if set, so a collaborator
who is given the files can point at them without moving anything.

| file | PII | what it is |
|---|---|---|
| `presurvey.xlsx` | yes | Registration + pre-event survey. 306 rows, 292 unique registrants. Col 1 email, col 2 degree, col 3 year, col 4 institution, col 5 consent, cols 6-18 the 13 Likert items, col 19 primary motivation. |
| `postsurvey.xlsx` | yes | Post-event survey. 92 rows, 91 unique respondents. Col 1 email, col 2 consent, cols 3-15 the same 13 items. |
| `Manuscript Data (Combined).xlsx` | yes | Combined export. The analyses use only the `Group Dynamic Analysis` sheet: 275 rows, 264 unique consenting registrants, with team name (col 2), degree (3), year (4), institution (5) and motivation (20). This is the record Figure 2 plots. |
| `Submissions.xlsx` | yes | Project submission form. Sheet `Form Responses 1`: 34 rows for 31 unique teams (Brunologix, The Washington Post and Trifusion each submitted twice), with the free-text team roster and the free-text reflection. Sheet `ThemeSentiment Reviewer Analysi`: the two coders' extracted codes and sentiment ratings for each reflection. |
| `Datathon Team Registration (Responses).xlsx` | yes | Team registration form, one row per team. 49 rows, 225 member-name cells; DataSuture filed twice (five members on 20 Oct, six on 27 Oct). Keeping the later row leaves **48 teams and 220 named members** — the figure the manuscript reports. Col 3 team name, cols 4/6/8/10/12/14 member names, cols 5/7/9/11/13/15 their emails. |
| `2025 MD+ Datathon signup (Responses).xlsx` | yes | The full registration workbook `presurvey.xlsx` is extracted from. `Form Responses 1` holds the same 306 responses and 292 unique emails, plus the team-name and team-finding columns the extract drops. `Sheet3` is a hand-harmonised institution list covering 231 of the 292 registrants (79 distinct values); it is kept for provenance and is **not** read by any script. |
| `coding/project_coding.md` | no | Clinical domain and patient-empowerment coding of the 31 projects, including the per-project matrix that Table 1 and Table 2 are computed from. |
| `coding/project_coding_narrative.md` | no | The full three-layer coding write-up. Sections 1.1 and 1.2 are the technical-methodology inventory behind Multimedia Appendix 4. |
| `coding/project_codes_raw.md` | no | The initial per-project code lists produced during familiarisation. |
| `coding/free_text_clusters.md` | no | Outputs of the free-text consensus clustering: cluster labels, definitions, response counts, sentiment, co-occurrence and silhouette by k. |

## Known gaps

* **Two partitions of participants into teams, both numbering 49.**
  `team_label` is the canonical team; `registration_team_group` is the distinct
  team-name string a participant typed at registration, which is what Figure 2E
  groups by. They are not the same partition and that both come to 49 is a
  coincidence. Both are in the dataset.

* **220 covers 48 of the 49 teams.** Artificially Intelligent submitted a
  project but never filed a team registration, so its members are absent from
  the team-registration export. The true headcount across all 49 teams is about
  226. 220 is what the form reproduces, and is what the manuscript reports.
  `s01_participant_flow.py` prints both, along with the 218 distinct people
  behind the 220 name slots.

* **The self-reported team name is the weakest of the three sources**: only 190
  of the 264 consenters filled it in, and 13 of those named a team that neither
  registered nor submitted. It drives Figure 2E and nothing else.

* **Institution is free text.** Two rules read it, on purpose.
  `bucket_institution()` is the display rule behind Figure 2C and panel E and
  sweeps unrecognised entries into `Other`. `institution_identity()` is the
  census rule: it resolves every string to an academic institution, a teaching
  hospital, or nothing, and yields **84 academic institutions** (87 with
  hospitals) across the 292 registrants. If a future export adds a string
  neither list covers, `s02_demographics.py` prints it under UNRESOLVED rather
  than quietly dropping it.
