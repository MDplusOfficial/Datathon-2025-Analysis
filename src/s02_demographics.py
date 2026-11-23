#!/usr/bin/env python3
"""
Participant and team characteristics (Results; Figure 2) for the 264
registrants who consented to research use of their data.

Writes outputs/demographics.json.
"""
import json
import os
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import OUT_DIR, cohorts, ensure_dirs


def main():
    ensure_dirs()
    c = cohorts()
    P = c["P"]
    reg = {k: P[k] for k in c["consented"]}
    n = len(reg)

    degree = Counter(r["degree_category"] for r in reg.values())
    year = Counter(r["year_in_program"] for r in reg.values())
    motivation = Counter(r["motivation_category"] for r in reg.values())
    institution = Counter(r["institution_display"] for r in reg.values())

    rare = [k for k, v in motivation.items() if v < 5 and k != "Other"]
    motivation_panel = Counter(motivation)
    for k in rare:
        motivation_panel["Other"] += motivation_panel.pop(k)

    intl = sum(1 for r in reg.values() if r["international"] == "y")

    pre = {k: v for k, v in P.items() if v["registered"] == "y"}
    census = {"academic": set(), "hospital": set()}
    for r in pre.values():
        if r["institution_kind"] in census:
            census[r["institution_kind"]].add(r["institution_canonical"])
    census["unresolved"] = set()

    teams = {}
    for e, r in reg.items():
        if r["registration_team_group"]:
            teams.setdefault(r["registration_team_group"], []).append(e)
    multi_inst = sum(1 for mem in teams.values()
                     if len({reg[e]["institution_display"] for e in mem}) >= 2)
    multi_deg = sum(1 for mem in teams.values()
                    if len({reg[e]["degree_category"] for e in mem}) >= 2)

    out = {
        "n": n,
        "n_registrants": len(pre),
        "institutions_academic": len(census["academic"]),
        "institutions_with_hospitals": (len(census["academic"])
                                        + len(census["hospital"])),
        "institutions_unresolved": sorted(census["unresolved"]),
        "degree": dict(degree.most_common()),
        "year": {str(k): v for k, v in sorted(year.items(),
                                              key=lambda kv: (kv[0] is None, kv[0]))},
        "motivation_raw": dict(motivation.most_common()),
        "motivation_panel_d": dict(motivation_panel.most_common()),
        "institution_categories": len(institution),
        "institution_named_categories": len(
            [k for k in institution if not k.startswith("Other")]),
        "institution_distinct_canonical": len(
            {r["institution_canonical"] for r in reg.values()
             if r["institution_canonical"]}),
        "international": intl,
        "international_pct": round(100 * intl / n, 1),
        "teams": len(teams),
        "team_members": sum(len(v) for v in teams.values()),
        "teams_multi_institution": [multi_inst, len(teams),
                                    round(100 * multi_inst / len(teams), 1)],
        "teams_multi_degree": [multi_deg, len(teams),
                               round(100 * multi_deg / len(teams), 1)],
        "institution_top": dict(sorted(institution.items(),
                                       key=lambda kv: (-kv[1], kv[0]))[:14]),
    }

    print("=" * 72)
    print("FIGURE 2 — participant demographics and team composition")
    print("=" * 72)
    print(f"  consenting registrants ............... {n}")
    print("\n  A. degree background")
    for k, v in degree.most_common():
        print(f"      {k:34s} {v:4d}")
    print(f"      {'sum':34s} {sum(degree.values()):4d}")
    print("\n  B. year in program")
    for k, v in sorted(year.items(), key=lambda kv: (kv[0] is None, kv[0])):
        print(f"      {str(k):34s} {v:4d}")
    print(f"      {'sum':34s} {sum(year.values()):4d}")
    print("\n  C. institutions")
    print(f"      distinct canonical ............. "
          f"{out['institution_distinct_canonical']}")
    print(f"      display categories (Figure 2C) . {out['institution_categories']}")
    print(f"      international .................. {intl} "
          f"({out['international_pct']}%)")
    print(f"\n      census over all {len(pre)} registrants")
    print(f"        academic institutions ........ {len(census['academic'])}")
    print(f"        teaching hospitals ........... {len(census['hospital'])} "
          f"({', '.join(sorted(census['hospital']))})")
    print(f"        academic + hospitals ......... "
          f"{len(census['academic']) + len(census['hospital'])}")
    if census["unresolved"]:
        print("        UNRESOLVED (needs a rule): "
              + "; ".join(sorted(census["unresolved"])))
    print("\n  D. primary motivation (panel, rare categories collapsed)")
    for k, v in motivation_panel.most_common():
        print(f"      {k:34s} {v:4d}")
    print(f"      {'sum':34s} {sum(motivation_panel.values()):4d}")
    print("\n  E. team composition")
    print(f"      teams .......................... {len(teams)}")
    print(f"      members with a team ............ {out['team_members']}")
    print(f"      >=2 institutions ............... "
          f"{multi_inst}/{len(teams)} = {out['teams_multi_institution'][2]}%")
    print(f"      >=2 degree categories .......... "
          f"{multi_deg}/{len(teams)} = {out['teams_multi_degree'][2]}%")

    with open(os.path.join(OUT_DIR, "demographics.json"), "w") as fh:
        json.dump(out, fh, indent=2)
    print(f"\n  wrote {os.path.normpath(os.path.join(OUT_DIR, 'demographics.json'))}")
    return out


if __name__ == "__main__":
    main()
