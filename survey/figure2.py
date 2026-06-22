#!/usr/bin/env python3
"""
figure2.py
==========
Generates Figure 2 (n=69) from the raw survey exports.

  A-C  Within-participant pre->post slopegraphs for the three constructs
       (Medical AI Readiness, AI Technology Acceptance/TAM, Digital Health Literacy)
  D    Composite pre vs post bar comparison (Wilcoxon, BH-corrected significance)
  E    Item-level mean-change ranking, colored by construct
       (blue/orange/purple -- deliberately NOT the green pre/post scheme used in D)

Output: ../figures/Figure2_revised.png

Usage:
    python figure2.py
    DATATHON_DATA=/path/to/data python figure2.py
"""
import os, math, statistics
from datetime import datetime
import openpyxl
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.patches import Patch
from scipy.stats import wilcoxon
from statsmodels.stats.multitest import multipletests

DATA_DIR = os.environ.get(
    "DATATHON_DATA",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data"),
)
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "figures", "Figure2_revised.png")

GROUPS = {"Medical AI Readiness": [0, 1, 2, 3, 4, 5],
          "AI Technology Acceptance (TAM)": [6, 7, 8, 9],
          "Digital Health Literacy": [10, 11, 12]}
ITEM_META = [("Identify AI-appropriate problems", 1, "R"), ("Explain core AI concepts", 0, "R"),
             ("Interpret AI outputs", 2, "R"), ("Ethical responsibilities", 3, "R"),
             ("Collaborate with non-clinical", 4, "R"), ("Vision for AI empowerment", 5, "R"),
             ("AI tools useful for patients", 6, "T"), ("AI improves care effectiveness", 7, "T"),
             ("Intend to recommend AI", 8, "T"), ("Confident addressing AI questions", 9, "T"),
             ("Find digital health resources", 10, "D"), ("Judge digital health quality", 11, "D"),
             ("Use digital tools for self-mgmt", 12, "D")]

DARK, MID, LIGHT = "#1b7837", "#5aae61", "#a6dba0"          # greens: pre/post + slopegraphs
ITEM_COLORS = {"R": "#0072B2", "T": "#E69F00", "D": "#7570B3"}  # categorical: construct in panel E


def parse_ts(v):
    if isinstance(v, datetime):
        return v
    for f in ("%Y-%m-%d %H:%M:%S", "%m/%d/%Y %H:%M:%S"):
        try:
            return datetime.strptime(str(v), f)
        except ValueError:
            pass
    return datetime.min


def load(fname, email_col, consent_col, first_item_col):
    wb = openpyxl.load_workbook(os.path.join(DATA_DIR, fname), data_only=True)
    ws = wb.active
    recs = []
    for r in ws.iter_rows(min_row=2, values_only=True):
        if not r[email_col]:
            continue
        vals = []
        for c in range(first_item_col, first_item_col + 13):
            try:
                vals.append(float(r[c]))
            except (TypeError, ValueError):
                vals.append(None)
        recs.append((str(r[email_col]).strip().lower(), parse_ts(r[0]),
                     str(r[consent_col]).strip().lower() if r[consent_col] else "", vals))
    return recs


def build_pairs():
    pre, post = {}, {}
    for e, ts, con, v in sorted(load("presurvey.xlsx", 1, 5, 6), key=lambda x: x[1]):
        pre.setdefault(e, (con, v))
    for e, ts, con, v in sorted(load("postsurvey.xlsx", 1, 2, 3), key=lambda x: x[1]):
        post[e] = (con, v)
    pre = {e: v for e, v in pre.items() if v[0] == "yes"}
    post = {e: v for e, v in post.items() if v[0] in ("yes", "y", "true", "1")}
    pairs = []
    for e in pre:
        if e in post:
            pv, qv = pre[e][1], post[e][1]
            if any(x is not None for x in pv) and any(x is not None for x in qv):
                pairs.append((pv, qv))
    return pairs


def comp(v, idx):
    xs = [v[i] for i in idx if v[i] is not None]
    return sum(xs) / len(xs) if xs else None


def ci95(xs):
    m = statistics.mean(xs)
    return m, 1.96 * statistics.stdev(xs) / math.sqrt(len(xs))


def star(p):
    return "***" if p < 0.001 else "**" if p < 0.01 else "*" if p < 0.05 else "ns"


def main():
    pairs = build_pairs()
    pp = {}
    for name, idx in GROUPS.items():
        rows = [(comp(p, idx), comp(q, idx)) for p, q in pairs]
        pp[name] = [(a, b) for a, b in rows if a is not None and b is not None]

    fig = plt.figure(figsize=(12, 14))
    gs = gridspec.GridSpec(3, 3, height_ratios=[1.0, 1.0, 1.15], hspace=0.55, wspace=0.42)
    short = {"Medical AI Readiness": "Medical AI Readiness",
             "AI Technology Acceptance (TAM)": "AI Technology Acceptance\n(TAM, patient-facing)",
             "Digital Health Literacy": "Digital Health Literacy"}
    colm = {"Medical AI Readiness": DARK, "AI Technology Acceptance (TAM)": MID,
            "Digital Health Literacy": LIGHT}

    for k, (name, idx) in enumerate(GROUPS.items()):
        ax = fig.add_subplot(gs[0, k])
        rows = pp[name]
        for a, b in rows:
            ax.plot([0, 1], [a, b], color=colm[name], alpha=0.12, lw=0.8)
        mp = statistics.mean([a for a, b in rows]); mq = statistics.mean([b for a, b in rows])
        ax.plot([0, 1], [mp, mq], color="black", lw=2.6, marker="o", ms=6, zorder=5)
        ax.set_xlim(-0.25, 1.25); ax.set_ylim(1, 5.0)
        ax.set_xticks([0, 1]); ax.set_xticklabels(["Pre", "Post"], fontsize=11)
        ax.set_title(short[name], fontsize=11, weight="bold", pad=10)
        if k == 0:
            ax.set_ylabel("Composite score (1-5)", fontsize=11)
        ax.text(0.5, 4.78, f"Mean Δ = +{mq - mp:.2f}", ha="center", fontsize=10, style="italic")
        ax.text(-0.30, 1.04, "ABC"[k], transform=ax.transAxes, fontsize=15, weight="bold", va="top")
        ax.spines[["top", "right"]].set_visible(False)

    # Panel D: composite bars
    gs_d = gridspec.GridSpecFromSubplotSpec(1, 3, subplot_spec=gs[1, :], width_ratios=[0.6, 3, 0.6])
    axd = fig.add_subplot(gs_d[0, 1])
    names = list(GROUPS); x = range(len(names)); w = 0.38
    pre_m = [ci95([a for a, b in pp[n]]) for n in names]
    post_m = [ci95([b for a, b in pp[n]]) for n in names]
    pv = [wilcoxon([b for a, b in pp[n]], [a for a, b in pp[n]]).pvalue for n in names]
    padj = multipletests(pv, method="fdr_bh")[1]
    axd.bar([i - w / 2 for i in x], [m for m, e in pre_m], w, yerr=[e for m, e in pre_m],
            color=LIGHT, capsize=3, label="Pre", edgecolor="white")
    axd.bar([i + w / 2 for i in x], [m for m, e in post_m], w, yerr=[e for m, e in post_m],
            color=DARK, capsize=3, label="Post", edgecolor="white")
    for i in x:
        top = max(pre_m[i][0] + pre_m[i][1], post_m[i][0] + post_m[i][1])
        axd.text(i, top + 0.12, star(padj[i]), ha="center", fontsize=11)
    axd.set_xticks(list(x))
    axd.set_xticklabels(["AI Readiness", "TAM\n(patient-facing)", "Digital Health\nLiteracy"], fontsize=9.5)
    axd.set_ylim(2.5, 5); axd.set_ylabel("Mean composite score", fontsize=10)
    axd.set_title("Composite Score Comparison", fontsize=11.5, weight="bold")
    axd.legend(frameon=False, fontsize=9, loc="upper left")
    axd.text(-0.18, 1.02, "D", transform=axd.transAxes, fontsize=15, weight="bold", va="top")
    axd.spines[["top", "right"]].set_visible(False)

    # Panel E: item ranking, colored by construct (non-green)
    axe = fig.add_subplot(gs[2, :])
    rows, ipv = [], []
    for lab, i, c in ITEM_META:
        d = [(q[i] - p[i]) for p, q in pairs if p[i] is not None and q[i] is not None]
        pre_v = [p[i] for p, q in pairs if p[i] is not None and q[i] is not None]
        post_v = [q[i] for p, q in pairs if p[i] is not None and q[i] is not None]
        rows.append([lab, statistics.mean(d), c]); ipv.append(wilcoxon(post_v, pre_v).pvalue)
    ipadj = multipletests(ipv, method="fdr_bh")[1]
    for r, pa in zip(rows, ipadj):
        r.append(pa)
    rows.sort(key=lambda r: r[1])
    yy = range(len(rows))
    axe.barh(list(yy), [r[1] for r in rows], color=[ITEM_COLORS[r[2]] for r in rows], edgecolor="white")
    for yi, r in zip(yy, rows):
        axe.text(r[1] + 0.01, yi, star(r[3]), va="center", fontsize=8.5)
    axe.set_yticks(list(yy)); axe.set_yticklabels([r[0] for r in rows], fontsize=9)
    axe.set_xlabel("Mean Change (Post - Pre)", fontsize=10)
    axe.set_xlim(0, max(r[1] for r in rows) * 1.16)
    axe.set_title("Item-Level Improvement Ranking", fontsize=11.5, weight="bold")
    axe.text(-0.02, 1.02, "E", transform=axe.transAxes, fontsize=15, weight="bold", va="top")
    axe.spines[["top", "right"]].set_visible(False)
    handles = [Patch(facecolor=ITEM_COLORS[k], label=l)
               for k, l in [("R", "Readiness"), ("T", "TAM"), ("D", "Digital literacy")]]
    axe.legend(handles=handles, loc="lower right", frameon=False, fontsize=8.5)

    fig.suptitle("Figure 2. Impact of Datathon on AI Readiness, Technology Acceptance,\n"
                 "and Digital Health Literacy (n=69)", fontsize=13, weight="bold", y=0.995)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    plt.savefig(OUT, dpi=300, bbox_inches="tight", facecolor="white", pad_inches=0.3)
    print("wrote", os.path.abspath(OUT))


if __name__ == "__main__":
    main()
