#!/usr/bin/env python3
"""
s01_participant_flow.py — every count in Figure 1, the CHERRIES completion-rate
stages, and the Ethical Considerations paragraph.

The post-event survey was distributed only to members of the 31 teams that
submitted a project, so post-event completion is reported against that
denominator (149) rather than against all registrants.

Reads data/datathon_dataset.xlsx. Build it first with s00_build_dataset.py.
Writes outputs/flow.json.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import OUT_DIR, cohorts, ensure_dirs


def main():
    ensure_dirs()
    c = cohorts()
    P, teams, meta = c["P"], c["teams"], c["meta"]

    registered = {k for k, v in P.items() if v["registered"] == "y"}
    reg_teams = [t for t in teams if t["registered"] == "y"]
    sub_teams = [t for t in teams if t["submitted"] == "y"]

    # Team membership comes from two forms, each authoritative for one thing.
    # The team registration form names 220 members across the 48 teams that
    # filed it. One further team, Artificially Intelligent, submitted a project
    # without registering, so the 49 teams the paper reports are 48 + 1 and the
    # 220 covers only 48 of them. The submission form names every member of
    # every submitting team, which is where 149 comes from.
    team_members = sum(t["member_name_cells"] for t in teams)
    distinct_members = sum(t["distinct_members"] for t in teams)
    submitting_members = sum(t["submission_members"] for t in teams)

    declined_post = c["post"] - c["post_consent"]
    declined_reg = {e for e in c["post_consent"]
                    if P[e]["registered"] == "y" and P[e]["consented"] != "y"}
    no_pre_record = {e for e in c["post_consent"] if P[e]["registered"] != "y"}

    flow = {
        "pre_form_rows": meta["pre_event_form_rows"],
        "registrants": len(registered),
        "consented": len(c["consented"]),
        "declined_at_registration": len(registered) - len(c["consented"]),
        "registered_teams": len(reg_teams),
        "unregistered_submitting_teams": meta["unregistered_submitting_teams"],
        "teams": len(teams),
        "team_members": team_members,
        "team_members_distinct_people": distinct_members,
        "members_named_at_registration": sum(
            1 for v in P.values() if v["team_label"]),
        # Team membership in PEOPLE, not in form cells. 220 counts the member
        # names a captain typed; 200 of those people had registered and 20
        # never did. 208 registrants were on a team in all -- the 200 named,
        # plus members of the one team that filed no roster. 292 - 208 = 84 is
        # therefore the number of registrants who did not join a team; the
        # 292 - 220 = 72 an earlier version showed subtracted a form count
        # from a person count and was not a count of anybody.
        "registrants_on_a_team": sum(
            1 for v in P.values() if v["on_a_team"] == "y"),
        "named_members_registered": meta["named_members_registered"],
        # Of the 149 named on the submission forms, 145 had registered and
        # 140 of those consented. The eligible denominator is NOT 144 of these
        # 149: it is those 140 plus 4 consenting registrants who completed the
        # post-event survey but appear on no roster. Saying "149 named members,
        # of whom 144 consented" is therefore false, and was wrong on an
        # earlier draft of Figure 1.
        "submitting_members_consented": meta["submitting_members_consented"],
        "eligible_not_on_any_roster": meta["eligible_not_on_any_roster"],
        "submitting_members_registered": (
            submitting_members - meta["submitting_members_unregistered"]),
        "named_members_unregistered": (
            team_members - meta["named_members_registered"]),
        "submitting_teams": len(sub_teams),
        "submitting_team_members": submitting_members,
        "post_form_rows": meta["post_event_form_rows"],
        "post_respondents": len(c["post"]),
        "post_declined_consent": len(declined_post),
        "post_consented": len(c["post_consent"]),
        "post_consented_declined_at_registration": len(declined_reg),
        "post_consented_no_pre_record": len(no_pre_record),
        "paired": len(c["paired"]),
        "consenting_on_submitting_teams": len(c["on_submitting"]),
    }

    flow["rates"] = {
        "consent_among_registrants": [
            flow["consented"], flow["registrants"],
            round(100 * flow["consented"] / flow["registrants"], 1)],
        "reached_submission": [
            submitting_members, team_members,
            round(100 * submitting_members / team_members, 1)],
        "post_completion_among_eligible": [
            flow["post_respondents"], submitting_members,
            round(100 * flow["post_respondents"] / submitting_members, 1)],
        "paired_among_post_completers": [
            flow["paired"], flow["post_respondents"],
            round(100 * flow["paired"] / flow["post_respondents"], 1)],
        "teams_submitting": [
            len(sub_teams), len(teams),
            round(100 * len(sub_teams) / len(teams), 1)],
    }

    w = 46
    print("=" * 72)
    print("PARTICIPANT FLOW")
    print("=" * 72)
    for k in ("pre_form_rows", "registrants", "consented",
              "declined_at_registration", "registered_teams",
              "unregistered_submitting_teams", "teams", "team_members",
              "team_members_distinct_people", "members_named_at_registration",
              "registrants_on_a_team", "named_members_registered",
              "named_members_unregistered", "submitting_members_registered",
              "submitting_members_consented", "eligible_not_on_any_roster",
              "submitting_teams", "submitting_team_members", "post_form_rows",
              "post_respondents", "post_declined_consent", "post_consented",
              "post_consented_declined_at_registration",
              "post_consented_no_pre_record", "paired",
              "consenting_on_submitting_teams"):
        print("  %-*s %s" % (w, k.replace("_", " "), flow[k]))

    print("\n  Figure 1 exclusions")
    print("  %-*s %d" % (w, "post respondents", flow["post_respondents"]))
    print("  %-*s -%d" % (w, "declined consent on the post-event survey",
                          flow["post_declined_consent"]))
    print("  %-*s -%d" % (w, "consented at post, declined at registration",
                          flow["post_consented_declined_at_registration"]))
    print("  %-*s -%d" % (w, "no matching pre-event registration record",
                          flow["post_consented_no_pre_record"]))
    print("  %-*s =%d" % (w, "analysed", flow["paired"]))

    print("\n  CHERRIES completion rate, reported in stages")
    for k, (a, b, p) in flow["rates"].items():
        print("  %-*s %d/%d = %s%%" % (w, k.replace("_", " "), a, b, p))

    print("\n  per-team member counts")
    print("  %-10s%12s%12s%12s%12s" % ("team", "registered", "members",
                                       "submitted", "on submission"))
    for t in teams:
        print("  %-10s%12s%12d%12s%12d"
              % (t["team_label"], t["registered"], t["member_name_cells"],
                 t["submitted"], t["submission_members"]))

    with open(os.path.join(OUT_DIR, "flow.json"), "w") as fh:
        json.dump(flow, fh, indent=2)
    print("\n  wrote %s" % os.path.normpath(os.path.join(OUT_DIR, "flow.json")))
    return flow


if __name__ == "__main__":
    main()
