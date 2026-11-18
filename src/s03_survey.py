#!/usr/bin/env python3
"""
s03_survey.py — Table 3 (composite pre-post) and Multimedia Appendix 6
(item-level pre-post), for the 69 paired respondents.

Wilcoxon signed-rank, two-sided, normal approximation, Benjamini-Hochberg
corrected across the three composites and separately across the 13 items.
Effect size r = Z / sqrt(N) with N = 69 paired respondents (not the number of
non-tied pairs), which is the convention the manuscript reports.

Composites are means of AVAILABLE items; no minimum number of completed items
is required. Cronbach alpha is computed on complete item vectors only, which is
why its n is slightly below 69.

Writes outputs/survey.json.
"""
import json
import os
import statistics
import sys

from scipy.stats import wilcoxon
from statsmodels.stats.multitest import multipletests

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import (COMPOSITES, ITEM_CODES, ITEMS, OUT_DIR, cohorts,
                    composite, cronbach_alpha, ensure_dirs)


def _wilcoxon(pre, post):
    pairs = [(a, b) for a, b in zip(pre, post) if a is not None and b is not None]
    xs = [p[0] for p in pairs]
    ys = [p[1] for p in pairs]
    res = wilcoxon(ys, xs, zero_method="wilcox", alternative="two-sided",
                   method="approx")
    return xs, ys, abs(res.zstatistic), res.pvalue


def main():
    ensure_dirs()
    c = cohorts()
    P = c["P"]
    paired = sorted(c["paired"])
    n = len(paired)

    out = {"n_paired": n, "composites": [], "items": []}

    # ------------------------------------------------------------- Table 3 --
    rows, pvals = [], []
    for lbl, idx in COMPOSITES:
        a = [composite(P[e]["pre"], idx) for e in paired]
        b = [composite(P[e]["post"], idx) for e in paired]
        xs, ys, z, p = _wilcoxon(a, b)
        pvals.append(p)
        alphas = []
        for when in ("pre", "post"):
            vecs = [[P[e][when][i] for i in idx] for e in paired
                    if all(P[e][when][i] is not None for i in idx)]
            alphas.append((cronbach_alpha(vecs), len(vecs)))
        rows.append((lbl, len(idx), xs, ys, z, p, alphas))
    adj = multipletests(pvals, method="fdr_bh")[1]

    print("=" * 86)
    print("TABLE 3 — pre-post changes in survey composite scores "
          f"(N = {n} paired respondents)")
    print("=" * 86)
    print(f"  {'Composite (items)':34s}{'Pre':>13s}{'Post':>13s}"
          f"{'alpha':>13s}{'Z':>7s}{'r':>6s}{'p_adj':>11s}")
    for (lbl, k, xs, ys, z, p, alphas), pa in zip(rows, adj):
        mpre, spre = statistics.mean(xs), statistics.stdev(xs)
        mpost, spost = statistics.mean(ys), statistics.stdev(ys)
        r = z / n ** 0.5
        print(f"  {lbl + ' (%d)' % k:34s}"
              f"{'%.2f (%.2f)' % (mpre, spre):>13s}"
              f"{'%.2f (%.2f)' % (mpost, spost):>13s}"
              f"{'%.2f / %.2f' % (alphas[0][0], alphas[1][0]):>13s}"
              f"{z:>7.2f}{r:>6.2f}{pa:>11.2e}")
        out["composites"].append({
            "label": lbl, "n_items": k, "n": len(xs),
            "pre_mean": round(mpre, 2), "pre_sd": round(spre, 2),
            "post_mean": round(mpost, 2), "post_sd": round(spost, 2),
            "alpha_pre": round(alphas[0][0], 2), "alpha_pre_n": alphas[0][1],
            "alpha_post": round(alphas[1][0], 2), "alpha_post_n": alphas[1][1],
            "Z": round(z, 2), "r": round(r, 2), "p": p, "p_adj": pa,
        })

    # --------------------------------------------------- Appendix 6 (items) --
    item_rows, pvals = [], []
    for i, name in enumerate(ITEMS):
        a = [P[e]["pre"][i] for e in paired]
        b = [P[e]["post"][i] for e in paired]
        xs, ys, z, p = _wilcoxon(a, b)
        pvals.append(p)
        item_rows.append((name, ITEM_CODES[i], xs, ys, z, p))
    adj = multipletests(pvals, method="fdr_bh")[1]
    ranked = sorted(zip(item_rows, adj),
                    key=lambda t: -(statistics.mean(t[0][3])
                                    - statistics.mean(t[0][2])))

    print()
    print("=" * 86)
    print("MULTIMEDIA APPENDIX 6 — item-level pre-post changes "
          "(Wilcoxon, BH corrected)")
    print("=" * 86)
    print(f"  {'Item':42s}{'code':>6s}{'n':>5s}{'Pre':>7s}{'Post':>7s}"
          f"{'d':>7s}{'Z':>7s}{'r':>6s}{'p_adj':>11s}")
    for (name, code, xs, ys, z, p), pa in ranked:
        mpre, mpost = statistics.mean(xs), statistics.mean(ys)
        r = z / len(xs) ** 0.5
        print(f"  {name:42s}{code:>6s}{len(xs):>5d}{mpre:>7.2f}{mpost:>7.2f}"
              f"{mpost - mpre:>+7.2f}{z:>7.2f}{r:>6.2f}{pa:>11.4f}")
        out["items"].append({
            "item": name, "code": code, "n": len(xs),
            "pre": round(mpre, 2), "post": round(mpost, 2),
            "delta": round(mpost - mpre, 2), "Z": round(z, 2),
            "r": round(r, 2), "p": p, "p_adj": pa,
        })
    ns = [len(xs) for _, _, xs, _, _, _ in item_rows]
    out["item_n_range"] = [min(ns), max(ns)]
    print(f"\n  per-item n ranges from {min(ns)} to {max(ns)} of {n}")

    with open(os.path.join(OUT_DIR, "survey.json"), "w") as fh:
        json.dump(out, fh, indent=2)
    print(f"  wrote {os.path.normpath(os.path.join(OUT_DIR, 'survey.json'))}")
    return out


if __name__ == "__main__":
    main()
