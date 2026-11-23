#!/usr/bin/env python3
"""
Figure 3: pre-post survey results for the 69 paired respondents.

  A-C  individual pre-post change for each composite
  D    composite means with 95% CIs
  E    item-level mean change
"""
import math
import os
import statistics
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from scipy.stats import wilcoxon
from statsmodels.stats.multitest import multipletests

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import FIG_DIR, cohorts, composite, ensure_dirs

GROUPS = {"Medical AI Readiness": [0, 1, 2, 3, 4, 5],
          "AI Technology Acceptance": [6, 7, 8, 9],
          "Digital Health Literacy": [10, 11, 12]}
ITEM_META = [
    ("Identify AI-appropriate problems", 1, "R"),
    ("Explain core AI concepts", 0, "R"),
    ("Interpret AI outputs", 2, "R"),
    ("Ethical responsibilities", 3, "R"),
    ("Collaborate with non-clinical", 4, "R"),
    ("Vision for AI empowerment", 5, "R"),
    ("AI tools useful for patients", 6, "T"),
    ("AI improves care effectiveness", 7, "T"),
    ("Intend to recommend AI", 8, "T"),
    ("Confident addressing AI questions", 9, "T"),
    ("Find digital health resources", 10, "D"),
    ("Judge digital health quality", 11, "D"),
    ("Use digital tools for self-mgmt", 12, "D"),
]
DARK, MID, LIGHT = "#1b7837", "#5aae61", "#a6dba0"
ITEM_COLORS = {"R": "#0072B2", "T": "#E69F00", "D": "#7570B3"}


def ci95(xs):
    return statistics.mean(xs), 1.96 * statistics.stdev(xs) / math.sqrt(len(xs))


def star(p):
    return "***" if p < 0.001 else "**" if p < 0.01 else "*" if p < 0.05 else "ns"


def main():
    ensure_dirs()
    c = cohorts()
    P = c["P"]
    pairs = [(P[e]["pre"], P[e]["post"]) for e in sorted(c["paired"])]

    pp = {}
    for name, idx in GROUPS.items():
        rows = [(composite(p, idx), composite(q, idx)) for p, q in pairs]
        pp[name] = [(a, b) for a, b in rows if a is not None and b is not None]

    fig = plt.figure(figsize=(12, 14))
    gs = gridspec.GridSpec(3, 3, height_ratios=[1.0, 1.0, 1.15],
                           hspace=0.55, wspace=0.42)
    short = {"Medical AI Readiness": "Medical AI Readiness",
             "AI Technology Acceptance": "AI Technology Acceptance\n(patient-facing)",
             "Digital Health Literacy": "Digital Health Literacy"}
    colm = {"Medical AI Readiness": DARK, "AI Technology Acceptance": MID,
            "Digital Health Literacy": LIGHT}

    for k, (name, idx) in enumerate(GROUPS.items()):
        ax = fig.add_subplot(gs[0, k])
        rows = pp[name]
        for a, b in rows:
            ax.plot([0, 1], [a, b], color=colm[name], alpha=0.12, lw=0.8)
        mp = statistics.mean([a for a, _ in rows])
        mq = statistics.mean([b for _, b in rows])
        ax.plot([0, 1], [mp, mq], color="black", lw=2.6, marker="o", ms=6, zorder=5)
        ax.set_xlim(-0.25, 1.25)
        ax.set_ylim(1, 5.0)
        ax.set_xticks([0, 1])
        ax.set_xticklabels(["Pre", "Post"], fontsize=11)
        ax.set_title(short[name], fontsize=11, weight="bold", pad=10)
        if k == 0:
            ax.set_ylabel("Composite score (1-5)", fontsize=11)
        ax.text(0.5, 4.78, "Mean Δ = +%.2f" % (mq - mp), ha="center",
                fontsize=10, style="italic")
        ax.text(-0.30, 1.04, "ABC"[k], transform=ax.transAxes, fontsize=15,
                weight="bold", va="top")
        ax.spines[["top", "right"]].set_visible(False)

    gs_d = gridspec.GridSpecFromSubplotSpec(1, 3, subplot_spec=gs[1, :],
                                            width_ratios=[0.6, 3, 0.6])
    axd = fig.add_subplot(gs_d[0, 1])
    names = list(GROUPS)
    x = range(len(names))
    w = 0.38
    pre_m = [ci95([a for a, _ in pp[n]]) for n in names]
    post_m = [ci95([b for _, b in pp[n]]) for n in names]
    pv = [wilcoxon([b for _, b in pp[n]], [a for a, _ in pp[n]]).pvalue
          for n in names]
    padj = multipletests(pv, method="fdr_bh")[1]
    axd.bar([i - w / 2 for i in x], [m for m, _ in pre_m], w,
            yerr=[e for _, e in pre_m], color=LIGHT, capsize=3, label="Pre",
            edgecolor="white")
    axd.bar([i + w / 2 for i in x], [m for m, _ in post_m], w,
            yerr=[e for _, e in post_m], color=DARK, capsize=3, label="Post",
            edgecolor="white")
    for i in x:
        top = max(pre_m[i][0] + pre_m[i][1], post_m[i][0] + post_m[i][1])
        axd.text(i, top + 0.12, star(padj[i]), ha="center", fontsize=11)
    axd.set_xticks(list(x))
    axd.set_xticklabels(["Medical AI\nReadiness",
                         "AI Technology\nAcceptance\n(patient-facing)",
                         "Digital Health\nLiteracy"], fontsize=9.5)
    axd.set_ylim(2.5, 5)
    axd.set_ylabel("Mean composite score", fontsize=10)
    axd.set_title("Composite Score Comparison", fontsize=11.5, weight="bold")
    axd.legend(frameon=False, fontsize=9, loc="upper left")
    axd.text(-0.18, 1.02, "D", transform=axd.transAxes, fontsize=15,
             weight="bold", va="top")
    axd.spines[["top", "right"]].set_visible(False)

    axe = fig.add_subplot(gs[2, :])
    rows, ipv = [], []
    for lab, i, con in ITEM_META:
        both = [(p[i], q[i]) for p, q in pairs
                if p[i] is not None and q[i] is not None]
        rows.append([lab, statistics.mean([b - a for a, b in both]), con])
        ipv.append(wilcoxon([b for _, b in both], [a for a, _ in both]).pvalue)
    for r, pa in zip(rows, multipletests(ipv, method="fdr_bh")[1]):
        r.append(pa)
    rows.sort(key=lambda r: r[1])
    yy = range(len(rows))
    axe.barh(list(yy), [r[1] for r in rows],
             color=[ITEM_COLORS[r[2]] for r in rows], edgecolor="white")
    for yi, r in zip(yy, rows):
        axe.text(r[1] + 0.01, yi, star(r[3]), va="center", fontsize=8.5)
    axe.set_yticks(list(yy))
    axe.set_yticklabels([r[0] for r in rows], fontsize=9)
    axe.set_xlabel("Mean Change (Post - Pre)", fontsize=10)
    axe.set_xlim(0, max(r[1] for r in rows) * 1.16)
    axe.set_title("Item-Level Improvement Ranking", fontsize=11.5, weight="bold")
    axe.text(-0.02, 1.02, "E", transform=axe.transAxes, fontsize=15,
             weight="bold", va="top")
    axe.spines[["top", "right"]].set_visible(False)
    axe.legend(handles=[Patch(facecolor=ITEM_COLORS[k], label=l)
                        for k, l in [("R", "Readiness"),
                                     ("T", "Technology acceptance"),
                                     ("D", "Digital literacy")]],
               loc="lower right", frameon=False, fontsize=8.5)

    for ext in ("png", "pdf"):
        dest = os.path.join(FIG_DIR, "Figure3_survey." + ext)
        plt.savefig(dest, dpi=300, bbox_inches="tight", facecolor="white",
                    pad_inches=0.3)
        print("  wrote %s" % os.path.normpath(dest))


if __name__ == "__main__":
    main()
