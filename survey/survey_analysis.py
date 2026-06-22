#!/usr/bin/env python3
"""
survey_analysis.py
==================
Pre/post survey analysis for the MD+ Datathon 2025 paper.

Computes:
  1. Participant funnel: registrants -> consented -> matched pre/post pairs (n=69)
  2. Three composite constructs (Wilcoxon signed-rank, BH-corrected):
        - Medical AI Readiness        (6 MAIRS-MS items)
        - AI Technology Acceptance    (4 patient-facing TAM items)
        - Digital Health Literacy     (3 items)
  3. Item-level mean change ranking (all 13 items)

Pipeline:
  pre  = signup/pre-survey, dedup by email keeping EARLIEST, consent == "Yes"
  post = post-survey,       dedup by email keeping LATEST,   consent == "Yes"
  pairs = emails present in both with >=1 item answered on each side

Usage:
    python survey_analysis.py
    DATATHON_DATA=/path/to/data python survey_analysis.py
"""
import os, statistics
from datetime import datetime
import openpyxl
from scipy.stats import wilcoxon
from statsmodels.stats.multitest import multipletests

DATA_DIR = os.environ.get(
    "DATATHON_DATA",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data"),
)

# 13 Likert items, in the column order they appear in both exports.
ITEMS = [
    "Explain core AI concepts",            # 0  } Medical AI Readiness (MAIRS-MS)
    "Identify AI-appropriate problems",    # 1  }
    "Interpret AI outputs",                # 2  }
    "Ethical responsibilities",            # 3  }
    "Collaborate with non-clinical",       # 4  }
    "Vision for AI empowerment",           # 5  }
    "AI tools useful for patients",        # 6  } AI Technology Acceptance (TAM, patient-facing)
    "AI improves care effectiveness",      # 7  }
    "Intend to recommend AI",              # 8  }
    "Confident addressing AI questions",   # 9  }
    "Find digital health resources",       # 10 } Digital Health Literacy
    "Judge digital health quality",        # 11 }
    "Use digital tools for self-mgmt",     # 12 }
]
READINESS = [0, 1, 2, 3, 4, 5]
TAM       = [6, 7, 8, 9]
LITERACY  = [10, 11, 12]


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
    """Return list of (email, timestamp, consent, [13 item values])."""
    wb = openpyxl.load_workbook(os.path.join(DATA_DIR, fname), data_only=True)
    ws = wb.active
    recs = []
    for r in ws.iter_rows(min_row=2, values_only=True):
        if not r[email_col]:
            continue
        email = str(r[email_col]).strip().lower()
        consent = str(r[consent_col]).strip().lower() if r[consent_col] else ""
        vals = []
        for c in range(first_item_col, first_item_col + 13):
            try:
                vals.append(float(r[c]))
            except (TypeError, ValueError):
                vals.append(None)
        recs.append((email, parse_ts(r[0]), consent, vals))
    return recs


def composite(vals, idx):
    xs = [vals[i] for i in idx if vals[i] is not None]
    return sum(xs) / len(xs) if xs else None


def main():
    # Column layout: pre-survey email=1 consent=5 items=6..18 ; post email=1 consent=2 items=3..15
    pre_recs  = load("presurvey.xlsx", 1, 5, 6)
    post_recs = load("postsurvey.xlsx", 1, 2, 3)

    # dedup: pre keeps earliest, post keeps latest
    pre = {}
    for e, ts, con, v in sorted(pre_recs, key=lambda x: x[1]):
        pre.setdefault(e, (ts, con, v))
    post = {}
    for e, ts, con, v in sorted(post_recs, key=lambda x: x[1]):
        post[e] = (ts, con, v)  # last wins

    print("PARTICIPANT FUNNEL")
    print(f"  pre-survey rows .................. {len(pre_recs)}")
    print(f"  unique registrants (pre) ......... {len(pre)}")
    print(f"  post-survey rows ................. {len(post_recs)}")
    print(f"  unique post respondents .......... {len(post)}")

    pre = {e: v for e, v in pre.items() if v[1] == "yes"}
    post = {e: v for e, v in post.items() if v[1] in ("yes", "y", "true", "1")}
    print(f"  consented registrants (pre) ...... {len(pre)}")
    print(f"  consented post respondents ....... {len(post)}")

    pairs = []
    for e in pre:
        if e in post:
            pv, qv = pre[e][2], post[e][2]
            if any(x is not None for x in pv) and any(x is not None for x in qv):
                pairs.append((pv, qv))
    print(f"  matched pre/post pairs (n) ....... {len(pairs)}")

    print("\nCOMPOSITE CONSTRUCTS (pre -> post, Wilcoxon signed-rank, BH-corrected)")
    groups = [("Medical AI Readiness (6)", READINESS),
              ("AI Technology Acceptance / TAM (4)", TAM),
              ("Digital Health Literacy (3)", LITERACY)]
    pvals, rows = [], []
    for label, idx in groups:
        keep = [(composite(p, idx), composite(q, idx)) for p, q in pairs]
        keep = [(a, b) for a, b in keep if a is not None and b is not None]
        a = [x[0] for x in keep]; b = [x[1] for x in keep]
        p = wilcoxon(b, a).pvalue
        pvals.append(p)
        rows.append((label, len(keep), statistics.mean(a), statistics.mean(b),
                     statistics.mean(b) - statistics.mean(a)))
    padj = multipletests(pvals, method="fdr_bh")[1]
    for (label, n, pre_m, post_m, d), pa in zip(rows, padj):
        print(f"  {label:36s} n={n}  pre={pre_m:.2f}  post={post_m:.2f}  "
              f"Delta=+{d:.2f}  p_adj={pa:.2e}")

    print("\nITEM-LEVEL MEAN CHANGE (ranked; Wilcoxon, BH-corrected)")
    res, ipv = [], []
    for i, name in enumerate(ITEMS):
        d = [(q[i] - p[i]) for p, q in pairs if p[i] is not None and q[i] is not None]
        pre_v = [p[i] for p, q in pairs if p[i] is not None and q[i] is not None]
        post_v = [q[i] for p, q in pairs if p[i] is not None and q[i] is not None]
        pv = wilcoxon(post_v, pre_v).pvalue
        res.append([name, statistics.mean(d), len(d)]); ipv.append(pv)
    ipadj = multipletests(ipv, method="fdr_bh")[1]
    for r, pa in zip(res, ipadj):
        r.append(pa)
    for name, d, n, pa in sorted(res, key=lambda r: -r[1]):
        star = "***" if pa < 0.001 else "**" if pa < 0.01 else "*" if pa < 0.05 else "ns"
        print(f"  {d:+.3f}  {star:>3}  (n={n}, p_adj={pa:.4f})  {name}")


if __name__ == "__main__":
    main()
