#!/usr/bin/env python3
"""
Selection into the paired analysis (Multimedia Appendix 7).

Baseline characteristics of the 264 consenting registrants in three groups:
  A  included in the paired analysis
  B  eligible (on a team that submitted a project), no paired data
  C  not eligible
compared using standardized mean differences (A vs B, A vs C).

Writes outputs/appendix7.json.
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
    print("MULTIMEDIA APPENDIX 7 - baseline characteristics by selection "
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
    print("  eligible = %d (A + B). Of the %d in group B, %d have no post-event "
          "response linked to their registration by email address, and %d "
          "completed the post-event survey but declined consent for use of "
          "post-event responses." % (na + nb, nb, no_response, declined))

    out = {"n": {"A": na, "B": nb, "C": nc, "total": na + nb + nc},
           "B_split": {"no_response": no_response, "declined_consent": declined},
           "header": hdr,
           "rows": [{"label": l.strip(), "cells": c, "smd": s, "heading": h}
                    for l, c, s, h in rows]}
    with open(os.path.join(OUT_DIR, "appendix7.json"), "w") as fh:
        json.dump(out, fh, indent=2)
    print("  wrote %s" % os.path.normpath(os.path.join(OUT_DIR, "appendix7.json")))

    return out


if __name__ == "__main__":
    main()
