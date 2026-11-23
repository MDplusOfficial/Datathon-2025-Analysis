# Datathon Analysis: Consolidated Data for Figures/Tables

Coding record for Table 1 (clinical domains) and Table 2 (patient-empowerment
mechanisms), across the 31 submitted projects.

`src/s05_projects.py` computes both tables from this file.

> **Superseded content removed 2026-09-16.** This file previously also held a
> project-by-theme grid of tick marks, a domain x theme cross-tabulation, and a
> "mean themes per project: 2.3" statement. The grid had fallen out of sync with
> the counts below (46 ticks against 50 assignments) and the cross-tabulation
> disagreed with both. The counts below are the coding of record, and are what
> Table 2 reports. The removed sections are not recoverable from this file.

---

# CLINICAL DOMAINS (Mutually Exclusive)

Each of the 31 projects is assigned to exactly one clinical domain, on the basis
of its primary focus.

| Clinical Domain | N | % | Projects |
|-----------------|---|---|----------|
| **Women's Health** | 9 | 29% | Bayes Anatomy, DeepDishLearning, FulldataScientists, Ghanta-Branscom, Neuron&Co, SSOM2, StarPeak, Aforeffort, NobelEdge |
| **Mental Health** | 4 | 13% | Algorhythm, NeurOnCDoc, KPopDataHunters, AIDO |
| **General Inpatient** | 4 | 13% | CLaRA, Curanostics, CareBridge, TLDR |
| **Diabetes** | 3 | 10% | Brachioplexusaurus, DA-Med-plus, NöroNest |
| **Emergency Medicine** | 3 | 10% | ArtificiallyIntelligent, Brunologix, Pythons |
| **Critical Care** | 3 | 10% | TeamMidBest, CodeDependencies, TheWashingtonPost |
| **Cardiology** | 2 | 6% | HeartRead, Trifusion |
| **Radiology** | 1 | 3% | GoldenGateGPTs |
| **Pharmacy** | 1 | 3% | RxGuardian |
| **Surgery** | 1 | 3% | Therayes |
| **TOTAL** | **31** | **100%** | |

Labels are the ones Table 1 prints. Percentages are of the 31 projects.

### Codebook revision: the removal of "Health Communication"

The initial clinical-domain scheme carried an eleventh category, "Health
Communication". It was removed after the first coding round because it cut
across clinical domains rather than constituting one; its six projects were
reassigned to the domain of their clinical context, and health communication was
retained as a cross-cutting descriptor. This leaves the 10 mutually exclusive
domains above.

- CLaRA → General Inpatient (discharge summaries, multi-condition)
- Curanostics → General Inpatient (discharge summary simplification)
- CareBridge → General Inpatient (discharge summaries, care transitions)
- TLDR → General Inpatient (lab results across conditions)
- GoldenGateGPTs → Radiology (chest X-ray reports)
- Brunologix → Emergency Medicine (ED interpreter, ED disparity analysis)

No other category was removed, merged or renamed. In particular Mental Health
was retained: a merge into a broader chronic-disease category was considered
during analysis and not adopted.

---

# PATIENT EMPOWERMENT MECHANISMS (Non-Exclusive)

Each project is assigned to every applicable mechanism, so the percentages sum
to more than 100%.

## Definitions

| Mechanism | Definition |
|-------|------------|
| **Symptom Forecasting** | AI tools that predict future health states, enabling patients to anticipate and prepare for symptoms or risks |
| **Actionable Self-Management** | AI tools that help patients identify modifiable factors, understand personal patterns, and take personalized action |
| **Health Literacy** | AI tools that translate complex medical information into accessible, understandable formats tailored to patient needs |
| **Patient-Clinician Communication** | AI tools that strengthen patients' ability to participate as partners in care by facilitating dialogue with providers |
| **Health Equity** | AI tools that extend healthcare capabilities to underserved populations by removing barriers of language, geography, cost, or resources |
| **AI Transparency** | AI tools that build patient trust through source verification, acknowledged limitations, and appropriate epistemic humility |

## Frequencies

| Mechanism | N | % of Projects |
|-------|---|---------------|
| **Symptom Forecasting** | 12 | 39% |
| **Actionable Self-Management** | 10 | 32% |
| **Health Literacy** | 8 | 26% |
| **Patient-Clinician Communication** | 8 | 26% |
| **Health Equity** | 6 | 19% |
| **AI Transparency** | 6 | 19% |

50 assignments across 31 projects, a mean of 1.6 mechanisms per project. The
total and the mean are derived from the N column above, not stored separately.

---

## Summary

- 31 projects, 10 mutually exclusive clinical domains, range 1-9 projects per domain
- Most common domain: Women's Health (9, 29%)
- 6 empowerment mechanisms, all represented across the corpus
- Most common mechanism: Symptom Forecasting (12, 39%)
- Every project addresses at least one mechanism
