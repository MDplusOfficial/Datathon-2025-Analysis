#!/usr/bin/env python3
"""
Figure 2: participant and team characteristics.

  A  degree program
  B  year in program
  C  institutions
  D  primary motivation
  E  team composition (institutional and training diversity)
"""
import os
import sys
from collections import Counter

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import FIG_DIR, cohorts, ensure_dirs

FIG2C_INSTITUTIONS = [
    "Icahn School of Medicine at Mount Sinai", "UT Southwestern",
    "Brown University (Warren Alpert)", "Loyola Stritch School of Medicine",
    "University of Illinois", "University of Miami", "UNC Chapel Hill",
    "UCSF", "Emory University", "Tufts University",
    "Western University of Health Sciences", "Usmanu Danfodiyo University",
]


def main():
    ensure_dirs()
    c = cohorts()
    reg = {k: c["P"][k] for k in c["consented"]}
    n = len(reg)

    degree = Counter(r["degree_category"] for r in reg.values())
    year = Counter(r["year_in_program"] for r in reg.values())
    inst = Counter(r["institution_display"] for r in reg.values())
    motiv = Counter(r["motivation_category"] for r in reg.values())
    for k in [k for k, v in motiv.items() if v < 5 and k != "Other"]:
        motiv["Other"] += motiv.pop(k)
    assert sum(motiv.values()) == n, sum(motiv.values())
    assert sum(degree.values()) == n

    teams = {}
    for e, r in reg.items():
        if r["registration_team_group"]:
            teams.setdefault(r["registration_team_group"], []).append(e)
    team_stats = pd.DataFrame([{
        "Unique Institutions": len({reg[e]["institution_display"] for e in mem}),
        "Unique Degrees": len({reg[e]["degree_category"] for e in mem}),
    } for mem in teams.values()])

    sns.set_theme(style="whitegrid", font_scale=1.6)
    fig = plt.figure(figsize=(22, 20))
    gs = fig.add_gridspec(3, 2)

    ax1 = fig.add_subplot(gs[0, 0])
    d = pd.Series(dict(sorted(degree.items(), key=lambda kv: (-kv[1], kv[0]))))
    sns.barplot(x=d.values, y=d.index, hue=d.index, legend=False,
                palette="viridis", ax=ax1)
    ax1.set_title("Participant Backgrounds", fontweight="bold", fontsize=20)
    ax1.set_xlabel("Count", fontsize=18)
    ax1.set_ylabel("Degree Category", fontsize=18)

    ax2 = fig.add_subplot(gs[0, 1])
    y = pd.Series({k: v for k, v in sorted(year.items()) if k is not None})
    sns.barplot(x=y.index.astype(int), y=y.values, hue=y.index.astype(int),
                legend=False, palette="rocket", ax=ax2)
    ax2.set_title("Distribution by Year in Program", fontweight="bold",
                  fontsize=20)
    ax2.set_xlabel("Year", fontsize=18)
    ax2.set_ylabel("Count", fontsize=18)

    ax3 = fig.add_subplot(gs[1, 0])
    i = pd.Series(dict(inst)).reindex(FIG2C_INSTITUTIONS)
    sns.barplot(x=i.values, y=i.index, hue=i.index, legend=False,
                palette="mako", ax=ax3)
    ax3.set_title("Top Represented Institutions", fontweight="bold", fontsize=20)
    ax3.set_xlabel("Count", fontsize=18)
    ax3.set_ylabel("Institution Category", fontsize=18)

    ax4 = fig.add_subplot(gs[1, 1])
    m = pd.Series(dict(sorted(motiv.items(), key=lambda kv: (-kv[1], kv[0]))))
    colors = sns.color_palette("viridis", n_colors=len(m))
    wedges, _ = ax4.pie(m.values, colors=colors, startangle=140)
    ax4.legend(wedges, ["%s (%d)" % (k, v) for k, v in m.items()],
               title="Motivations", loc="center left",
               bbox_to_anchor=(1, 0, 0.5, 1))
    ax4.set_title("Primary Motivation for Joining", fontweight="bold",
                  fontsize=20)

    ax5 = fig.add_subplot(gs[2, :])
    matrix = pd.crosstab(team_stats["Unique Institutions"],
                         team_stats["Unique Degrees"])
    sns.heatmap(matrix, annot=True, fmt="d", cmap="mako_r", linewidths=.5,
                cbar_kws={"label": "Number of Teams"}, ax=ax5)
    ax5.collections[0].colorbar.set_label("Number of Teams", fontsize=18)
    ax5.set_title("Team Composition Matrix: Institutional vs. Training Diversity",
                  fontweight="bold", fontsize=20)
    ax5.set_ylabel("Number of Unique Institutions", fontsize=18)
    ax5.set_xlabel("Number of Unique Degree Types", fontsize=18)
    ax5.invert_yaxis()

    for ax, label in zip([ax1, ax2, ax3, ax4, ax5], list("ABCDE")):
        ax.text(-0.1, 1.1, label, transform=ax.transAxes, fontsize=20,
                fontweight="bold", va="top", ha="right")

    plt.tight_layout()
    for ext in ("png", "pdf"):
        dest = os.path.join(FIG_DIR, "Figure2_demographics." + ext)
        plt.savefig(dest, dpi=300, bbox_inches="tight", facecolor="white")
        print("  wrote %s" % os.path.normpath(dest))
    plt.close()


if __name__ == "__main__":
    main()
