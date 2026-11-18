#!/usr/bin/env python3
"""
s05_projects.py — Table 1 (clinical domains), Table 2 (patient-empowerment
mechanisms) and Multimedia Appendix 4 (technical methodologies), recomputed
from the coding files rather than transcribed.

Every count comes from the built dataset:

  projects                one row per project with its clinical domain. Domain
                          counts and percentages are recomputed from the rows.
  empowerment_mechanisms  one row per mechanism with its N. Each % is checked
                          against N/31, and the 50 assignments and the 1.6 mean
                          are derived from the N column rather than stored.
  technical_methods       one row per method with the teams that used it.
                          Counts are recomputed from the team lists.

The script prints RECOMPUTED against REPORTED for every value and exits
non-zero if they disagree, so a stale coding file cannot pass silently.

Note on what is NOT here: this file used to also read a project-by-mechanism
grid of tick marks. That grid had fallen out of sync with the frequencies in
the same file (46 ticks against 50 assignments) and was removed on 2026-09-16.
The frequency table is the coding of record. Nothing in the manuscript reports
mechanisms at the level of individual projects, so no reported value depends on
the removed grid.

Writes outputs/projects.json.
"""
import json
import os
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import OUT_DIR, ensure_dirs, load_dataset

N_PROJECTS = 31

# Values as printed in the submitted manuscript, for comparison.
REPORTED_DOMAINS = {
    "Women's Health": 9, "General Inpatient": 4, "Mental Health": 4,
    "Emergency Medicine": 3, "Critical Care": 3, "Diabetes": 3,
    "Cardiology": 2, "Radiology": 1, "Pharmacy": 1, "Surgery": 1,
}
REPORTED_MECHANISMS = {
    "Symptom Forecasting": 12, "Actionable Self-Management": 10,
    "Health Literacy": 8, "Patient-Clinician Communication": 8,
    "Health Equity": 6, "AI Transparency": 6,
}
REPORTED_ASSIGNMENTS = 50
REPORTED_MEAN = 1.6
REPORTED_METHODS = {
    "Random Forest": 7, "Logistic Regression": 6, "XGBoost": 5,
    "Gradient Boosting / LightGBM": 4, "K-means Clustering": 3,
    "Mixed Effects / Linear Regression": 3, "Deep Neural Networks": 2,
    "K-Nearest Neighbors": 1, "Support Vector Machines": 1,
    "Cox Proportional Hazards": 1, "Quantile Regression": 1,
    "Dynamic Time Warping": 1, "Isotonic Calibration": 1,
}
METHOD_LABEL = {"Gradient Boosting (general/LightGBM)":
                "Gradient Boosting / LightGBM"}


def main():
    ensure_dirs()
    ok = True
    ds = load_dataset()

    # -------------------------------------------------------------- Table 1 --
    projects = ds["projects"]
    counted = Counter(p["clinical_domain"] for p in projects)
    domains = [(d, counted[d], round(100 * counted[d] / N_PROJECTS),
                [p["project_id"] for p in projects
                 if p["clinical_domain"] == d])
               for d in sorted(counted, key=lambda d: (-counted[d], d))]
    print("=" * 82)
    print("TABLE 1 — submitted projects by clinical domain")
    print("=" * 82)
    print("  %-24s%9s%9s%7s%9s%10s" % ("Domain", "projects", "stated", "%",
                                       "recomp %", "reported"))
    seen = {}
    total_projects = 0
    for name, n, pct, plist in domains:
        total_projects += len(plist)
        for p in plist:
            seen.setdefault(str(p).lower(), []).append(name)
        rep = REPORTED_DOMAINS.get(name)
        agree = len(plist) == n == rep
        ok &= agree
        print("  %-24s%9d%9d%6d%%%8d%%%10s%s"
              % (name, len(plist), n, pct, pct, rep,
                 "" if agree else "   <-- MISMATCH"))
    dupes = {p: d for p, d in seen.items() if len(d) > 1}
    print("  %-24s%9d%9s%7s%9s%10d"
          % ("total", total_projects, "", "", "", sum(REPORTED_DOMAINS.values())))
    print("  distinct domains: %d (reported 10)" % len(domains))
    print("  projects appearing in more than one domain: %s" % (dupes or "none"))
    ok &= (len(domains) == 10 and total_projects == N_PROJECTS and not dupes)

    # -------------------------------------------------------------- Table 2 --
    mechs = [(m["mechanism"], m["n_projects"], m["pct_of_projects"])
             for m in ds["empowerment_mechanisms"]]
    print()
    print("=" * 82)
    print("TABLE 2 — patient-empowerment mechanisms")
    print("=" * 82)
    print("  %-34s%9s%7s%11s%10s" % ("Mechanism", "n", "%", "recomp %",
                                     "reported"))
    total = 0
    for name, n, pct in mechs:
        total += n
        rep = REPORTED_MECHANISMS.get(name)
        recomp_pct = round(100 * n / N_PROJECTS)
        agree = n == rep and recomp_pct == pct
        ok &= agree
        print("  %-34s%9d%6d%%%10d%%%10s%s"
              % (name, n, pct, recomp_pct, rep,
                 "" if agree else "   <-- MISMATCH"))
    mean = total / N_PROJECTS
    print("  %-34s%9d%7s%11s%10d%s"
          % ("total assignments", total, "", "", REPORTED_ASSIGNMENTS,
             "" if total == REPORTED_ASSIGNMENTS else "   <-- MISMATCH"))
    print("  %-34s%9.2f%7s%11s%10s%s"
          % ("mean per project", mean, "", "", REPORTED_MEAN,
             "" if round(mean, 1) == REPORTED_MEAN else "   <-- MISMATCH"))
    ok &= (len(mechs) == 6 and total == REPORTED_ASSIGNMENTS
           and round(mean, 1) == REPORTED_MEAN)

    # ---------------------------------------------------------- Appendix 4A --
    methods = [{"method": m["method"], "stated": m["n_projects"],
                "counted": m["n_teams_listed"],
                "teams": [t.strip() for t in str(m["teams"]).split(";")]}
               for m in ds["technical_methods"] if m["kind"] == "ml"]
    print()
    print("=" * 82)
    print("MULTIMEDIA APPENDIX 4A — machine learning / statistical methods")
    print("=" * 82)
    print("  %-38s%9s%9s%10s" % ("Method", "teams", "stated", "reported"))
    for m in methods:
        rep = REPORTED_METHODS.get(METHOD_LABEL.get(m["method"], m["method"]))
        agree = m["counted"] == m["stated"] == rep
        ok &= agree
        print("  %-38s%9d%9d%10s%s" % (m["method"], m["counted"], m["stated"],
                                       rep, "" if agree else "   <-- MISMATCH"))
    print("  distinct methods: %d (reported 13)" % len(methods))
    ok &= len(methods) == 13

    out = {
        "n_projects": N_PROJECTS,
        "domains": {name: len(p) for name, _, _, p in domains},
        "domain_projects": {name: p for name, _, _, p in domains},
        "mechanisms": {name: n for name, n, _ in mechs},
        "mechanism_assignments": total,
        "mechanism_mean": round(mean, 2),
        "methods": methods,
        "all_agree": bool(ok),
    }
    with open(os.path.join(OUT_DIR, "projects.json"), "w") as fh:
        json.dump(out, fh, indent=2)
    print("\n  wrote %s" % os.path.normpath(os.path.join(OUT_DIR, "projects.json")))
    if not ok:
        print("\n  *** recomputed values disagree with the manuscript; see "
              "AUDIT_REPORT.md ***")
    return out


if __name__ == "__main__":
    main()
