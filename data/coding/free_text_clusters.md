# Free-text consensus clustering — result tables

Inputs: the 21 usable free-text reflections and their reviewer-extracted codes,
which `src/s06_freetext.py` recomputes directly from the
`ThemeSentiment Reviewer Analysi` sheet of `../Submissions.xlsx`.

The clustering step itself (five-method consensus over a hybrid TF-IDF /
co-occurrence feature space, k = 3 to 12) was run once in
`Diversity_and_Thematic_Analysis.ipynb`. Its outputs are recorded here so that
the appendix, the figures and the Results text all read the same numbers, and so
that `s06_freetext.py` can check them against the raw coding sheet.

Labels are **clusters**, not themes: reviewer G12 asked that this analysis be
described as an exploratory organisational aid rather than a validated thematic
solution, and the wording is the same in the Abstract, Results, Discussion,
figure captions and Multimedia Appendix 5.

## Clusters

Short label is what appears in the manuscript, Multimedia Appendix 5 and the
figure axes. Long label is the descriptive name the clustering step produced.

| short_label | long_label | responses | strongly_positive | moderately_positive | neutral_mixed |
|---|---|---|---|---|---|
| Teamwork and logistics | Overall positive teamwork experience and logistics | 16 | 12 | 3 | 1 |
| Interdisciplinary collaboration | Interdisciplinary collaboration and practical constraints | 11 | 9 | 2 | 0 |
| Motivation, impact, and workload | Motivation, meaningful impact, and workload constraints | 8 | 6 | 2 | 0 |
| AI/ML skill building and onboarding | Applied AI/ML skill building and onboarding needs | 4 | 3 | 1 | 0 |
| Resources, support, and feedback | Program resources, support, and feedback structures | 4 | 4 | 0 | 0 |
| Educational growth and clarity | Educational growth and deliverable clarity | 3 | 2 | 1 | 0 |
| Peer learning and problem solving | Peer learning through exploratory problem solving | 3 | 3 | 0 | 0 |

## Cluster definitions (Multimedia Appendix 5B)

| short_label | definition |
|---|---|
| Teamwork and logistics | Cohesive team dynamics, effective communication and coordination, and overall positive experience, together with logistical or submission-related improvement needs. |
| Interdisciplinary collaboration | Value of interdisciplinary, multi-perspective teamwork and patient-centered or clinical application, alongside practical constraints such as cross-time-zone coordination or limited computing resources. |
| Motivation, impact, and workload | Participant motivation, a sense of meaningful patient-oriented impact, and workload or timeline constraints. |
| AI/ML skill building and onboarding | Hands-on AI/ML and prototyping skill development, alongside requests for more structured onboarding, time, mentorship, and dataset explanation. |
| Resources, support, and feedback | Helpful data access, examples, mentorship, feedback, and coordination support from the organizing team. |
| Educational growth and clarity | Educational and technical learning, alongside confusion or misalignment around deliverable expectations. |
| Peer learning and problem solving | Learning from peers, hands-on exploration, and creative problem-solving, including scoping challenges such as data limitations. |

## Co-occurrence (number of responses in which both clusters appear)

Rows and columns follow the cluster order above. The diagonal is zero by
construction.

| cluster | Teamwork and logistics | Interdisciplinary collaboration | Motivation, impact, and workload | AI/ML skill building and onboarding | Resources, support, and feedback | Educational growth and clarity | Peer learning and problem solving |
|---|---|---|---|---|---|---|---|
| Teamwork and logistics | 0 | 10 | 4 | 2 | 3 | 3 | 3 |
| Interdisciplinary collaboration | 10 | 0 | 5 | 1 | 2 | 3 | 2 |
| Motivation, impact, and workload | 4 | 5 | 0 | 2 | 1 | 1 | 0 |
| AI/ML skill building and onboarding | 2 | 1 | 2 | 0 | 1 | 0 | 0 |
| Resources, support, and feedback | 3 | 2 | 1 | 1 | 0 | 1 | 0 |
| Educational growth and clarity | 3 | 3 | 1 | 0 | 1 | 0 | 1 |
| Peer learning and problem solving | 3 | 2 | 0 | 0 | 0 | 1 | 0 |

## Consensus silhouette by candidate number of clusters

| k | consensus_silhouette |
|---|---|
| 3 | 0.120438 |
| 4 | 0.159863 |
| 5 | 0.108955 |
| 6 | 0.203874 |
| 7 | 0.270508 |
| 8 | 0.293897 |
| 9 | 0.311454 |
| 10 | 0.353382 |
| 11 | 0.377625 |
| 12 | 0.390213 |
