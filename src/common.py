#!/usr/bin/env python3
"""
common.py — single source of truth for every loader and coding rule.
=====================================================================

Every script in this package imports its data through this module. Nothing else
reads a spreadsheet directly. That is the point: the round-2 review asked us to
confirm that the shared code produces the reported numbers, and the only way to
guarantee that is to have exactly one implementation of each rule.

Data files live in ../data (override with $DATATHON_DATA).

Rules that are easy to get wrong, and are therefore fixed here:

  * pre-event survey de-duplication. 306 form rows, 292 unique registrants.
    CONSENT is taken from the participant's LATEST submission (a later answer
    supersedes an earlier one). ITEM RESPONSES and CHARACTERISTICS are taken
    from the EARLIEST submission that actually contains answers. Both failure
    modes exist in this dataset: one registrant re-registered with a blank item
    block, another abandoned a first submission and completed it three days
    later. Latest-wins alone loses a complete baseline; earliest-wins alone
    keeps an empty record. This split rule is why the consented denominator is
    264 and not 263.

  * post-event survey de-duplication: LATEST submission per email.

  * demographics for the appendix tables come from the Group Dynamic Analysis
    sheet (latest registration per email) — the same record Figure 2 plots — so
    Multimedia Appendix 7 cannot contradict Figure 2. Composite SCORES still
    come from the pre-event survey.

  * degree / year / motivation / institution buckets are the ones the Figure 2
    notebook uses, reproduced verbatim.
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

# --------------------------------------------------------------- instrument --

ITEMS = [
    "Explain core AI concepts",            # 0  } Medical AI readiness
    "Identify AI-appropriate problems",    # 1  }
    "Interpret AI outputs",                # 2  }
    "Ethical responsibilities",            # 3  }
    "Collaborate with non-clinical",       # 4  }
    "Vision for AI empowerment",           # 5  }
    "AI tools useful for patients",        # 6  } AI technology acceptance
    "AI improves care effectiveness",      # 7  }
    "Intend to recommend AI",              # 8  }
    "Confident addressing AI questions",   # 9  }
    "Find digital health resources",       # 10 } Digital health literacy
    "Judge digital health quality",        # 11 }
    "Use digital tools for self-mgmt",     # 12 }
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


# ------------------------------------------------------------------ helpers --

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
    """Collapse spacing / punctuation / case so team names match across files."""
    s = unicodedata.normalize("NFKD", str(name))
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]", "", s.lower())


def norm_person(s):
    """Normalise a free-text member name for de-duplication."""
    s = unicodedata.normalize("NFKD", str(s))
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = re.sub(r"^(and|&)\s+", "", s.strip(" \t,;-​").lower())
    s = re.sub(r"^(dr|mr|ms|mrs)\.?\s+", "", s)
    return re.sub(r"\s+", " ", re.sub(r"[^a-z ]", "", s)).strip()


def _path(name):
    return os.path.join(DATA_DIR, name)


# =========================================================================
# RAW LOADERS — used ONLY by s00_build_dataset.py
# =========================================================================
# These open the source exports and apply the de-duplication and linkage rules
# described above. No analysis script calls them; analyses read the built
# dataset through load_dataset() / cohorts() further down. Keeping the two
# layers apart is what stops a fuzzy match being re-derived, slightly
# differently, in two places.

def load_pre():
    """presurvey.xlsx -> (n_form_rows, {email: record}).

    See the module docstring for the split de-duplication rule.
    """
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
    for rec in sorted(recs, key=lambda x: x["ts"]):          # latest wins
        consent[rec["email"]] = rec["consent"]
    out = {}
    for rec in sorted(recs, key=lambda x: (                  # earliest non-empty
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
    """postsurvey.xlsx -> (n_form_rows, {email: record}), latest wins."""
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
    """Group Dynamic Analysis -> {email: record}, latest registration wins.

    This sheet holds only the consenting cohort (n=264) and is the record
    Figure 2 plots. Columns: 2 team, 3 degree, 4 year, 5 institution,
    20 motivation.
    """
    out = {}
    for r in _gda_rows():
        out[norm_email(r[1])] = {
            "team": (str(r[2]).strip() if r[2] else ""),
            "degree": r[3], "year": r[4], "institution": r[5],
            "motivation": r[20],
        }
    return out


def load_team_registrations():
    """Team-registration form -> {team name: {"members": [...], "ts": ...}}.

    "Datathon Team Registration (Responses).xlsx", one row per team: col 3 is
    the team name, cols 4/6/8/10/12/14 the member names and cols 5/7/9/11/13/15
    the matching emails.

    49 rows carry 225 non-empty member-name cells. DataSuture filed the form
    twice, listing five members on 20 Oct and six on 27 Oct; keeping only the
    later row leaves **48 teams and 220 member names**, which is the figure the
    manuscript reports. 220 counts name slots, not distinct people — resolving
    each slot to its email, and falling back to the name where the email cell is
    blank or junk, gives 218.

    Note that 220 EXCLUDES Artificially Intelligent, which submitted a project
    but never filed a team registration. 48 registered teams + that one is the
    49 teams the manuscript reports, so the true headcount across all 49 teams
    is about 226. 220 is kept because it is what this form reproduces.
    """
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
        if team not in out or ts > out[team]["ts"]:     # latest filing wins
            out[team] = {"ts": ts, "members": members}
    return out


def team_people(reg):
    """Distinct people across a load_team_registrations() result.

    Two member rows carry "." in the email cell and one carries none at all, so
    identity falls back to the normalised name when the email is not usable.
    """
    people = set()
    for v in reg.values():
        for m in v["members"]:
            e = m["email"]
            people.add(e if "@" in e else "name:" + m["name"])
    return people


# Free-text entries in the submission form's "Team Members" column that are not
# people: contribution prose, and bare credentials left behind when a name such
# as "Deep Shelke, MBBS" is split on its comma.
_NOT_A_NAME = {
    "md", "mbbs", "do", "phd", "ms", "mph", "bs", "ba", "rn", "pharmd", "mba",
    "analysis", "all authors contributed significantly to the conception",
}


def load_submissions():
    """Submissions.xlsx -> {team name: {member}} for the 31 submitting teams.

    34 form rows; Brunologix, The Washington Post and Trifusion each submitted
    twice, so members are unioned across a team's rows.
    """
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
    """Reviewer free-text coding -> list of per-response records.

    Sheet "ThemeSentiment Reviewer Analysi" of Submissions.xlsx. Header spans
    rows 1-3; data starts at row 4. Columns 10/11 = coder KB codes/sentiment,
    12/13 = coder SM, 14/15 = a third coder who did not code this round.
    """
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


# -------------------------------------------------------------- categorical --
# Reproduced verbatim from diversity/demographics_and_diversity.ipynb so these
# tables cannot contradict the categories plotted in Figure 2.

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
    """Year in program as an integer; "6+" becomes 6.

    openpyxl reads this column out of presurvey.xlsx as a float and out of the
    Group Dynamic Analysis sheet as text, so float() comes before int().
    """
    if s is None:
        return None
    try:
        return int(float(str(s).replace("+", "").strip()))
    except ValueError:
        return None


# The motivation item offered a fixed list plus a free-text "Other", so these
# are the response options themselves, not an induced coding. Everything not
# listed here is a free-text answer and falls into "Other".
# NOTE: Multimedia Appendix 2 currently describes the options as "Learning AI
# skills, Publishing, Networking, Patient impact, Prize, Other". No response in
# the data reads "Patient impact" or "Prize"; three read "Funding". See
# AUDIT_REPORT.md.
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
# Keyword list for schools outside the United States that are not named in
# INSTITUTION_MAP. This drives the "Other (International)" bucket of Figure 2C
# and, through it, panel E.
_INST_INTL = ['international', 'turkey', 'istanbul', 'brazil', 'porto alegre',
              'lagos', 'pakistan', 'lahore', 'egypt', 'bahamas', 'marmara',
              'cayetano', 'gulf medical', 'sgu', 'caribbean', 'turkische',
              'ilorin']
# Schools named in INSTITUTION_MAP that are outside the United States.
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


# Counting participants at schools outside the United States is a separate
# question from "how many distinct institutions is this team drawn from", so it
# gets its own rule rather than reusing the display buckets. One entry is missed
# by the bucket keywords: Istanbul University-Cerrahpasa, entered with a Turkish
# dotted capital I and a misspelt "Uneversity".
# Not counted: "UofL (previous - University of Toronto)", where the current
# institution is the University of Louisville.
_EXTRA_INTL = ['cerrahpa']


def is_international(v):
    """True if this free-text institution is outside the United States."""
    cat = bucket_institution(v)
    if cat == "Other (International)" or cat in INTL_NAMED:
        return True
    s = str(v).lower() if v else ""
    return any(k in s for k in _EXTRA_INTL)


# ------------------------------------------------- the institution census --
# "292 registrants from N institutions" is a different question from the one
# bucket_institution() answers. That function is a DISPLAY bucketing: it powers
# Figure 2C's bar chart and, through it, panel E's team-diversity matrix, and it
# deliberately sweeps anything it does not recognise into Other, Other
# (International) or Other / N/A. Counting distinct institutions needs those
# buckets opened up, so it gets its own resolver and its own two lists. Changing
# anything below cannot move a figure.
#
# INSTITUTION_MAP recognises 68 institutions across the 292 registrants. Thirty
# further distinct strings land in an Other bucket. Of those: 10 are not
# institutions at all, 1 is another spelling of an institution already counted
# (UCLA), 3 are teaching hospitals rather than degree-granting schools, and the
# remaining 16 are genuine academic institutions the map simply lacks a pattern
# for. 68 + 16 = **84 degree-granting academic institutions**, or 87 counting
# the teaching hospitals.

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
    # Not a new institution: the long spelling of UCLA, which INSTITUTION_MAP
    # matches only as "ucla" or "david geffen". Listed so the census resolves
    # every string; it adds nothing to the count.
    r'university of california,?\s*los\s*angeles': 'UCLA',
}

# Free-text answers in the institution field that name no institution: five
# employers and five non-answers.
NOT_AN_INSTITUTION = [
    r'conduct\s*science', r'conductscience', r'curanostics', r'freenome',
    r'uptotrials',
    r'^graduated?$', r'^n/?a$', r'^n/?a\s*\(graduated\)$', r'^left\s*clinical',
]

# Named, but hospitals rather than degree-granting schools. Counted separately
# so the headline figure stays "academic institutions".
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
    """Resolve a free-text institution to a canonical name.

    Returns (name, kind) where kind is "academic", "hospital" or None. None
    means the answer names no institution.
    """
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
    """records = iterable of free-text institution answers.

    Returns {"academic": set, "hospital": set, "unresolved": set}.
    "unresolved" should stay empty; anything in it is a string no list covers
    and needs a decision before the count can be reported.
    """
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


# ------------------------------------------------------------ team aliases --
# Teams that registered under one name and submitted under another. team_key()
# already absorbs case, spacing, punctuation and accents, so only genuine
# renames and misspellings need listing. Without these, naive name matching
# badly undercounts the participants eligible for the post-event survey.
#
# Each key is a registration-time spelling; the value is the submission-form
# spelling it refers to.
TEAM_ALIASES = {
    "Plater": "The Washington Post",        # 6 of 6 members match
    "Data!": "Algorhythm",                  # renamed itself before submitting
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

# Artificially Intelligent submitted a project but never filed a team
# registration, so it is absent from the team-registration export. 48 registered
# teams + this one = the 49 teams the manuscript reports.
UNREGISTERED_SUBMITTING_TEAMS = ["Artificially Intelligent"]


# -------------------------------------------------------------- statistics ---

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
    """Standardised mean difference between two groups, pooled SD."""
    ma, sa, na = mean_sd(a)
    mb, sb, nb = mean_sd(b)
    if ma is None or mb is None or na < 2 or nb < 2:
        return None
    pooled = (((na - 1) * sa ** 2 + (nb - 1) * sb ** 2) / (na + nb - 2)) ** 0.5
    return 0.0 if pooled == 0 else (ma - mb) / pooled


def smd_proportion(pa, pb):
    """SMD for one binary category."""
    denom = ((pa * (1 - pa) + pb * (1 - pb)) / 2) ** 0.5
    return 0.0 if denom == 0 else (pa - pb) / denom


def cronbach_alpha(rows):
    """rows = complete item vectors (no missing values)."""
    k = len(rows[0])
    item_var = sum(statistics.variance([r[i] for r in rows]) for i in range(k))
    tot_var = statistics.variance([sum(r) for r in rows])
    return k / (k - 1) * (1 - item_var / tot_var)


# =========================================================================
# THE DATASET — what every analysis script reads
# =========================================================================
# One file, built once by s00_build_dataset.py, de-identified, with every
# record-linkage decision already resolved. Analyses do arithmetic on these
# columns and never touch a raw export.

DATASET = os.environ.get("DATATHON_DATASET",
                         os.path.join(DATA_DIR, "datathon_dataset.xlsx"))

_CACHE = {}


def load_dataset(path=None):
    """The built dataset as {sheet_name: [row dict, ...]}, plus meta as a dict."""
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
    # collapse the 13 item columns into lists, which is how every analysis
    # wants them
    for r in out["participants"]:
        r["pre"] = [r.pop("pre_%d" % i) for i in range(1, 14)]
        r["post"] = [r.pop("post_%d" % i) for i in range(1, 14)]
    _CACHE[path] = out
    return out


def cohorts(path=None):
    """Every group the paper uses, keyed by participant_id.

    Returns the dataset plus:
      P             {participant_id: row}
      consented     the 264 who consented at registration
      post          the 91 who completed the post-event survey
      post_consent  the 84 of those who consented on that form
      paired        the 69 analysed
      on_submitting the consenting registrants on a submitting team
      group_A/B/C   the three mutually exclusive Multimedia Appendix 7 groups
    """
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
