#!/usr/bin/env python3
"""
Builds the de-identified analysis dataset (data/datathon_dataset.xlsx) from the
raw exports: registration with the pre-event survey, the post-event survey, the
team registration form, the project submission form, and the coding files.

Records are linked across forms by email address and replaced with study IDs.
Team membership combines the team registration roster with each registrant's
self-reported team; the one team that submitted without filing a roster is
taken from self-report. Post-event respondents are counted as members of a
submitting team, since the survey went only to those teams.

Requires the raw exports, which contain identifiers and are not shared.
"""
import csv
import datetime
import os
import re
import sys
from collections import defaultdict

import openpyxl
from openpyxl.styles import Font
from openpyxl.utils import get_column_letter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C

OUT = os.path.join(C.DATA_DIR, "datathon_dataset.xlsx")
CROSSWALK = os.path.join(C.DATA_DIR, "_crosswalk_private.csv")
CODING = os.path.join(C.DATA_DIR, "coding", "project_coding.md")
NARRATIVE = os.path.join(C.DATA_DIR, "coding", "project_coding_narrative.md")
DOMAINS_MD = os.path.join(C.DATA_DIR, "coding", "project_domains.md")
CLUSTERS_MD = os.path.join(C.DATA_DIR, "coding", "free_text_clusters.md")

DICTIONARY = [
    ("participants", "participant_id",
     "P001-P306, assigned in email order across both surveys", "derived"),
    ("participants", "registered",
     "completed the registration form; y for 292, n for the 14 post-event "
     "respondents whose email matches no registration record",
     "pre-event survey"),
    ("participants", "consented",
     "consented to research use at registration; y for 264 of 292",
     "pre-event survey, LATEST submission per registrant"),
    ("participants", "pre_submissions",
     "how many times this person filled the registration form (1 or 2); "
     "sums to the 306 form rows", "pre-event survey"),
    ("participants", "degree_category",
     "Medical Student (MD/DO), Dual Degree, Master's Student, etc.",
     "registration sheet (latest); pre-event survey for the 28 non-consenters"),
    ("participants", "year_in_program", "integer; '6+' becomes 6", "as above"),
    ("participants", "motivation_category",
     "closed response options; free text falls into Other", "as above"),
    ("participants", "demographics_source",
     "which source the three columns above came from", "derived"),
    ("participants", "institution_canonical",
     "free-text institution resolved to a canonical name, or blank if the "
     "answer named no institution", "pre-event survey (covers all 292)"),
    ("participants", "institution_kind", "academic / hospital / blank",
     "derived"),
    ("participants", "institution_display",
     "the coarser bucketing Figure 2C plots, which sweeps unrecognised "
     "answers into Other", "derived"),
    ("participants", "international",
     "institution is outside the United States", "derived"),
    ("participants", "team_label",
     "the canonical team (T01-T49) this person named at registration; blank "
     "where they left it blank or named a team that neither registered nor "
     "submitted", "registration sheet + team registration form + submissions"),
    ("participants", "registration_team_group",
     "G01-G49, one per distinct team name typed at registration (the "
     "grouping used in Figure 2E); not the same grouping as team_label",
     "registration sheet"),
    ("participants", "on_a_team",
     "on any of the 49 teams, by the same reconciliation as on_submitting_team",
     "derived"),
    ("participants", "on_submitting_team",
     "their registration team submitted a project", "derived"),
    ("participants", "post_responded", "completed the post-event survey",
     "post-event survey"),
    ("participants", "post_consented",
     "consented to research use on the post-event survey",
     "post-event survey"),
    ("participants", "paired",
     "consented at both timepoints and has usable items at both; the 69",
     "derived"),
    ("participants", "comparison_group",
     "Multimedia Appendix 7 group: A in the paired analysis; B eligible, no "
     "paired data; C consented, not eligible", "derived"),
    ("participants", "pre_1 .. pre_13",
     "the 13 Likert items at registration, in instrument order R1-R6, A1-A4, "
     "D1-D3", "pre-event survey, EARLIEST submission containing answers"),
    ("participants", "post_1 .. post_13", "the same 13 items after the event",
     "post-event survey, LATEST submission"),
    ("teams", "team_label", "T01-T49", "derived"),
    ("teams", "registered", "filed the team registration form", "derived"),
    ("teams", "member_name_cells",
     "named members on the team registration form; sums to 220",
     "team registration form, latest filing per team"),
    ("teams", "distinct_members",
     "the same members resolved by email; sums to 218", "derived"),
    ("teams", "submitted", "submitted a project", "submission form"),
    ("teams", "submission_members",
     "members named on the submission form; sums to 149", "submission form"),
    ("teams", "consenting_members",
     "consenting registrants who named this team at registration",
     "registration sheet"),
    ("projects", "clinical_domain",
     "one of the 10 mutually exclusive domains in Table 1", "project coding"),
    ("projects", "team_label",
     "the team that submitted it, where the coding label names a team; blank "
     "where the coding label is the product name", "derived"),
    ("projects", "title",
     "the project title, as published in Table 1", "project coding"),
    ("technical_methods", "teams",
     "team labels that used the method; '?' where the coding file names the "
     "product rather than the team", "project coding"),
    ("freetext_responses", "codes_kb / codes_sm",
     "each coder's extracted codes, semicolon separated", "coder worksheet"),
    ("freetext_responses", "usable",
     "at least one coder extracted codes; the 21", "derived"),
]


def _md_table(path, heading):
    body = open(path).read().split(heading, 1)[1]
    out = []
    for line in body.splitlines():
        if line.startswith("#"):
            break
        if line.strip().startswith("|"):
            out.append(line.rstrip())
    return out


def _cells(line):
    return [c.strip().strip("*").strip() for c in line.strip().strip("|").split("|")]


def write_sheet(wb, name, header, rows, widths=None):
    ws = wb.create_sheet(name)
    ws.append(header)
    for c in ws[1]:
        c.font = Font(bold=True)
    for r in rows:
        ws.append(list(r))
    ws.freeze_panes = "A2"
    for i, h in enumerate(header, start=1):
        w = (widths or {}).get(h, min(max(12, len(str(h)) + 2), 44))
        ws.column_dimensions[get_column_letter(i)].width = w
    return ws


def build():
    pre_rows, pre = C.load_pre()
    post_rows, post = C.load_post()
    reg = C.load_registry()
    team_reg = C.load_team_registrations()
    subs = C.load_submissions()
    coding = C.load_free_text_coding()

    everyone = sorted(set(pre) | set(post))
    pid = {e: "P%03d" % (i + 1) for i, e in enumerate(everyone)}

    alias = {C.team_key(k): C.team_key(v) for k, v in C.TEAM_ALIASES.items()}

    def tkey(name):
        k = C.team_key(name)
        return alias.get(k, k)

    all_team_keys = set()
    for t in team_reg:
        all_team_keys.add(tkey(t))
    for t in subs:
        all_team_keys.add(tkey(t))
    tid = {k: "T%02d" % (i + 1) for i, k in enumerate(sorted(all_team_keys))}
    sub_keys = {tkey(t) for t in subs}

    consented = {e for e, r in pre.items() if r["consent"] == "yes"}
    post_c = {e for e, r in post.items()
              if r["consent"] in ("yes", "y", "true", "1")}
    paired = {e for e in consented if e in post_c
              and any(x is not None for x in pre[e]["items"])
              and any(x is not None for x in post[e]["items"])}
    cap_by_team, self_by_team = {}, {}
    for t, v in team_reg.items():
        cap_by_team.setdefault(tkey(t), []).extend(v["members"])
    for e, r in reg.items():
        t = (r.get("team") or "").strip()
        if t and t != "-":
            self_by_team.setdefault(tkey(t), []).append(e)

    def resolve(keys):
        found, unregistered, slots_reg = set(), [], 0
        for k in keys:
            slots = cap_by_team.get(k, [])
            named = list(self_by_team.get(k, []))
            matched, unmatched_slots = set(), []
            for m in slots:
                if m["email"] in pre:
                    matched.add(m["email"])
                    slots_reg += 1
                    if m["email"] in named:
                        named.remove(m["email"])
                else:
                    unmatched_slots.append(m)
            spare = [e for e in named if e not in matched]
            take = min(len(unmatched_slots), len(spare))
            matched.update(spare[:take])
            slots_reg += take
            if not slots:
                matched.update(spare)
            else:
                unregistered += [m["name"] for m in unmatched_slots[take:]]
            found |= matched
        return found, unregistered, slots_reg

    roster, never_registered, _ = resolve(sub_keys)
    roster_any, never_registered_any, named_registered = resolve(all_team_keys)
    on_submitting = roster | (set(post) & set(pre))
    on_sub = on_submitting & consented
    on_any_team = roster_any | (set(post) & set(pre))

    raw_teams = sorted({(r["team"] or "").strip() for r in reg.values()
                        if (r["team"] or "").strip() not in ("", "-")})
    gid = {t: "G%02d" % (i + 1) for i, t in enumerate(raw_teams)}

    p_header = (["participant_id", "registered", "consented", "pre_submissions",
                 "degree_category", "year_in_program", "motivation_category",
                 "demographics_source", "institution_canonical",
                 "institution_kind", "institution_display", "international",
                 "team_label", "registration_team_group", "on_a_team",
                 "on_submitting_team",
                 "post_responded",
                 "post_consented", "paired", "comparison_group"]
                + ["pre_%d" % i for i in range(1, 14)]
                + ["post_%d" % i for i in range(1, 14)])
    p_rows = []
    for e in everyone:
        r = pre.get(e)
        src = reg.get(e)
        demo = src or r
        inst = r["institution"] if r else None
        name, kind = C.institution_identity(inst)
        team = (src or {}).get("team") or ""
        grp = ("A" if e in paired else
               "B" if e in on_sub else
               "C" if e in consented else "")
        p_rows.append(
            [pid[e], "y" if r else "n",
             "y" if e in consented else "n",
             r["n_submissions"] if r else 0,
             C.bucket_degree(demo["degree"]) if demo else "",
             C.clean_year(demo["year"]) if demo else None,
             C.bucket_motivation(demo["motivation"]) if demo else "",
             ("registration sheet" if src else
              "pre-event survey" if r else "post-event survey only"),
             name or "", kind or "",
             C.bucket_institution(inst) if r else "",
             "y" if r and C.is_international(inst) else "n",
             tid.get(tkey(team), "") if team and team != "-" else "",
             gid.get(team, "") if team and team != "-" else "",
             "y" if e in on_any_team else "n",
             "y" if e in on_sub else "n",
             "y" if e in post else "n",
             "y" if e in post_c else "n",
             "y" if e in paired else "n", grp]
            + [(r["items"][i] if r else None) for i in range(13)]
            + [(post[e]["items"][i] if e in post else None) for i in range(13)])

    reg_by_key = {tkey(t): t for t in team_reg}
    sub_by_key = {tkey(t): t for t in subs}
    consenting_by_key = defaultdict(int)
    for e in consented:
        t = reg.get(e, {}).get("team") or ""
        if t and t != "-" and tkey(t) in tid:
            consenting_by_key[tkey(t)] += 1

    t_header = ["team_label", "registered", "member_name_cells",
                "distinct_members", "submitted", "submission_members",
                "consenting_members"]
    t_rows = []
    for k in sorted(all_team_keys):
        rt = team_reg.get(reg_by_key.get(k, ""), None)
        members = rt["members"] if rt else []
        distinct = set()
        for m in members:
            distinct.add(m["email"] if "@" in m["email"] else "name:" + m["name"])
        t_rows.append([tid[k], "y" if rt else "n", len(members), len(distinct),
                       "y" if k in sub_keys else "n",
                       len(subs.get(sub_by_key.get(k, ""), [])),
                       consenting_by_key.get(k, 0)])

    def to_team(label):
        k = tkey(label)
        if k in tid:
            return tid[k]
        for cand in all_team_keys:
            if k and (cand.startswith(k[:8]) or k.startswith(cand[:8])):
                return tid[cand]
        return ""

    proj_rows, proj_header = [], ["project_id", "clinical_domain",
                                  "team_label", "title"]
    domain_of = {}
    for line in _md_table(CODING, "# CLINICAL DOMAINS")[2:]:
        c = _cells(line)
        if len(c) < 4 or not c[0] or c[0].upper() == "TOTAL":
            continue
        for p in [x.strip() for x in c[3].split(",") if x.strip()]:
            domain_of[p] = c[0]
    titles = parse_titles()
    n = 0
    for label, dom in sorted(domain_of.items(), key=lambda kv: (kv[1], kv[0])):
        n += 1
        proj_rows.append(["PR%02d" % n, dom, to_team(label),
                          titles.get(dom, {}).pop(0) if titles.get(dom) else ""])

    mech_rows = []
    defs = {}
    for line in _md_table(CODING, "## Definitions")[2:]:
        c = _cells(line)
        if len(c) >= 2 and c[0]:
            defs[c[0]] = c[1]
    for line in _md_table(CODING, "## Frequencies")[2:]:
        c = _cells(line)
        if len(c) >= 3 and c[0]:
            mech_rows.append([c[0], int(re.sub(r"\D", "", c[1])),
                              int(re.sub(r"\D", "", c[2])), defs.get(c[0], "")])

    meth_rows = []
    for heading, kind in (
            ("## 1.1 Machine Learning / Statistical Methods", "ml"),
            ("## 1.2 Large Language Models & NLP Tools", "llm")):
        for line in _md_table(NARRATIVE, heading)[2:]:
            c = _cells(line)
            if len(c) < 3 or not c[0]:
                continue
            teams = [x.strip() for x in re.split(r",(?![^()]*\))", c[2])
                     if x.strip()]
            labels = [to_team(re.split(r"\s*\(", t)[0]) or "?" for t in teams]
            meth_rows.append([kind, c[0], int(re.sub(r"\D", "", c[1]) or 0),
                              len(teams) if kind == "ml" else "",
                              "; ".join(labels)])

    ft_header = ["response_id", "team_label", "has_text", "usable",
                 "n_codes_kb", "n_codes_sm", "codes_kb", "codes_sm",
                 "sentiment_kb", "sentiment_sm"]
    ft_rows = []
    for i, rec in enumerate(coding, start=1):
        usable = bool(rec["kb"] or rec["sm"])
        ft_rows.append(
            ["FR%02d" % i, tid.get(tkey(rec["team"]), ""),
             "y" if rec["text"] and str(rec["text"]).strip() else "n",
             "y" if usable else "n", len(set(rec["kb"])), len(set(rec["sm"])),
             "; ".join(sorted(set(rec["kb"]))), "; ".join(sorted(set(rec["sm"]))),
             rec["kb_sent"] or "", rec["sm_sent"] or ""])

    cl_header = ["short_label", "long_label", "responses", "strongly_positive",
                 "moderately_positive", "neutral_mixed", "definition"]
    cl_rows, cooc_rows, sil_rows = parse_clusters()

    meta = [
        ["built", datetime.date.today().isoformat(), ""],
        ["pre_event_form_rows", pre_rows,
         "rows on the registration form; 292 unique registrants"],
        ["post_event_form_rows", post_rows,
         "rows on the post-event survey; 91 unique respondents"],
        ["team_registration_form_rows", 49,
         "rows on the team registration form; 48 teams, DataSuture filed twice"],
        ["team_member_name_cells_raw", 225,
         "non-empty member-name cells across those 49 rows; 220 after dropping "
         "the earlier DataSuture filing"],
        ["submission_form_rows", 34,
         "rows on the project submission form; 31 unique teams, three filed twice"],
        ["teamform_members_not_submitting",
         sum(len(v["members"]) for t, v in team_reg.items()
             if tkey(t) not in sub_keys),
         "named members on the team registration form whose team did not "
         "submit a project"],
        ["teamform_members_submitting",
         sum(len(v["members"]) for t, v in team_reg.items()
             if tkey(t) in sub_keys),
         "named members on the team registration form whose team submitted "
         "a project"],
        ["submitting_members_consented", len(roster & consented),
         "named members of submitting teams who registered and consented"],
        ["eligible_not_on_any_roster", len((set(post) & set(pre)) - roster),
         "consenting registrants who completed the post-event survey but "
         "appear on no team roster"],
        ["submitting_members_unregistered", len(never_registered),
         "named members of the 31 submitting teams with no registration "
         "record"],
        ["named_members_registered", named_registered,
         "named team members who completed registration"],
        ["unregistered_submitting_teams", 1,
         "Artificially Intelligent submitted a project without registering, so "
         "the 220 member names cover 48 of the 49 teams"],
        ["free_text_code_assignments", 195,
         "each coder's contribution counted separately; 190 after "
         "de-duplicating within a response, 140 unique code strings"],
    ]

    wb = openpyxl.Workbook()
    wb.remove(wb.active)
    write_sheet(wb, "meta", ["key", "value", "note"], meta,
                {"note": 70, "key": 32})
    write_sheet(wb, "dictionary", ["sheet", "column", "meaning", "source"],
                DICTIONARY, {"meaning": 60, "source": 46, "column": 24})
    write_sheet(wb, "participants", p_header, p_rows,
                {"institution_canonical": 38, "degree_category": 26,
                 "motivation_category": 20, "demographics_source": 20,
                 "institution_display": 38})
    write_sheet(wb, "teams", t_header, t_rows)
    write_sheet(wb, "projects", proj_header, proj_rows,
                {"title": 90, "clinical_domain": 22, "coding_label": 24})
    write_sheet(wb, "empowerment_mechanisms",
                ["mechanism", "n_projects", "pct_of_projects", "definition"],
                mech_rows, {"definition": 90, "mechanism": 32})
    write_sheet(wb, "technical_methods",
                ["kind", "method", "n_projects", "n_teams_listed", "teams"],
                meth_rows, {"teams": 70, "method": 40})
    write_sheet(wb, "freetext_responses", ft_header, ft_rows,
                {"codes_kb": 70, "codes_sm": 70})
    write_sheet(wb, "freetext_clusters", cl_header, cl_rows,
                {"definition": 90, "short_label": 34, "long_label": 46})
    write_sheet(wb, "freetext_cooccurrence", ["cluster"] + [r[0] for r in cl_rows],
                cooc_rows, {"cluster": 34})
    write_sheet(wb, "freetext_silhouette", ["k", "consensus_silhouette"],
                sil_rows)
    wb.save(OUT)

    with open(CROSSWALK, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["participant_id", "email"])
        for e in everyone:
            w.writerow([pid[e], e])
        w.writerow([])
        w.writerow(["team_label", "team_name_registration", "team_name_submission"])
        for k in sorted(all_team_keys):
            w.writerow([tid[k], reg_by_key.get(k, ""), sub_by_key.get(k, "")])

    return {"participants": len(p_rows), "teams": len(t_rows),
            "projects": len(proj_rows), "mechanisms": len(mech_rows),
            "methods": len(meth_rows), "freetext": len(ft_rows),
            "clusters": len(cl_rows)}


def parse_titles():
    out = defaultdict(list)
    if not os.path.exists(DOMAINS_MD):
        return out
    cur = None
    for line in open(DOMAINS_MD):
        if not line.strip().startswith("|"):
            continue
        c = _cells(line)
        if len(c) < 2:
            continue
        m = re.match(r"(.+?)\s*\(n=\d+", c[0])
        if m:
            cur = m.group(1).strip()
        elif cur and not c[0] and c[1] and not c[1].startswith("-"):
            out[cur].append(c[1])
    return out


def parse_clusters():
    rows, cooc, sil = [], [], []
    defs = {}
    for line in _md_table(CLUSTERS_MD,
                          "## Cluster definitions (Multimedia Appendix 5B)")[2:]:
        c = _cells(line)
        if len(c) >= 2 and c[0]:
            defs[c[0]] = c[1]
    for line in _md_table(CLUSTERS_MD, "## Clusters")[2:]:
        c = _cells(line)
        if len(c) >= 6 and c[0]:
            rows.append([c[0], c[1], int(c[2]), int(c[3]), int(c[4]), int(c[5]),
                         defs.get(c[0], "")])
    for line in _md_table(
            CLUSTERS_MD,
            "## Co-occurrence (number of responses in which both clusters appear)")[2:]:
        c = _cells(line)
        if c[0]:
            cooc.append([c[0]] + [int(x) for x in c[1:8]])
    for line in _md_table(
            CLUSTERS_MD,
            "## Consensus silhouette by candidate number of clusters")[2:]:
        c = _cells(line)
        if c[0]:
            sil.append([int(c[0]), float(c[1])])
    return rows, cooc, sil


def main():
    counts = build()
    print("=" * 72)
    print("BUILD — single analysis dataset")
    print("=" * 72)
    for k, v in counts.items():
        print("  %-24s %d rows" % (k, v))
    print("\n  wrote %s" % os.path.normpath(OUT))
    print("  wrote %s   <- PII, gitignored, never share"
          % os.path.normpath(CROSSWALK))


if __name__ == "__main__":
    main()
