#!/usr/bin/env python3
"""
Characterization of submitted projects: clinical domains (Table 1), patient
empowerment mechanisms (Table 2) and technical methods (Multimedia Appendix 4),
computed from the codebook coding.

Writes outputs/projects.json.
"""
import json
import os
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import OUT_DIR, ensure_dirs, load_dataset

N_PROJECTS = 31


def main():
    ensure_dirs()
    ds = load_dataset()

    projects = ds["projects"]
    counted = Counter(p["clinical_domain"] for p in projects)
    domains = [(d, counted[d], round(100 * counted[d] / N_PROJECTS),
                [p["project_id"] for p in projects
                 if p["clinical_domain"] == d])
               for d in sorted(counted, key=lambda d: (-counted[d], d))]
    seen = Counter(str(p).lower() for *_, plist in domains for p in plist)
    print("=" * 60)
    print("TABLE 1 - submitted projects by clinical domain")
    print("=" * 60)
    for name, n, pct, plist in domains:
        print("  %-36s%6d%7d%%" % (name, len(plist), pct))
    print("  %-36s%6d" % ("total", sum(len(p) for *_, p in domains)))
    print("  distinct domains: %d; projects in more than one domain: %d"
          % (len(domains), sum(1 for v in seen.values() if v > 1)))

    mechs = [(m["mechanism"], m["n_projects"]) for m in ds["empowerment_mechanisms"]]
    total = sum(n for _, n in mechs)
    mean = total / N_PROJECTS
    print()
    print("=" * 60)
    print("TABLE 2 - patient empowerment mechanisms")
    print("=" * 60)
    for name, n in mechs:
        print("  %-36s%6d%7d%%" % (name, n, round(100 * n / N_PROJECTS)))
    print("  %-36s%6d" % ("total assignments", total))
    print("  %-36s%6.1f" % ("mean per project", mean))

    methods = [{"method": m["method"], "stated": m["n_projects"],
                "counted": m["n_teams_listed"],
                "teams": [t.strip() for t in str(m["teams"]).split(";")]}
               for m in ds["technical_methods"] if m["kind"] == "ml"]
    print()
    print("=" * 60)
    print("MULTIMEDIA APPENDIX 4 - machine learning and statistical methods")
    print("=" * 60)
    for m in methods:
        print("  %-44s%6d" % (m["method"], m["counted"]))
    print("  distinct methods: %d" % len(methods))

    out = {
        "n_projects": N_PROJECTS,
        "domains": {name: len(p) for name, _, _, p in domains},
        "domain_projects": {name: p for name, _, _, p in domains},
        "mechanisms": {name: n for name, n in mechs},
        "mechanism_assignments": total,
        "mechanism_mean": round(mean, 2),
        "methods": methods,
    }
    with open(os.path.join(OUT_DIR, "projects.json"), "w") as fh:
        json.dump(out, fh, indent=2)
    print("\n  wrote %s" % os.path.normpath(os.path.join(OUT_DIR, "projects.json")))
    return out


if __name__ == "__main__":
    main()
