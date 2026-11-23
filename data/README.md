# Data

The analyses read one de-identified dataset, `datathon_dataset.xlsx`, built by
`src/s00_build_dataset.py` from the raw exports below. Data were collected under
an IRB exemption (Rutgers New Jersey Medical School, Pro2025002209), so neither
the dataset nor the raw exports are included here. The de-identified dataset is
available from the corresponding author on reasonable request.

## datathon_dataset.xlsx

Participants are identified as P001-P306 and teams as T01-T49; the file holds
no names or email addresses. The `dictionary` sheet defines every column and its
source.

| sheet | rows | contents |
|---|---|---|
| `meta` | | counts describing the source forms |
| `dictionary` | | column definitions |
| `participants` | 306 | registration, consent, characteristics, team membership, survey items |
| `teams` | 49 | registration and submission status, member counts |
| `projects` | 31 | clinical domain of each submitted project |
| `empowerment_mechanisms` | 6 | patient empowerment mechanisms |
| `technical_methods` | 31 | methods reported by each team |
| `freetext_responses` | 34 | reviewers' codes and sentiment for each reflection |
| `freetext_clusters` | 7 | cluster labels, definitions and response counts |
| `freetext_cooccurrence` | 7 | cluster co-occurrence |
| `freetext_silhouette` | 10 | consensus silhouette by number of clusters |

## Raw exports (not shared)

| file | contents |
|---|---|
| `presurvey.xlsx` | registration form with the pre-event survey (306 submissions, 292 registrants) |
| `postsurvey.xlsx` | post-event survey (92 submissions, 91 respondents) |
| `Manuscript Data (Combined).xlsx` | characteristics of consenting registrants |
| `Submissions.xlsx` | project submission form (34 submissions, 31 teams) and the reviewers' coding of the free-text reflections |
| `Datathon Team Registration (Responses).xlsx` | team registration form (220 named members across 48 teams; one further team submitted without filing it) |
| `2025 MD+ Datathon signup (Responses).xlsx` | full registration export |

## Coding files (included)

| file | contents |
|---|---|
| `coding/project_coding.md` | clinical domain and patient empowerment coding of the 31 projects |
| `coding/project_coding_narrative.md` | coding write-up, including the technical methods inventory |
| `coding/project_codes_raw.md` | initial codes for each project |
| `coding/project_domains.md` | projects by clinical domain |
| `coding/free_text_clusters.md` | outputs of the free-text clustering |

## Notes

- `team_label` is a participant's team; `registration_team_group` is the team
  name typed at registration, which Figure 2E groups by.
- Institution is free text. In `src/common.py`, `bucket_institution()` groups it
  for Figure 2 and `institution_identity()` resolves it for the institution
  count.
