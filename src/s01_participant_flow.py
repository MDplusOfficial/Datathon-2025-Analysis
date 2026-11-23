#!/usr/bin/env python3
"""
Participant flow (Figure 1) and the staged survey counts reported in the
Results, Ethical Considerations and the CHERRIES checklist.

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
        "registrants_on_a_team": sum(
            1 for v in P.values() if v["on_a_team"] == "y"),
        "named_members_registered": meta["named_members_registered"],
        "teamform_members_submitting": meta["teamform_members_submitting"],
        "teamform_members_not_submitting": meta["teamform_members_not_submitting"],
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

    both = flow["post_consented"] - flow["post_consented_declined_at_registration"]
    flow["rates"] = {
        "consented_at_registration": [flow["consented"], flow["registrants"]],
        "teams_submitting": [len(sub_teams), len(teams)],
        "completed_post_survey": [flow["post_respondents"], submitting_members],
        "consented_both": [both, flow["post_respondents"]],
        "matched_to_pre_survey": [flow["paired"], both],
    }
    for k, (num, den) in flow["rates"].items():
        flow["rates"][k].append(round(100 * num / den, 1))

    f = flow
    rows = [
        ("Registered and completed the pre-event survey", f["registrants"], ""),
        ("  declined research consent at registration",
         f["declined_at_registration"], ""),
        ("Consented at registration", f["consented"], ""),
        ("Formed a team (%d teams), named members" % f["teams"],
         f["team_members"], ""),
        ("  of whom registered", f["named_members_registered"], ""),
        ("  named without registering", f["named_members_unregistered"], ""),
        ("  registrants who did not join a team",
         f["registrants"] - f["registrants_on_a_team"],
         "%d - %d registrants on a team" % (f["registrants"],
                                            f["registrants_on_a_team"])),
        ("On a team that submitted (%d teams), named members"
         % f["submitting_teams"], f["submitting_team_members"], ""),
        ("  of whom consented at registration",
         f["submitting_members_consented"], ""),
        ("  named members on teams that did not submit",
         f["teamform_members_not_submitting"], "team registration form"),
        ("Completed the post-event survey", f["post_respondents"], ""),
        ("  did not complete",
         f["submitting_team_members"] - f["post_respondents"], ""),
        ("Consented to use of pre- and post-event data", both, ""),
        ("  excluded for consent",
         f["post_declined_consent"] + f["post_consented_declined_at_registration"],
         "%d at the post-event survey, %d at registration"
         % (f["post_declined_consent"],
            f["post_consented_declined_at_registration"])),
        ("Paired analysis", f["paired"], ""),
        ("  not matched to a pre-event survey by email address",
         f["post_consented_no_pre_record"], ""),
    ]
    print("=" * 78)
    print("PARTICIPANT FLOW (Figure 1)")
    print("=" * 78)
    for label, n, note in rows:
        print("  %-54s%5d   %s" % (label, n, note))
    print("\n  consenting registrants eligible for the post-event survey: %d"
          % f["consenting_on_submitting_teams"])
    print("    = %d named members of submitting teams who consented"
          % f["submitting_members_consented"])
    print("    + %d who completed the post-event survey but are on no team roster"
          % f["eligible_not_on_any_roster"])

    print("\n  staged rates (CHERRIES)")
    for k, (num, den, pct) in f["rates"].items():
        print("  %-54s%d/%d (%s%%)" % (k.replace("_", " "), num, den, pct))

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
