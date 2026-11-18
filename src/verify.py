#!/usr/bin/env python3
"""
verify.py — assert every number the manuscript reports against the value this
codebase computes from the source data.

MANUSCRIPT below is a transcription of what the submitted manuscript, tables,
figures and appendices actually say. Nothing else in this package reads it; it
exists only so that a single command answers the reviewer's question — does the
shared code produce the reported analyses?

    python src/verify.py            # human-readable report
    python src/verify.py --json     # machine-readable

Exit status is 0 only if every check passes.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import s01_participant_flow
import s02_demographics
import s03_survey
import s04_appendix7
import s05_projects
import s06_freetext
from common import OUT_DIR, ensure_dirs

# --------------------------------------------------------------------------
# What the submitted manuscript says. "where" names every place a value
# appears, because a value is only reconciled when it agrees everywhere.
# --------------------------------------------------------------------------
MANUSCRIPT = [
    # (key, reported value, where it appears)
    ("registrants", 292, "Abstract; Results p1; Ethics; Figure 1; CHERRIES; GREET"),
    ("consented", 264, "Ethics; Results p1; Figure 1 note; CHERRIES; Appendix 7"),
    ("consent_pct", 90, "Ethics; Results p1; CHERRIES"),
    ("teams", 49, "Results p1; Figure 1; Figure 2E; GREET"),
    ("team_members", 220, "Results p1; Figure 1; CHERRIES; GREET"),
    ("team_members_distinct_people", 218, "not reported; 220 counts name slots"),
    ("registered_teams", 48, "not reported; 48 + Artificially Intelligent = 49"),
    ("submitting_teams", 31, "Abstract; Results; Methods; Table 1; Figure 1"),
    ("submitting_members", 149, "Abstract; Results p1; Figure 1; CHERRIES"),
    ("submitting_teams_pct", 63.3, "Results p1 (GREET says 63.2)"),
    ("post_respondents", 91, "Results p1; Figure 1; CHERRIES"),
    ("post_completion_pct", 61.1, "Results p1; CHERRIES"),
    ("paired", 69, "Abstract; Results; Table 3; Figure 3; Appendix 6/7"),
    ("paired_pct_of_post", 75.8, "Results p1; CHERRIES"),
    ("reached_submission_pct", 67.7, "CHERRIES"),
    ("institutions", 84, "Abstract; Results p1; GREET (academic, all 292)"),
    ("international", 21, "Results p1"),
    ("international_pct", 8, "Results p1"),
    ("motivation_learn_ai", 142, "Results p1; Figure 2D"),
    ("motivation_publication", 53, "Results p1; Figure 2D"),
    ("motivation_networking", 51, "Results p1; Figure 2D"),
    ("teams_multi_institution", 21, "Results p1; Figure 2E"),
    ("teams_multi_institution_pct", 42.9, "Results p1"),
    ("teams_multi_degree", 22, "Results p1; Figure 2E"),
    ("teams_multi_degree_pct", 44.9, "Results p1"),
    ("clinical_domains", 10, "Abstract; Results; Discussion; Table 1"),
    ("ml_methods", 13, "Results; Appendix 4A"),
    ("empowerment_mechanisms", 6, "Abstract; Results; Table 2; Appendix 4"),
    ("empowerment_assignments", 50, "Results"),
    ("empowerment_mean", 1.6, "Results"),
    ("free_text_reflections", 31, "Methods; Results"),
    ("free_text_usable", 21, "Methods; Results; Limitations; Appendix 5"),
    ("free_text_codes", 140, "Methods; Results; Limitations"),
    ("free_text_assignments", 195, "Methods; Results; Limitations"),
    ("clusters", 7, "Results; Appendix 5; Figures 4-5"),
    ("readiness_pre", 3.61, "Abstract; Results; Table 3; Appendix 7"),
    ("readiness_post", 4.24, "Abstract; Results; Table 3"),
    ("acceptance_pre", 3.93, "Abstract; Results; Table 3; Appendix 7"),
    ("acceptance_post", 4.36, "Abstract; Results; Table 3"),
    ("literacy_pre", 3.67, "Abstract; Results; Table 3; Appendix 7"),
    ("literacy_post", 4.23, "Abstract; Results; Table 3"),
    ("r_min", 0.52, "Results; Discussion; Table 3"),
    ("r_max", 0.71, "Results; Discussion; Table 3"),
    ("item_n_min", 67, "Methods"),
    ("item_n_max", 69, "Methods"),
    ("appendix7_A", 69, "Appendix 7; response to G2/Y2"),
    ("appendix7_B", 75, "Appendix 7; Results; response to G2/Y2"),
    ("appendix7_C", 120, "Appendix 7; response to G2/Y2"),
    ("appendix7_B_no_response", 71, "Appendix 7 note"),
    ("appendix7_B_declined", 4, "Appendix 7 note"),
    ("max_attrition_smd_composites", 0.17, "Results; Limitations; response to Y2"),
    ("selection_smd_year", -0.43, "Results; response to Y2"),
    ("year_paired", 1.80, "Results; Appendix 7"),
    ("year_not_eligible", 2.38, "Results; Appendix 7"),
    ("cluster_top_n", 16, "Results; Appendix 5"),
    ("cluster_top_pct", 76.2, "Results; Appendix 5"),
    ("cluster_2_pct", 52.4, "Results; Appendix 5"),
    ("cluster_3_pct", 38.1, "Results; Appendix 5"),
    ("cooc_top", 10, "Results; Figure 5"),
]

# Notes attached to individual checks, printed when one does not pass. Empty
# while everything either reproduces or is a known open coding question.
UNVERIFIABLE = {}


def collect():
    """Run every analysis script once and flatten its results."""
    flow = s01_participant_flow.main()
    demo = s02_demographics.main()
    surv = s03_survey.main()
    app7 = s04_appendix7.main()
    proj = s05_projects.main()
    free = s06_freetext.main()

    comp = {c["label"]: c for c in surv["composites"]}
    rows = {r["label"]: r for r in app7["rows"]}

    def smd(label, col):
        return float(rows[label]["smd"][col])

    return {
        "registrants": flow["registrants"],
        "consented": flow["consented"],
        "consent_pct": round(100 * flow["consented"] / flow["registrants"]),
        "teams": flow["teams"],
        "team_members": flow["team_members"],
        "team_members_distinct_people": flow["team_members_distinct_people"],
        "registered_teams": flow["registered_teams"],
        "submitting_teams": flow["submitting_teams"],
        "submitting_members": flow["submitting_team_members"],
        "submitting_teams_pct": flow["rates"]["teams_submitting"][2],
        "post_respondents": flow["post_respondents"],
        "post_completion_pct": flow["rates"]["post_completion_among_eligible"][2],
        "paired": flow["paired"],
        "paired_pct_of_post": flow["rates"]["paired_among_post_completers"][2],
        "reached_submission_pct": flow["rates"]["reached_submission"][2],
        "institutions": demo["institutions_academic"],
        "international": demo["international"],
        "international_pct": round(demo["international_pct"]),
        "motivation_learn_ai": demo["motivation_panel_d"]["Learn AI Skills"],
        "motivation_publication": demo["motivation_panel_d"]["Publication"],
        "motivation_networking": demo["motivation_panel_d"]["Networking"],
        "teams_multi_institution": demo["teams_multi_institution"][0],
        "teams_multi_institution_pct": demo["teams_multi_institution"][2],
        "teams_multi_degree": demo["teams_multi_degree"][0],
        "teams_multi_degree_pct": demo["teams_multi_degree"][2],
        "clinical_domains": len(proj["domains"]),
        "ml_methods": len(proj["methods"]),
        "empowerment_mechanisms": len(proj["mechanisms"]),
        "empowerment_assignments": proj["mechanism_assignments"],
        "empowerment_mean": round(proj["mechanism_mean"], 1),
        "free_text_reflections": flow["submitting_teams"],
        "free_text_usable": free["recomputed"]["usable_responses"],
        "free_text_codes": free["recomputed"]["unique_codes"],
        "free_text_assignments": free["recomputed"]["code_assignments"],
        "clusters": len(free["clusters"]),
        "readiness_pre": comp["Medical AI readiness"]["pre_mean"],
        "readiness_post": comp["Medical AI readiness"]["post_mean"],
        "acceptance_pre": comp["AI technology acceptance"]["pre_mean"],
        "acceptance_post": comp["AI technology acceptance"]["post_mean"],
        "literacy_pre": comp["Digital health literacy"]["pre_mean"],
        "literacy_post": comp["Digital health literacy"]["post_mean"],
        "r_min": min(c["r"] for c in surv["composites"]),
        "r_max": max(c["r"] for c in surv["composites"]),
        "item_n_min": surv["item_n_range"][0],
        "item_n_max": surv["item_n_range"][1],
        "appendix7_A": app7["n"]["A"],
        "appendix7_B": app7["n"]["B"],
        "appendix7_C": app7["n"]["C"],
        "appendix7_B_no_response": app7["B_split"]["no_response"],
        "appendix7_B_declined": app7["B_split"]["declined_consent"],
        "max_attrition_smd_composites": max(
            abs(smd(l, 0)) for l in ("Medical AI readiness, mean (SD)",
                                     "AI technology acceptance, mean (SD)",
                                     "Digital health literacy, mean (SD)",
                                     "Year in program, mean (SD)")),
        "selection_smd_year": smd("Year in program, mean (SD)", 1),
        "year_paired": float(rows["Year in program, mean (SD)"]["cells"][0].split()[0]),
        "year_not_eligible": float(
            rows["Year in program, mean (SD)"]["cells"][2].split()[0]),
        "cluster_top_n": free["clusters"][0]["responses"],
        "cluster_top_pct": round(
            100 * free["clusters"][0]["responses"]
            / free["recomputed"]["usable_responses"], 1),
        "cluster_2_pct": round(
            100 * free["clusters"][1]["responses"]
            / free["recomputed"]["usable_responses"], 1),
        "cluster_3_pct": round(
            100 * free["clusters"][2]["responses"]
            / free["recomputed"]["usable_responses"], 1),
        "cooc_top": max(free["cooccurrence"].values()),
    }


def main():
    ensure_dirs()
    computed = collect()

    results = []
    for key, reported, where in MANUSCRIPT:
        got = computed.get(key)
        if got is None:
            status = "UNVERIFIABLE"
        elif isinstance(reported, float) or isinstance(got, float):
            status = "OK" if abs(float(got) - float(reported)) < 0.005 else "MISMATCH"
        else:
            status = "OK" if got == reported else "MISMATCH"
        results.append({"key": key, "reported": reported, "computed": got,
                        "status": status, "where": where,
                        "note": UNVERIFIABLE.get(key, "")})

    if "--json" in sys.argv:
        print(json.dumps(results, indent=2))
    else:
        print()
        print("=" * 100)
        print("VERIFICATION — manuscript value vs value computed from source data")
        print("=" * 100)
        print("  %-32s%12s%12s%14s  %s"
              % ("value", "reported", "computed", "status", "appears in"))
        for r in results:
            print("  %-32s%12s%12s%14s  %s"
                  % (r["key"], r["reported"],
                     "-" if r["computed"] is None else r["computed"],
                     r["status"], r["where"][:46]))
        n_ok = sum(1 for r in results if r["status"] == "OK")
        n_bad = sum(1 for r in results if r["status"] == "MISMATCH")
        n_unv = sum(1 for r in results if r["status"] == "UNVERIFIABLE")
        print("\n  %d checks: %d reproduce, %d mismatch, %d not derivable"
              % (len(results), n_ok, n_bad, n_unv))
        for r in results:
            if r["status"] != "OK":
                print("\n  [%s] %s — manuscript says %s, code says %s"
                      % (r["status"], r["key"], r["reported"],
                         "nothing" if r["computed"] is None else r["computed"]))
                print("      appears in: %s" % r["where"])
                if r["note"]:
                    for line in _wrap(r["note"], 88):
                        print("      " + line)

    with open(os.path.join(OUT_DIR, "verification.json"), "w") as fh:
        json.dump(results, fh, indent=2)
    return 0 if all(r["status"] == "OK" for r in results) else 1


def _wrap(text, width):
    words, line, out = text.split(), "", []
    for w in words:
        if len(line) + len(w) + 1 > width:
            out.append(line)
            line = w
        else:
            line = (line + " " + w).strip()
    if line:
        out.append(line)
    return out


if __name__ == "__main__":
    sys.exit(main())
