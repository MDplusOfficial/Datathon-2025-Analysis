#!/usr/bin/env python3
"""
s08_figure1_flow.py
===================
Generates Figure 1, the CONSORT-style participant flow diagram.

The left spine is the enrolment and team pathway; the right-hand boxes are the
exclusions at each step. The post-survey was distributed only to members of
teams that submitted a project, so post-survey completion is reported against
that eligible denominator rather than against all consented registrants.

No count is typed in here: they all come from outputs/flow.json, which
s01_participant_flow.py writes from the source data. Run that first.

Output: ../figures/Figure1_flow.{png,pdf} at exactly 1200 x 1200 px

Usage:
    python s01_participant_flow.py && python s08_figure1_flow.py
"""
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

HERE = os.path.dirname(os.path.abspath(__file__))
OUTDIR = os.path.join(HERE, "..", "figures")
FLOW = json.load(open(os.path.join(HERE, "..", "outputs", "flow.json")))

# --------------------------------------------------------------- counts ----
# All counts come from s01_participant_flow.py via outputs/flow.json.
#
# The spine is the EVENT pathway, so every box is a count of all participants
# at that stage. Consent is shown as its own annotated node off the first box
# rather than as a spine step, because it does not remove anyone from the
# event pathway -- it defines which participants' survey responses could be
# analysed. All survey analyses are restricted to the consented cohort.
REGISTERED      = FLOW["registrants"]
CONSENTED       = FLOW["consented"]        # most recent consent per registrant
DECLINED        = REGISTERED - CONSENTED
# 220 named members across the 48 teams that filed a team registration. The
# 49th team, Artificially Intelligent, submitted a project without registering,
# so its members are not in this count.
FORMED_TEAMS    = FLOW["team_members"]
# 220 counts member NAMES a captain typed. 200 of those people had registered
# and 20 never did; 208 registrants were on a team in all (the 200 named, plus
# members of the one team that filed no roster). The team-formation exclusion
# is therefore 292 - 208 = 84 registrants. Subtracting 220 from 292 compares a
# form count with a person count and yields nothing real.
ON_A_TEAM       = FLOW["registrants_on_a_team"]
NAMED_REG       = FLOW["named_members_registered"]
NAMED_UNREG     = FLOW["named_members_unregistered"]
ELIGIBLE_CONS   = FLOW["consenting_on_submitting_teams"]
N_TEAMS         = FLOW["teams"]
SUBMITTED       = FLOW["submitting_team_members"]
N_SUB_TEAMS     = FLOW["submitting_teams"]
POST_RESPONSES  = FLOW["post_respondents"]
DECL_POST       = FLOW["post_declined_consent"]
DECL_REG        = FLOW["post_consented_declined_at_registration"]
POST_CONSENTED  = FLOW["post_consented"] - DECL_REG   # consented at BOTH times
PAIRED          = FLOW["paired"]
UNLINKED        = POST_CONSENTED - PAIRED

MAIN = [
    ("Registered for the datathon\nand completed the pre-event survey",
     [f"n = {REGISTERED}"], None, None),
    (f"Formed a team\n({N_TEAMS} teams)",
     [f"n = {FORMED_TEAMS} named members"],
     f"of whom {NAMED_REG} had registered and {NAMED_UNREG} had not",
     f"Registrants who did not\njoin a team\nn = {REGISTERED - ON_A_TEAM}"),
    (f"On a team that submitted a project ({N_SUB_TEAMS} teams),\nand so eligible for the post-event survey",
     [f"n = {SUBMITTED} named members"],
     f"of whom {ELIGIBLE_CONS} consented at registration",
     f"Team did not submit a project\nn = {FORMED_TEAMS - SUBMITTED}"),
    ("Completed the post-event survey",
     [f"n = {POST_RESPONSES}"], None,
     f"Did not complete the\npost-event survey\nn = {SUBMITTED - POST_RESPONSES}"),
    ("Consented to research use of both\npre- and post-event responses",
     [f"n = {POST_CONSENTED}"], None,
     f"Declined research consent\nn = {DECL_POST + DECL_REG}\n"
     f"({DECL_POST} at the post-event survey,\n{DECL_REG} at registration)"),
    ("Analysed: paired pre- and\npost-event responses",
     [f"n = {PAIRED}"], None,
     f"Did not match a pre-event\nrecord by email address\nn = {UNLINKED}"),
]

FOOTNOTE = (
    f"The post-event survey was distributed only to members of the {N_SUB_TEAMS} "
    f"teams that submitted a project, so n = {SUBMITTED} is the eligible "
    f"denominator for post-event completion ({POST_RESPONSES}/{SUBMITTED} = "
    f"{100*POST_RESPONSES/SUBMITTED:.0f}%). Post-event survey completion "
    f"({POST_RESPONSES}), consent eligibility ({POST_CONSENTED}), successful "
    f"pre/post linkage ({PAIRED}) and inclusion in the paired analysis "
    f"({PAIRED}) are reported separately; all {POST_CONSENTED - UNLINKED} "
    f"consented respondents who linked to a pre-event registration record had "
    f"usable item responses at both timepoints, so linkage and inclusion "
    f"coincided. Consent to research use of de-identified responses was "
    f"collected at registration and again on the post-event survey; "
    f"{CONSENTED} of {REGISTERED} registrants "
    f"({100*CONSENTED/REGISTERED:.0f}%) consented at registration, and all "
    f"survey analyses are restricted to participants who consented at both "
    f"timepoints. Team membership is taken from the team registration form, "
    f"which named {FORMED_TEAMS} members across "
    f"{FLOW['registered_teams']} teams; one further team submitted a project "
    f"without registering, giving {N_TEAMS} teams in total. The {FORMED_TEAMS} "
    f"and {SUBMITTED} boxes count members NAMED on the team-registration and "
    f"project-submission forms; of those, {NAMED_REG} and "
    f"{FLOW['submitting_members_registered']} respectively had completed "
    f"registration, and {ON_A_TEAM} registrants were on a team in all. The "
    f"team-formation exclusion is given in registrants for that reason."
)

BOX_W, BOX_H   = 0.50, 0.104
SIDE_W, SIDE_H = 0.33, 0.080
X_MAIN, X_SIDE = 0.29, 0.785
FACE, EDGE = "#eef3f8", "#33475b"
SIDE_FACE, SIDE_EDGE = "#f7f7f5", "#8a8a86"


def box(ax, x, y, w, h, title, lines, face, edge, tsize, vsize, note=None):
    ax.add_patch(FancyBboxPatch(
        (x - w / 2, y - h / 2), w, h,
        boxstyle="round,pad=0.006,rounding_size=0.012",
        facecolor=face, edgecolor=edge, linewidth=1.3, zorder=2))
    if lines:
        ax.text(x, y + (h * 0.22 if note else h * 0.16), title,
                ha="center", va="center",
                fontsize=tsize, color="#16222e", zorder=3)
        ax.text(x, y - (h * 0.09 if note else h * 0.28), "  ".join(lines),
                ha="center", va="center",
                fontsize=vsize, fontweight="bold", color="#16222e", zorder=3)
        if note:
            ax.text(x, y - h * 0.33, note, ha="center", va="center",
                    fontsize=tsize - 2.0, color="#55646f", zorder=3)
    else:
        ax.text(x, y, title, ha="center", va="center", fontsize=tsize,
                color="#2f2f2c", zorder=3)


def main():
    n = len(MAIN)
    # 8 in square at 150 dpi -> exactly 1200 x 1200 px
    fig, ax = plt.subplots(figsize=(8, 8))
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    top, bottom = 0.866, 0.078
    ys = [top - i * (top - bottom) / (n - 1) for i in range(n)]
    hs = [BOX_H] * n

    for i, ((title, lines, note, side), y) in enumerate(zip(MAIN, ys)):
        box(ax, X_MAIN, y, BOX_W, hs[i], title, lines, FACE, EDGE, 10.0, 11.0,
            note=note)

        if i < n - 1:
            ax.add_patch(FancyArrowPatch(
                (X_MAIN, y - hs[i] / 2), (X_MAIN, ys[i + 1] + hs[i + 1] / 2),
                arrowstyle="-|>", mutation_scale=15,
                linewidth=1.3, color=EDGE, zorder=1))

        # Exclusion box branches off the arrow *into* this step.
        if side:
            y_branch = (ys[i - 1] - hs[i - 1] / 2 + y + hs[i] / 2) / 2
            box(ax, X_SIDE, y_branch, SIDE_W, SIDE_H, side, None,
                SIDE_FACE, SIDE_EDGE, 8.4, 8.4)
            ax.add_patch(FancyArrowPatch(
                (X_MAIN, y_branch), (X_SIDE - SIDE_W / 2, y_branch),
                arrowstyle="-|>", mutation_scale=13,
                linewidth=1.1, color=SIDE_EDGE, zorder=1))

    ax.text(0.5, 0.985,
            "Participant flow through registration, team formation,\n"
            "project submission, and survey completion",
            ha="center", va="top", fontsize=11.5, fontweight="bold",
            color="#16222e")
    os.makedirs(OUTDIR, exist_ok=True)
    for ext in ("png", "pdf"):
        dest = os.path.join(OUTDIR, f"Figure1_flow.{ext}")
        fig.savefig(dest, dpi=150, facecolor="white")
        print("wrote", os.path.normpath(dest))
    print("\n--- caption text (paste below the figure, not onto it) ---\n")
    print(FOOTNOTE.replace("\n", " "))


if __name__ == "__main__":
    main()
