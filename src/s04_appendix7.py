#!/usr/bin/env python3
"""
s04_appendix7.py — Multimedia Appendix 7, baseline characteristics by
post-event survey completion.

The comparison assesses SELECTION INTO THE PAIRED ANALYSIS: participants who
contributed paired data against other eligible participants who could have
contributed paired data but did not. Three mutually exclusive groups, together
the whole consenting cohort:

  A  included in the paired analysis                       (n=69)
  B  eligible, did not contribute paired data              (n=75)
  C  not eligible, because their team did not submit       (n=120)

An earlier version of this table labelled group B "received the post-event
survey and did not complete it". That was never what B held: B is everyone
eligible who did not end up in the paired analysis, which includes people who
DID complete the post-event survey but declined research use of that response.
The count was also built off a different roster from the one Figure 1 uses, so
the groups did not nest inside the figure. Both are fixed here.

Composite SCORES come from the pre-event survey. Degree, year and motivation
come from the registration sheet, which is the record Figure 2 plots, so this
table cannot contradict that figure.

Writes outputs/appendix7.json and, with --docx, the appendix itself.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import (COMPOSITES, OUT_DIR, cohorts, composite, ensure_dirs,
                    mean_sd, smd_continuous, smd_proportion)

KEEP_DEGREE = ["Medical Student (MD/DO)", "Dual Degree (MD/PhD, MD/MS)",
               "Master's Student"]
KEEP_MOTIV = ["Learn AI Skills", "Publication", "Networking"]
DEGREE_LABEL = {"Medical Student (MD/DO)": "Medical student (MD/DO)",
                "Dual Degree (MD/PhD, MD/MS)": "Dual degree (MD/PhD, MD/MS)",
                "Master's Student": "Master's student", "Other": "Other"}
MOTIV_LABEL = {"Learn AI Skills": "Learning AI skills",
               "Publication": "Publication", "Networking": "Networking",
               "Other": "Other"}

NOTE = (
    "Baseline scores are pre-event survey composites on 5-point Likert scales. "
    "The post-event survey was distributed only to members of the 31 teams that "
    "submitted a project, so a participant was eligible to contribute paired "
    "data only if their team submitted; 144 consenting registrants were "
    "eligible on that basis. The submission forms name 149 members of those "
    "teams; 145 had completed registration and 140 of those consented. A "
    "further 4 consenting registrants completed the post-event survey but "
    "appear on no team roster, so the eligible denominator is 140 + 4 = 144. "
    "Figure 1 counts members NAMED on the team-registration and "
    "project-submission forms through project submission and people "
    "thereafter, so its upper boxes do not subtract to the exclusions beside "
    "them: the 220 named members include 20 who never registered, 208 "
    "registrants were on a team in all, and within the team-registration "
    "form 145 of the 220 were on submitting teams and 75 were not. "
    "The three groups are mutually exclusive and "
    "comprise all 264 consenting registrants; those who did not consent, or did "
    "not complete the pre-event survey, fall outside all of them. Of the 75 "
    "eligible participants who did not contribute paired data, 71 did not "
    "complete the post-event survey and 4 completed it but did not consent to "
    "research use of that response. SMD = standardised mean difference; an "
    "absolute value below 0.2 denotes negligible imbalance. Degree and "
    "motivation categories follow Figure 2."
)


def build():
    c = cohorts()
    P = c["P"]
    A, B, C = sorted(c["group_A"]), sorted(c["group_B"]), sorted(c["group_C"])
    groups = [A, B, C]

    rows = []

    def add_cont(label, fn):
        series = [[fn(e) for e in g] for g in groups]
        cells = []
        for s in series:
            m, sd, _ = mean_sd(s)
            cells.append("%.2f (%.2f)" % (m, sd) if m is not None else "-")
        smds = [smd_continuous(series[0], series[1]),
                smd_continuous(series[0], series[2])]
        rows.append((label, cells,
                     ["%+.2f" % v if v is not None else "-" for v in smds], False))

    for lbl, idx in COMPOSITES:
        add_cont("%s, mean (SD)" % lbl,
                 lambda e, i=idx: composite(P[e]["pre"], i))
    add_cont("Year in program, mean (SD)", lambda e: P[e]["year_in_program"])

    for field, keep, heading, labels in (
            ("degree_category", KEEP_DEGREE, "Degree program, n (%)",
             DEGREE_LABEL),
            ("motivation_category", KEEP_MOTIV,
             "Primary motivation, n (%)", MOTIV_LABEL)):
        rows.append((heading, ["", "", ""], ["", ""], True))
        cats = {}
        for gi, g in enumerate(groups):
            for e in g:
                cat = P[e][field]
                cat = cat if cat in keep else "Other"
                cats.setdefault(cat, [0, 0, 0])[gi] += 1
        for cat in keep + ["Other"]:
            cnt = cats.get(cat, [0, 0, 0])
            props = [cnt[i] / len(groups[i]) for i in range(3)]
            rows.append((
                "    " + labels[cat],
                ["%d (%.0f%%)" % (cnt[i], 100 * props[i]) for i in range(3)],
                ["%+.2f" % smd_proportion(props[0], props[1]),
                 "%+.2f" % smd_proportion(props[0], props[2])],
                False))

    # group B splits into non-responders and post-survey non-consenters
    responded_declined = sum(1 for e in B if P[e]["post_responded"] == "y")
    return rows, len(A), len(B), len(C), len(B) - responded_declined, responded_declined


def main():
    ensure_dirs()
    rows, na, nb, nc, no_response, declined = build()
    hdr = ["Characteristic", "Included in paired analysis (n=%d)" % na,
           "Eligible, did not contribute paired data (n=%d)" % nb,
           "Not eligible (n=%d)" % nc,
           "SMD (paired vs eligible)", "SMD (paired vs not eligible)"]
    print("=" * 104)
    print("MULTIMEDIA APPENDIX 7 — baseline characteristics by selection "
          "into the paired analysis")
    print("=" * 104)
    print("  %-38s%14s%14s%14s%11s%11s"
          % ("Characteristic", "A paired (%d)" % na, "B elig-unpaired (%d)" % nb,
             "C not elig (%d)" % nc, "SMD A-B", "SMD A-C"))
    for label, cells, smds, is_head in rows:
        print("  %-38s%14s%14s%14s%11s%11s"
              % (label, cells[0], cells[1], cells[2], smds[0], smds[1]))
    print("\n  groups: %d + %d + %d = %d consenting registrants"
          % (na, nb, nc, na + nb + nc))
    print("  eligible = %d (A + B); of the %d in group B, %d did not complete "
          "the post-event survey and %d completed it but declined research use"
          % (na + nb, nb, no_response, declined))

    out = {"n": {"A": na, "B": nb, "C": nc, "total": na + nb + nc},
           "B_split": {"no_response": no_response, "declined_consent": declined},
           "header": hdr, "note": NOTE,
           "rows": [{"label": l.strip(), "cells": c, "smd": s, "heading": h}
                    for l, c, s, h in rows]}
    with open(os.path.join(OUT_DIR, "appendix7.json"), "w") as fh:
        json.dump(out, fh, indent=2)
    print("  wrote %s" % os.path.normpath(os.path.join(OUT_DIR, "appendix7.json")))

    if "--docx" in sys.argv:
        write_docx(rows, na, nb, nc)
    return out


def write_docx(rows, na, nb, nc):
    import docx
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.shared import Pt

    def cell(c, text, bold=False, size=9.5, align=None):
        c.text = ""
        p = c.paragraphs[0]
        run = p.add_run(text)
        run.font.size = Pt(size)
        run.font.bold = bold
        if align:
            p.alignment = align

    doc = docx.Document()
    doc.add_heading("Multimedia Appendix 7. Baseline Characteristics of "
                    "Participants Included in the Paired Analysis, Other "
                    "Eligible Participants Who Did Not Contribute Paired Data, "
                    "and Registrants Who Were Not Eligible", level=1)
    headers = ["Characteristic", "Included in\npaired analysis\n(n=%d)" % na,
               "Eligible, no\npaired data\n(n=%d)" % nb,
               "Not\neligible\n(n=%d)" % nc,
               "SMD\n(paired vs\neligible)", "SMD\n(paired vs\nnot eligible)"]
    table = doc.add_table(rows=1, cols=6)
    table.style = "Table Grid"
    for i, h in enumerate(headers):
        cell(table.rows[0].cells[i], h, bold=True, size=10,
             align=WD_ALIGN_PARAGRAPH.CENTER if i else None)
    for label, vals, smds, is_head in rows:
        cells = table.add_row().cells
        cell(cells[0], label, bold=is_head)
        for i, v in enumerate(list(vals) + list(smds), start=1):
            cell(cells[i], v, align=WD_ALIGN_PARAGRAPH.CENTER)
    note = doc.add_paragraph()
    note.add_run(NOTE).font.size = Pt(9)
    dest = os.path.normpath(os.path.join(OUT_DIR, "Multimedia Appendix 7.docx"))
    doc.save(dest)
    print("  wrote %s" % dest)


if __name__ == "__main__":
    main()
