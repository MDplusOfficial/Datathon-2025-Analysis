#!/usr/bin/env python3
"""
s06_freetext.py — Multimedia Appendix 5, Figures 4 and 5, Supplementary Figure
S1, and the free-text counts quoted in the Methods and Results.

Two halves:

  1. RECOMPUTED from the freetext_responses sheet — the number of usable
     responses, unique codes and code assignments. A code is retained for a
     response if either coder identified it (an inclusive union), so "unique
     codes" is the union across coders and "code assignments" counts each
     coder's contribution.

  2. CHECKED from the freetext_clusters / _cooccurrence / _silhouette sheets —
     the clustering step ran once, in Diversity_and_Thematic_Analysis.ipynb,
     over a feature space this script does not rebuild. Its outputs are carried
     in the dataset and checked here for internal consistency: sentiment must
     sum to each cluster's response count, no cluster may exceed the number of
     usable responses, the co-occurrence matrix must be symmetric with a zero
     diagonal, and no pair may co-occur more often than the smaller of the two
     clusters.

Writes outputs/freetext.json and, with --figures, regenerates Figures 4 and 5
and Supplementary Figure S1.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import FIG_DIR, OUT_DIR, ensure_dirs, load_dataset


def _codes(v):
    return [c.strip() for c in str(v or "").split(";") if c.strip()]


def recompute():
    recs = load_dataset()["freetext_responses"]
    usable = [r for r in recs if r["usable"] == "y"]
    per_response = [set(_codes(r["codes_kb"])) | set(_codes(r["codes_sm"]))
                    for r in usable]
    unique = set().union(*per_response) if per_response else set()
    assignments = sum(r["n_codes_kb"] + r["n_codes_sm"] for r in usable)
    deduped = sum(len(p) for p in per_response)
    with_text = sum(1 for r in recs if r["has_text"] == "y")
    return {
        "submission_rows_with_free_text": with_text,
        "usable_responses": len(usable),
        "unique_codes": len(unique),
        "code_assignments": assignments,
        "code_assignments_deduped_within_response": deduped,
    }


def check_clusters(n_usable):
    ds = load_dataset()
    clusters = ds["freetext_clusters"]
    cooc = ds["freetext_cooccurrence"]
    sil = ds["freetext_silhouette"]
    problems = []

    labels = [c["short_label"] for c in clusters]
    for c in clusters:
        n = c["responses"]
        s = (c["strongly_positive"] + c["moderately_positive"]
             + c["neutral_mixed"])
        if s != n:
            problems.append("%s: sentiment sums to %d, responses = %d"
                            % (c["short_label"], s, n))
        if n > n_usable:
            problems.append("%s: %d responses exceeds %d usable"
                            % (c["short_label"], n, n_usable))
    size = {c["short_label"]: c["responses"] for c in clusters}

    m = {}
    for row in cooc:
        a = row["cluster"]
        for b in labels:
            m[(a, b)] = row[b]
    for a in labels:
        if m[(a, a)] != 0:
            problems.append("co-occurrence diagonal for %s is not zero" % a)
        for b in labels:
            if m[(a, b)] != m[(b, a)]:
                problems.append("co-occurrence not symmetric: %s / %s" % (a, b))
            if a != b and m[(a, b)] > min(size[a], size[b]):
                problems.append("%s x %s = %d exceeds the smaller cluster (%d)"
                                % (a, b, m[(a, b)], min(size[a], size[b])))

    ks = [r["k"] for r in sil]
    if ks != list(range(3, 13)):
        problems.append("silhouette table does not cover k = 3..12")
    chosen = next(r for r in sil if r["k"] == 7)

    return clusters, m, sil, chosen, problems


def main():
    ensure_dirs()
    rc = recompute()
    print("=" * 72)
    print("FREE-TEXT CODING — recomputed from the reviewer coding sheet")
    print("=" * 72)
    for k, v in rc.items():
        print("  %-46s %s" % (k.replace("_", " "), v))

    clusters, cooc, sil, chosen, problems = check_clusters(rc["usable_responses"])
    n = rc["usable_responses"]
    print()
    print("=" * 72)
    print("MULTIMEDIA APPENDIX 5B — consensus clusters (N = %d usable responses)" % n)
    print("=" * 72)
    print("  %-38s%7s%8s%7s%7s%8s"
          % ("Cluster", "n", "%", "str+", "mod+", "neutral"))
    for c in clusters:
        r = c["responses"]
        print("  %-38s%7d%7.1f%%%7s%7s%8s"
              % (c["short_label"], r, 100 * r / n, c["strongly_positive"],
                 c["moderately_positive"], c["neutral_mixed"]))
    print("  %-38s%7d" % ("cluster-response assignments",
                          sum(c["responses"] for c in clusters)))

    print("\n  strongest co-occurrences")
    labels = [c["short_label"] for c in clusters]
    pairs = sorted({tuple(sorted((a, b))): cooc[(a, b)]
                    for a in labels for b in labels if a != b}.items(),
                   key=lambda kv: -kv[1])[:3]
    for (a, b), v in pairs:
        print("    %-36s x %-36s %d" % (a, b, v))

    print("\n  consensus silhouette: k=6 %s, k=7 %s, k=8 %s (selected k=7)"
          % (next(r["consensus_silhouette"] for r in sil if r["k"] == 6),
             chosen["consensus_silhouette"],
             next(r["consensus_silhouette"] for r in sil if r["k"] == 8)))

    if problems:
        print("\n  *** cluster tables failed internal checks ***")
        for p in problems:
            print("    - " + p)
    else:
        print("\n  cluster tables pass all internal consistency checks")

    out = {"recomputed": rc,
           "clusters": [dict(c) for c in clusters],
           "cooccurrence": {"%s|%s" % k: v for k, v in cooc.items()},
           "silhouette": {str(r["k"]): float(r["consensus_silhouette"])
                          for r in sil},
           "problems": problems}
    with open(os.path.join(OUT_DIR, "freetext.json"), "w") as fh:
        json.dump(out, fh, indent=2)
    print("  wrote %s" % os.path.normpath(os.path.join(OUT_DIR, "freetext.json")))

    if "--figures" in sys.argv:
        make_figures(clusters, cooc, sil)
    return out


def make_figures(clusters, cooc, sil):
    """Redraw Figures 4 and 5 and Supplementary Figure S1.

    Plotting follows cell 57 of Diversity_and_Thematic_Analysis.ipynb, so these
    match the submitted artwork. Labels say "cluster", never "theme": reviewer
    G12 asked that this analysis be kept explicitly exploratory.
    """
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    import seaborn as sns

    labels = [c["short_label"] for c in clusters]
    sns.set_theme(style="whitegrid", context="talk")
    plt.rcParams["figure.dpi"] = 160
    plt.rcParams["font.family"] = "DejaVu Sans"

    def emit(name):
        os.makedirs(FIG_DIR, exist_ok=True)
        dest = os.path.join(FIG_DIR, name + ".png")
        plt.savefig(dest, dpi=160, bbox_inches="tight", facecolor="white")
        plt.close()
        print("  wrote %s" % os.path.normpath(dest))

    # ------------------------------ Figure 4: sentiment within clusters ----
    sent = pd.DataFrame(
        {"strongly positive": [c["strongly_positive"] for c in clusters],
         "moderately positive": [c["moderately_positive"] for c in clusters],
         "neutral/mixed": [c["neutral_mixed"] for c in clusters]},
        index=labels).iloc[::-1]
    ax = sent.plot(kind="barh", stacked=True, figsize=(12, 7),
                   color=["#2E8B57", "#E3A008", "#C44E52"], edgecolor="none")
    ax.set_xlabel("Number of coded responses")
    ax.set_ylabel("Cluster label")
    ax.set_title("Sentiment distribution within 7 clusters")
    ax.legend(title="Sentiment", loc="lower right", frameon=True)
    for cont in ax.containers:
        ax.bar_label(cont, labels=[str(int(v)) if v > 0 else ""
                                   for v in cont.datavalues],
                     label_type="center", color="white", fontsize=10)
    plt.tight_layout()
    emit("Figure4_sentiment")

    # ------------------------------------ Figure 5: cluster co-occurrence --
    m = pd.DataFrame([[cooc[(a, b)] for b in labels] for a in labels],
                     index=labels, columns=labels)
    mask = np.triu(np.ones_like(m, dtype=bool), k=0)
    plt.figure(figsize=(11, 8.75))
    sns.heatmap(m, mask=mask, annot=True, fmt="d", cmap="Blues", linewidths=0.5,
                linecolor="white", cbar_kws={"label": "Co-occurring responses"},
                square=True)
    plt.title("Co-occurrence of 7 clusters")
    plt.xlabel("Cluster label")
    plt.ylabel("Cluster label")
    plt.xticks(rotation=35, ha="right")
    plt.yticks(rotation=0)
    plt.tight_layout()
    emit("Figure5_cooccurrence")

    # ------------------------- Supplementary Figure S1: silhouette by k ----
    df = pd.DataFrame({"k": [r["k"] for r in sil],
                       "consensus_silhouette": [float(r["consensus_silhouette"])
                                                for r in sil]})
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=df, x="k", y="consensus_silhouette", marker="o",
                 color="#4C78A8", linewidth=2.5)
    plt.axvline(7, color="#C44E52", linestyle="--", linewidth=2,
                label="Selected 7-cluster solution")
    plt.scatter([7], [df.loc[df["k"].eq(7), "consensus_silhouette"].iloc[0]],
                color="#C44E52", s=120, zorder=5)
    plt.title("Consensus silhouette by candidate number of clusters")
    plt.xlabel("Candidate number of clusters")
    plt.ylabel("Consensus silhouette score")
    plt.xticks(df["k"].tolist())
    plt.legend(frameon=True, loc="lower right")
    plt.tight_layout()
    emit("SupplementaryFigureS1_silhouette")


if __name__ == "__main__":
    main()
