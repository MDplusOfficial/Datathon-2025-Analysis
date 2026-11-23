#!/usr/bin/env python3
"""
Shared helpers: data loaders, cleaning rules for degree, year, motivation and
institution, composite scoring, standardized mean differences, and the
participant cohorts used by every analysis.

The pre-event survey has 306 form rows from 292 registrants. Consent is taken
from each registrant's latest submission; item responses and characteristics
from the earliest submission that contains answers.

Data are read from ../data (override with the DATATHON_DATA variable).
"""
import csv
import os
import re
import statistics
import unicodedata
from collections import defaultdict
from datetime import datetime

import openpyxl

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.environ.get("DATATHON_DATA", os.path.join(HERE, "..", "data"))
OUT_DIR = os.path.join(HERE, "..", "outputs")
FIG_DIR = os.path.join(HERE, "..", "figures")


ITEMS = [
    "Explain core AI concepts",
    "Identify AI-appropriate problems",
    "Interpret AI outputs",
    "Ethical responsibilities",
    "Collaborate with non-clinical",
    "Vision for AI empowerment",
    "AI tools useful for patients",
    "AI improves care effectiveness",
    "Intend to recommend AI",
    "Confident addressing AI questions",
    "Find digital health resources",
    "Judge digital health quality",
    "Use digital tools for self-mgmt",
]
ITEM_CODES = ["R1", "R2", "R3", "R4", "R5", "R6",
              "A1", "A2", "A3", "A4", "D1", "D2", "D3"]
READINESS = [0, 1, 2, 3, 4, 5]
TAM = [6, 7, 8, 9]
LITERACY = [10, 11, 12]
COMPOSITES = [
    ("Medical AI readiness", READINESS),
    ("AI technology acceptance", TAM),
    ("Digital health literacy", LITERACY),
]


def parse_ts(v):
    if isinstance(v, datetime):
        return v
    for f in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M:%S.%f", "%m/%d/%Y %H:%M:%S"):
        try:
            return datetime.strptime(str(v), f)
        except ValueError:
            pass
    return datetime.min


def norm_email(v):
    return str(v).strip().lower() if v else ""


def team_key(name):
    s = unicodedata.normalize("NFKD", str(name))
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]", "", s.lower())


def norm_person(s):
    s = unicodedata.normalize("NFKD", str(s))
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = re.sub(r"^(and|&)\s+", "", s.strip(" \t,;-​").lower())
    s = re.sub(r"^(dr|mr|ms|mrs)\.?\s+", "", s)
    return re.sub(r"\s+", " ", re.sub(r"[^a-z ]", "", s)).strip()


def _path(name):
    return os.path.join(DATA_DIR, name)


def load_pre():
    ws = openpyxl.load_workbook(_path("presurvey.xlsx"), data_only=True).active
    recs = []
    for r in ws.iter_rows(min_row=2, values_only=True):
        if not r[1]:
            continue
        vals = []
        for c in range(6, 19):
            try:
                vals.append(float(r[c]))
            except (TypeError, ValueError):
                vals.append(None)
        recs.append({
            "email": norm_email(r[1]),
            "ts": parse_ts(r[0]),
            "degree": (str(r[2]).strip() if r[2] else ""),
            "year": (str(r[3]).strip() if r[3] else ""),
            "institution": (str(r[4]).strip() if r[4] else ""),
            "consent": (str(r[5]).strip().lower() if r[5] else ""),
            "items": vals,
            "motivation": (str(r[19]).strip() if r[19] else ""),
        })
    consent = {}
    for rec in sorted(recs, key=lambda x: x["ts"]):
        consent[rec["email"]] = rec["consent"]
    out = {}
    for rec in sorted(recs, key=lambda x: (
            not any(v is not None for v in x["items"]), x["ts"])):
        out.setdefault(rec["email"], rec)
    n_sub = {}
    for rec in recs:
        n_sub[rec["email"]] = n_sub.get(rec["email"], 0) + 1
    for email, rec in out.items():
        rec["consent"] = consent[email]
        rec["n_submissions"] = n_sub[email]
    return len(recs), out


def load_post():
    ws = openpyxl.load_workbook(_path("postsurvey.xlsx"), data_only=True).active
    recs = []
    for r in ws.iter_rows(min_row=2, values_only=True):
        if not r[1]:
            continue
        vals = []
        for c in range(3, 16):
            try:
                vals.append(float(r[c]))
            except (TypeError, ValueError):
                vals.append(None)
        recs.append({"email": norm_email(r[1]), "ts": parse_ts(r[0]),
                     "consent": (str(r[2]).strip().lower() if r[2] else ""),
                     "items": vals})
    out = {}
    for rec in sorted(recs, key=lambda x: x["ts"]):
        out[rec["email"]] = rec
    return len(recs), out


def _gda_rows():
    wb = openpyxl.load_workbook(_path("Manuscript Data (Combined).xlsx"),
                                data_only=True)
    ws = wb["Group Dynamic Analysis"]
    rows = [r for r in ws.iter_rows(min_row=2, values_only=True) if r[1]]
    return sorted(rows, key=lambda r: parse_ts(r[0]))


def load_registry():
    out = {}
    for r in _gda_rows():
        out[norm_email(r[1])] = {
            "team": (str(r[2]).strip() if r[2] else ""),
            "degree": r[3], "year": r[4], "institution": r[5],
            "motivation": r[20],
        }
    return out


def load_team_registrations():
    ws = openpyxl.load_workbook(
        _path("Datathon Team Registration (Responses).xlsx"),
        data_only=True)["Form Responses 1"]
    name_cols = [4, 6, 8, 10, 12, 14]
    out = {}
    for r in ws.iter_rows(min_row=2, values_only=True):
        if not any(x is not None and str(x).strip() for x in r):
            continue
        team = str(r[3]).strip() if r[3] else ""
        if not team:
            continue
        members = []
        for c in name_cols:
            if c < len(r) and r[c] and str(r[c]).strip():
                members.append({"name": norm_person(r[c]),
                                "email": norm_email(r[c + 1])})
        ts = str(r[0])
        if team not in out or ts > out[team]["ts"]:
            out[team] = {"ts": ts, "members": members}
    return out


def team_people(reg):
    people = set()
    for v in reg.values():
        for m in v["members"]:
            e = m["email"]
            people.add(e if "@" in e else "name:" + m["name"])
    return people


_NOT_A_NAME = {
    "md", "mbbs", "do", "phd", "ms", "mph", "bs", "ba", "rn", "pharmd", "mba",
    "analysis", "all authors contributed significantly to the conception",
}


def load_submissions():
    wb = openpyxl.load_workbook(_path("Submissions.xlsx"), data_only=True)
    out = defaultdict(set)
    for r in wb["Form Responses 1"].iter_rows(min_row=2, values_only=True):
        if not r[1]:
            continue
        team = str(r[1]).strip()
        out.setdefault(team, set())
        if not r[2]:
            continue
        for part in re.split(r"\n+|\)\s*[,;]|,(?![^()]*\))", str(r[2])):
            part = re.sub(r"^\d+[\.\)]\s*", "", part.strip(" \t,;-​"))
            name = norm_person(re.split(r"\s*\(", part)[0])
            if name and name not in _NOT_A_NAME and " " in name and len(name) <= 60:
                out[team].add(name)
    return dict(out)


def load_free_text_coding():
    wb = openpyxl.load_workbook(_path("Submissions.xlsx"), data_only=True)
    ws = wb["ThemeSentiment Reviewer Analysi"]
    quotes = "‘’“”'\""

    def codes(cell):
        if cell is None:
            return []
        txt = str(cell).strip()
        if not txt or txt.lower() in ("none", "n/a", "-"):
            return []
        out = []
        for p in re.split(r"[,;\n]+", txt):
            p = re.sub(r"\s+", " ", p.strip().strip(quotes).strip().lower())
            if p:
                out.append(p)
        return out

    recs = []
    for r in ws.iter_rows(min_row=4, values_only=True):
        if not r[1]:
            continue
        recs.append({"team": str(r[1]).strip(), "text": r[8],
                     "kb": codes(r[10]), "kb_sent": r[11],
                     "sm": codes(r[12]), "sm_sent": r[13]})
    return recs


def bucket_degree(s):
    if s is None or str(s).strip() == "" or str(s).lower() == "nan":
        return "Unknown"
    d = str(s).lower().strip()
    if any(x in d for x in ["dual", "md/phd", "md/ms", "md/master", "mstp"]):
        return "Dual Degree (MD/PhD, MD/MS)"
    if any(x in d for x in ["resident", "fellow", "intern", "pgy"]):
        return "Resident/Fellow"
    if "phd" in d and "md" not in d:
        return "PhD Student"
    if any(x in d for x in ["master", "msc", "mph", "ms ", "m.s."]):
        return "Master's Student"
    if any(x in d for x in ["md", "do", "mbbs", "medical"]):
        return "Medical Student (MD/DO)"
    if any(x in d for x in ["dds", "dmd", "dental", "b.d.s"]):
        return "Dental Student"
    if "pharmd" in d or "pharmacist" in d:
        return "PharmD"
    if any(x in d for x in ["undergraduate", "bachelor", "undergrad", "^bs$",
                            "b.s."]):
        return "Undergraduate"
    if any(x in d for x in ["research", "founder", "n/a", "gap year"]):
        return "Other / Non-Student"
    return "Other"


def clean_year(s):
    if s is None:
        return None
    try:
        return int(float(str(s).replace("+", "").strip()))
    except ValueError:
        return None


MOTIVATION_MAP = {
    "Wanting to work on a healthcare problem solving team project": "Team Project",
    "A combination of learning AI skills and publication": "Skills & Publication",
    "Learning AI Skills": "Learn AI Skills",
    "Publication": "Publication",
    "Networking": "Networking",
    "Interest": "General Interest",
}


def bucket_motivation(s):
    return MOTIVATION_MAP.get(str(s).strip(), "Other")


INSTITUTION_MAP = {
    r'sinai|icahn|mssm|ismms': 'Icahn School of Medicine at Mount Sinai',
    r'utsw|ut\s*southwestern|university of texas southwestern': 'UT Southwestern',
    r'brown|warren\s*alpert': 'Brown University (Warren Alpert)',
    r'loyola|stritch': 'Loyola Stritch School of Medicine',
    r'unc|chapel\s*hill|university of north carolina': 'UNC Chapel Hill',
    r'ucsf|university of california.*san francisco': 'UCSF',
    r'gwu|george\s*washington|gw\s*(school|smhs)': 'George Washington University',
    r'tufts': 'Tufts University',
    r'stanford': 'Stanford University',
    r'emory': 'Emory University',
    r'ucla|david\s*geffen': 'UCLA',
    r'university of miami|miami.*miller': 'University of Miami',
    r'uic|university of illinois': 'University of Illinois',
    r'drexel': 'Drexel University',
    r'northwestern|feinberg': 'Northwestern University',
    r'westernu|western\s*university\s*of\s*health': 'Western University of Health Sciences',
    r'nymc|new\s*york\s*medical\s*college': 'New York Medical College',
    r'rochester': 'University of Rochester',
    r'rush': 'Rush Medical College',
    r'einstein': 'Albert Einstein College of Medicine',
    r'yale': 'Yale School of Medicine',
    r'penn|perelman': 'University of Pennsylvania',
    r'rutgers': 'Rutgers',
    r'hackensack|hmhn': 'Hackensack Meridian School of Medicine',
    r'tulane': 'Tulane University',
    r'duke': 'Duke University',
    r'weill\s*cornell': 'Weill Cornell',
    r'vcu|virginia\s*commonwealth': 'Virginia Commonwealth University',
    r'baylor': 'Baylor College of Medicine',
    r'university of southern california|^usc$': 'University of Southern California',
    r'ucsd': 'UC San Diego',
    r'\buci\b': 'UC Irvine',
    r'fsu|florida\s*state': 'Florida State University',
    r'georgetown': 'Georgetown University',
    r'midwestern': 'Midwestern University',
    r'lecom': 'LECOM',
    r'medical\s*college\s*of\s*georgia': 'Medical College of Georgia',
    r'uab|alabama.*birmingham': 'University of Alabama at Birmingham',
    r'suny\s*downstate': 'SUNY Downstate',
    r'obafemi|oauife': 'Obafemi Awolowo University',
    r'usmanu|danfod': 'Usmanu Danfodiyo University',
    r'carle': 'Carle Illinois College of Medicine',
    r'umkc|missouri.*kansas': 'University of Missouri-Kansas City',
    r'ohsu|oregon\s*health': 'Oregon Health & Science University',
    r'creighton': 'Creighton University',
    r'nyu|grossman': 'NYU Grossman School of Medicine',
    r'stevens\s*institute': 'Stevens Institute of Technology',
    r'texas\s*a&?m|tamu': 'Texas A&M',
    r'pittsburgh|upmc|carnegie\s*mellon': 'University of Pittsburgh',
    r'university of michigan': 'University of Michigan',
    r'university of maryland|umaryland': 'University of Maryland',
    r'nebraska': 'University of Nebraska',
    r'louisville': 'University of Louisville',
    r'cincinnati': 'University of Cincinnati',
    r'colorado|anschutz': 'University of Colorado',
    r'nevada.*reno': 'University of Nevada Reno',
    r'georgia.*tech|ga\s*tech': 'Georgia Institute of Technology',
    r'upstate\s*medical': 'Upstate Medical University',
    r'quinnipiac|netter': 'Quinnipiac University (Netter)',
    r'mcmaster': 'McMaster University',
    r'berkeley': 'UC Berkeley',
    r'nyit': 'NYIT College of Osteopathic Medicine',
    r'wright\s*state': 'Wright State University',
    r'neomed': 'Northeast Ohio Medical University',
    r'geisinger': 'Geisinger Commonwealth',
    r'eastern\s*virginia': 'Eastern Virginia Medical School',
    r'dell\s*medical': 'Dell Medical School',
    r'california\s*northstate': 'California Northstate University',
}

_INST_SKIP = [r'^n/?a', r'graduated', r'gap\s*year', r'left\s*clinical',
              r'curanostics', r'conduct\s*science', r'freenome', r'uptotrials',
              r'employee']
_INST_INTL = ['international', 'turkey', 'istanbul', 'brazil', 'porto alegre',
              'lagos', 'pakistan', 'lahore', 'egypt', 'bahamas', 'marmara',
              'cayetano', 'gulf medical', 'sgu', 'caribbean', 'turkische',
              'ilorin']
INTL_NAMED = {'Obafemi Awolowo University', 'Usmanu Danfodiyo University',
              'McMaster University'}


def bucket_institution(v):
    if v is None or str(v).strip() == "" or str(v).lower() == "nan":
        return "Other"
    s = str(v).lower().strip()
    if any(re.search(p, s) for p in _INST_SKIP):
        return "Other / N/A"
    for pattern, name in INSTITUTION_MAP.items():
        if re.search(pattern, s):
            return name
    if any(k in s for k in _INST_INTL):
        return "Other (International)"
    return "Other"


_EXTRA_INTL = ['cerrahpa']


def is_international(v):
    cat = bucket_institution(v)
    if cat == "Other (International)" or cat in INTL_NAMED:
        return True
    s = str(v).lower() if v else ""
    return any(k in s for k in _EXTRA_INTL)


INSTITUTION_MAP_SUPPLEMENT = {
    r'cayetano': 'Cayetano Heredia University',
    r'gulf\s*medical': 'Gulf Medical University',
    r'istanbul\s*technical': 'Istanbul Technical University',
    r'cerrahpa': 'Istanbul University-Cerrahpasa',
    r'lagos': 'Lagos State University College of Medicine',
    r'marmara': 'Marmara University',
    r'\bmisr\b|university for science and technology': 'Misr University for Science and Technology',
    r"queen'?s\s*university": "Queen's University",
    r'\bsgu\b': "St George's University",
    r'turkische|turkisch[- ]deutsche': 'Turkish-German University',
    r'porto\s*alegre': 'Universidade Federal de Ciencias da Saude de Porto Alegre',
    r'ilorin': 'University of Ilorin',
    r'medical\s*university\s*of\s*so': 'Medical University of South Carolina',
    r'north\s*carolina\s*state': 'North Carolina State University',
    r'northeastern': 'Northeastern University',
    r'\biu school of medicine|indiana\s*university': 'Indiana University School of Medicine',
    r'university of california,?\s*los\s*angeles': 'UCLA',
}

NOT_AN_INSTITUTION = [
    r'conduct\s*science', r'conductscience', r'curanostics', r'freenome',
    r'uptotrials',
    r'^graduated?$', r'^n/?a$', r'^n/?a\s*\(graduated\)$', r'^left\s*clinical',
]

TEACHING_HOSPITALS = {
    'Evercare Hospital Lahore', 'Garden City Hospital',
    'Maine Medical Center - Portland',
}
_HOSPITAL_PATTERNS = {
    r'evercare': 'Evercare Hospital Lahore',
    r'garden\s*city\s*hospital': 'Garden City Hospital',
    r'maine\s*medical\s*center': 'Maine Medical Center - Portland',
}


def institution_identity(v):
    if v is None or str(v).strip() == "" or str(v).lower() == "nan":
        return None, None
    s = str(v).lower().strip()
    if any(re.search(p, s) for p in NOT_AN_INSTITUTION):
        return None, None
    for pattern, name in _HOSPITAL_PATTERNS.items():
        if re.search(pattern, s):
            return name, "hospital"
    for pattern, name in INSTITUTION_MAP.items():
        if re.search(pattern, s):
            return name, "academic"
    for pattern, name in INSTITUTION_MAP_SUPPLEMENT.items():
        if re.search(pattern, s):
            return name, "academic"
    return None, None


def count_institutions(records):
    out = {"academic": set(), "hospital": set(), "unresolved": set()}
    for v in records:
        if v is None or not str(v).strip():
            continue
        name, kind = institution_identity(v)
        if kind:
            out[kind].add(name)
        elif not any(re.search(p, str(v).lower().strip())
                     for p in NOT_AN_INSTITUTION):
            out["unresolved"].add(str(v).strip())
    return out


TEAM_ALIASES = {
    "Plater": "The Washington Post",
    "Data!": "Algorhythm",
    "Neuron and Co": "Neuron & Co.",
    "NoroNest": "NöroNest",
    "Ghanta-Branscom": "Ghanta-Branscom School of Marwaha-Duan at Borges Robles",
    "Code Dependency": "Code Dependencies",
    "NobleEdge": "NobelEdge",
    "The Pythons": "Pythons",
    "Brachialplexusasorus": "Brachioplexusosaurus",
    "neuroncdocs": "Neurondoc",
    "A for effort": "A for Effort",
}

UNREGISTERED_SUBMITTING_TEAMS = ["Artificially Intelligent"]


def composite(vals, idx):
    xs = [vals[i] for i in idx if vals[i] is not None]
    return sum(xs) / len(xs) if xs else None


def mean_sd(xs):
    xs = [x for x in xs if x is not None]
    if not xs:
        return None, None, 0
    if len(xs) == 1:
        return xs[0], 0.0, 1
    return statistics.mean(xs), statistics.stdev(xs), len(xs)


def smd_continuous(a, b):
    ma, sa, na = mean_sd(a)
    mb, sb, nb = mean_sd(b)
    if ma is None or mb is None or na < 2 or nb < 2:
        return None
    pooled = (((na - 1) * sa ** 2 + (nb - 1) * sb ** 2) / (na + nb - 2)) ** 0.5
    return 0.0 if pooled == 0 else (ma - mb) / pooled


def smd_proportion(pa, pb):
    denom = ((pa * (1 - pa) + pb * (1 - pb)) / 2) ** 0.5
    return 0.0 if denom == 0 else (pa - pb) / denom


def cronbach_alpha(rows):
    k = len(rows[0])
    item_var = sum(statistics.variance([r[i] for r in rows]) for i in range(k))
    tot_var = statistics.variance([sum(r) for r in rows])
    return k / (k - 1) * (1 - item_var / tot_var)


DATASET = os.environ.get("DATATHON_DATASET",
                         os.path.join(DATA_DIR, "datathon_dataset.xlsx"))

_CACHE = {}


def load_dataset(path=None):
    path = path or DATASET
    if path in _CACHE:
        return _CACHE[path]
    if not os.path.exists(path):
        raise SystemExit(
            "dataset not found: %s\n"
            "Build it first:  python src/s00_build_dataset.py" % path)
    wb = openpyxl.load_workbook(path, data_only=True)
    out = {}
    for name in wb.sheetnames:
        ws = wb[name]
        header = [c.value for c in ws[1]]
        rows = []
        for r in ws.iter_rows(min_row=2, values_only=True):
            if all(v is None for v in r):
                continue
            rows.append(dict(zip(header, r)))
        out[name] = rows
    out["meta"] = {r["key"]: r["value"] for r in out["meta"]}
    for r in out["participants"]:
        r["pre"] = [r.pop("pre_%d" % i) for i in range(1, 14)]
        r["post"] = [r.pop("post_%d" % i) for i in range(1, 14)]
    _CACHE[path] = out
    return out


def cohorts(path=None):
    ds = load_dataset(path)
    P = {r["participant_id"]: r for r in ds["participants"]}

    def flag(col, val="y"):
        return {k for k, v in P.items() if v[col] == val}

    return {
        "ds": ds, "P": P, "meta": ds["meta"],
        "teams": ds["teams"], "projects": ds["projects"],
        "consented": flag("consented"),
        "post": flag("post_responded"),
        "post_consent": flag("post_consented"),
        "paired": flag("paired"),
        "on_submitting": flag("on_submitting_team"),
        "group_A": flag("comparison_group", "A"),
        "group_B": flag("comparison_group", "B"),
        "group_C": flag("comparison_group", "C"),
    }


def ensure_dirs():
    for d in (OUT_DIR, FIG_DIR):
        os.makedirs(d, exist_ok=True)
