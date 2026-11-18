# Datathon Thematic Analysis: Three-Layer Framework
## "Empowering Patients Through AI" Safe Patient Medical AI Datathon

---

# LAYER 1: Technical & Methodological Inventory

## 1.1 Machine Learning / Statistical Methods

| Method | Projects Using | Team Names |
|--------|---------------|------------|
| **XGBoost** | 5 | AIDO, Brachioplexusaurus, Pythons, Ghanta-Branscom, Trifusion |
| **Random Forest** | 7 | Algorhythm, NöroNest, FulldataScientists, KPopDataHunters, SSOM2, StarPeak, Therayes |
| **Logistic Regression** | 6 | DA-Med-plus, NöroNest, RxGuardian, SSOM2, Therayes, HeartRead |
| **Gradient Boosting (general/LightGBM)** | 4 | NeurOnCDoc, SSOM2, HeartRead, NöroNest |
| **Deep Neural Networks** | 2 | Neuron&Co (multi-output DNN), Trifusion |
| **K-Nearest Neighbors** | 1 | NöroNest |
| **Support Vector Machines** | 1 | CodeDependencies |
| **K-means Clustering** | 3 | Bayes Anatomy, Pythons, StarPeak |
| **Mixed Effects / Linear Regression** | 3 | DeepDishLearning, NobelEdge, Aforeffort |
| **Cox Proportional Hazards** | 1 | ArtificiallyIntelligent |
| **Quantile Regression** | 1 | ArtificiallyIntelligent |
| **Dynamic Time Warping** | 1 | KPopDataHunters |
| **Isotonic Calibration** | 1 | NeurOnCDoc |

**Summary Statistics:**
- Total unique ML/statistical methods: 13
- Most common: Random Forest (7), Logistic Regression (6), XGBoost (5)
- Range per project: 1-3 methods typically compared

---

## 1.2 Large Language Models & NLP Tools

| LLM / NLP Tool | Projects Using | Application |
|----------------|---------------|-------------|
| **GPT-OSS-20b / GPT-OSS-120b** | 3 | CareBridge (discharge summaries), GoldenGateGPTs (radiology), KPopDataHunters (forecasting) |
| **Llama 3.1 / 3.3** | 2 | GoldenGateGPTs (radiology reports), KPopDataHunters (forecasting) |
| **Gemini 2.5 Pro** | 1 | TLDR/Staphylococcus Aura (lab result summaries) |
| **JSL-MedLlama-3-8B-v2.0** | 1 | Curanostics (discharge simplification) |
| **ChatGPT (API)** | 1 | AIDO (patient explanation generation) |
| **DeepSeek-V3** | 1 | KPopDataHunters (forecasting comparison) |
| **Gemma 3** | 1 | KPopDataHunters (forecasting comparison) |
| **Phi-4** | 1 | KPopDataHunters (forecasting comparison) |
| **Perplexity Sonar API** | 1 | CLaRA (source-restricted search) |
| **Whisper** | 1 | Brunologix (speech recognition) |
| **Hume AI** | 1 | Brunologix (emotion detection & TTS) |
| **Google Translate API** | 1 | Brunologix (translation) |
| **MedCPT** | 1 | Pythons (clinical text embeddings) |
| **MiniLM** | 1 | NeurOnCDoc (embeddings for clustering) |
| **BERT / BERTScore** | 3 | CareBridge, GoldenGateGPTs, Bayes Anatomy (evaluation/similarity) |
| **medSpaCy** | 1 | GoldenGateGPTs (clinical accuracy) |
| **TF-IDF** | 1 | Bayes Anatomy (response divergence) |
| **Rule-based NLP** | 2 | HeartRead (SDOH extraction), TheWashingtonPost (posture extraction) |

**Summary Statistics:**
- Projects using LLMs for generation: 7
- Projects using NLP for extraction/embedding: 6
- Projects using LLMs for evaluation: 3
- Unique LLM architectures tested: 10+

---

## 1.3 Datasets Utilized

| Dataset | Projects Using | Description |
|---------|---------------|-------------|
| **MIMIC-IV** | 15 | ArtificiallyIntelligent, Brachioplexusaurus, Brunologix, CLaRA, CodeDependencies, Curanostics, HeartRead, RxGuardian, CareBridge, TeamMidBest, TheWashingtonPost, Therayes, Trifusion, TLDR, Pythons |
| **MIMIC-IV-ED** | 3 | ArtificiallyIntelligent, Brunologix, Pythons |
| **MIMIC-IV-Note** | 3 | Curanostics, CareBridge, TheWashingtonPost |
| **MIMIC-CXR** | 2 | GoldenGateGPTs, (referenced in CareBridge) |
| **mcPHASES** | 9 | Bayes Anatomy, DeepDishLearning, FulldataScientists, Ghanta-Branscom, Neuron&Co, SSOM2, StarPeak, Aforeffort, (referenced) |
| **Flaredown** | 4 | Algorhythm, NeurOnCDoc, NobelEdge, KPopDataHunters |
| **BRFSS 2015** | 1 | NöroNest |
| **Diabetes Datathon Dataset** | 1 | DA-Med-plus |
| **Chronic Illness Symptoms Dataset** | 1 | AIDO |

**Summary Statistics:**
- MIMIC ecosystem: 18 projects (58%)
- mcPHASES (women's health): 9 projects (29%)
- Flaredown (chronic illness): 4 projects (13%)
- Population survey (BRFSS): 1 project

---

## 1.4 Evaluation Metrics & Frameworks

| Metric / Framework | Projects Using | Purpose |
|--------------------|---------------|---------|
| **AUROC / AUC** | 18 | Discrimination performance |
| **SHAP Analysis** | 9 | Feature importance / interpretability |
| **Precision / Recall / F1** | 12 | Classification performance |
| **Accuracy** | 10 | Overall correctness |
| **Flesch Reading Ease** | 4 | Readability assessment |
| **Gunning Fog Index** | 2 | Readability assessment |
| **Flesch-Kincaid Grade Level** | 2 | Readability assessment |
| **BERTScore** | 2 | Semantic similarity |
| **ROUGE-L** | 1 | Text similarity |
| **Brier Score** | 1 | Calibration |
| **Mean Absolute Error / RMSE** | 3 | Regression performance |
| **R² Score** | 2 | Variance explained |
| **Natural Language Inference** | 1 | Factuality checking |
| **Cosine Similarity (TF-IDF)** | 1 | Response divergence |
| **Permutation Importance** | 1 | Feature importance |

**Summary Statistics:**
- Most common: AUROC (18), Precision/Recall/F1 (12), Accuracy (10)
- Interpretability-focused: SHAP (9 projects)
- Health literacy metrics: 5 projects used readability scores

---

## 1.5 Output Modalities / Interfaces

| Output Type | Projects | Examples |
|-------------|----------|----------|
| **Risk Score / Probability** | 14 | Depression risk, mortality risk, flare probability |
| **Patient-Facing Dashboard/App** | 8 | Axia, CLaRA, SynClari, patient dashboards |
| **Simplified Text Summary** | 6 | Discharge summaries, lab reports, radiology reports |
| **Chatbot Interface** | 2 | DA-Med-plus, Ghanta-Branscom (planned) |
| **Clinician Alert/Report** | 4 | EHR alerts, PDF reports for clinicians |
| **Real-time Translation** | 1 | Brunologix speech-to-speech |
| **Interactive Visualization** | 4 | Timelines, risk radars, lab graphs |
| **Research/Descriptive Output** | 5 | Disparity quantification, descriptive analysis |

---

# LAYER 2: Clinical Domain & Specialty Mapping

## 2.1 Primary Clinical Domain by Project

> **This is the INITIAL coding scheme, before the codebook revision.** It has 12
> categories, including "Health Communication (Cross-cutting)", and its counts
> overlap — several projects appear twice and some rows carry "(partial: ...)"
> notes. It is kept as the record of the first coding round, which the response
> to reviewer G11 describes.
>
> The **final** scheme is the 10 mutually exclusive domains in
> `datathon_consolidated_data.md`, which is what Table 1 prints and what
> `reproducibility/src/s05_projects.py` reads. Health Communication was removed
> because it cut across domains rather than constituting one, and its six
> projects were reassigned to the domain of their clinical context. No other
> category was removed or merged; Mental Health was retained.

| Clinical Domain | N | Projects |
|-----------------|---|----------|
| **Women's Health / Reproductive** | 9 | Bayes Anatomy, DeepDishLearning, FulldataScientists, Ghanta-Branscom, Neuron&Co, SSOM2, StarPeak, Aforeffort, (partial: NobelEdge) |
| **Mental Health / Psychiatry** | 3 | AIDO, KPopDataHunters, (partial: Neuron&Co) |
| **Diabetes / Endocrinology** | 3 | Brachioplexusaurus, DA-Med-plus, NöroNest |
| **Chronic Disease / Pain** | 4 | Algorhythm, NeurOnCDoc, NobelEdge, (partial: multiple) |
| **Cardiovascular / Heart Failure** | 2 | CodeDependencies, HeartRead |
| **Emergency Medicine** | 3 | ArtificiallyIntelligent, Brunologix, Pythons |
| **Critical Care / ICU** | 3 | TeamMidBest, CodeDependencies, TheWashingtonPost |
| **Orthopedic Surgery** | 1 | Therayes |
| **Radiology** | 1 | GoldenGateGPTs |
| **Pharmacy / Medication Safety** | 1 | RxGuardian |
| **General Inpatient / Hospitalist** | 2 | Trifusion, (partial: multiple) |
| **Health Communication (Cross-cutting)** | 6 | CLaRA, Curanostics, CareBridge, TLDR, GoldenGateGPTs, Brunologix |

**Summary statistics for the initial scheme above, not for Table 1:**
- Women's health: 29% of projects (notably high representation)
- Mental health: 10%
- Health communication/literacy: 19% (cross-cutting; category later removed)
- Emergency/critical care combined: 19%

---

## 2.2 Patient Population Focus

| Population | N | Projects |
|------------|---|----------|
| **General Adult Inpatients** | 10 | Various MIMIC-based projects |
| **Menstruating Adults / Women** | 9 | mcPHASES-based projects |
| **Chronic Illness Patients** | 4 | Flaredown-based projects |
| **Emergency Department Patients** | 4 | ED-focused projects |
| **ICU Patients** | 4 | Critical care projects |
| **Older Adults (≥65)** | 2 | RxGuardian, (partial: others) |
| **Limited English Proficiency** | 2 | ArtificiallyIntelligent, Brunologix |
| **Low-Resource Settings (Global)** | 1 | DA-Med-plus (rural Africa) |
| **Diabetic Patients** | 3 | Diabetes-focused projects |
| **Post-Surgical Patients** | 1 | Therayes |

---

# LAYER 3: Patient Empowerment Thematic Analysis (Braun & Clarke)

## 3.1 Refined Coding for Patient Empowerment

After reviewing all projects through the lens of "how does this empower patients," I identified the following refined codes:

### Empowerment Mechanism Codes:

**Understanding & Comprehension**
- `simplifies-medical-language` - Translates jargon to plain language
- `adjusts-to-reading-level` - Customizes complexity to patient literacy
- `contextualizes-results` - Explains findings in patient's specific situation
- `provides-citations` - Links to trustworthy sources for verification
- `visualizes-health-data` - Makes abstract data concrete through graphics

**Anticipation & Preparation**
- `predicts-future-symptoms` - Forecasts symptom occurrence or severity
- `identifies-risk-windows` - Highlights high-risk periods (e.g., menstrual phases)
- `enables-proactive-planning` - Allows patients to prepare for bad days
- `provides-early-warning` - Alerts before problems manifest

**Self-Management & Agency**
- `identifies-modifiable-triggers` - Shows factors patients can change
- `supports-lifestyle-decisions` - Guides sleep, diet, activity choices
- `tracks-personal-patterns` - Reveals individual trends over time
- `provides-personalized-recommendations` - Tailored action suggestions

**Access & Inclusion**
- `removes-language-barriers` - Translation for LEP patients
- `works-in-low-resource-settings` - No lab/specialist requirement
- `reduces-cost-barriers` - Alternative to expensive tests
- `preserves-emotional-nuance` - Maintains human connection in translation

**Voice & Participation**
- `supports-shared-decision-making` - Prepares patients for clinician conversations
- `generates-clinician-ready-summaries` - Patient can bring data to appointments
- `quantifies-patient-experience` - Validates subjective symptoms with data
- `documents-disparities` - Makes inequities visible and actionable

**Safety & Trust**
- `uses-verified-sources` - Restricts to trusted medical information
- `acknowledges-uncertainty` - Transparent about what AI doesn't know
- `maintains-human-oversight` - Designed to augment, not replace, clinicians
- `flags-when-to-seek-care` - Directs to professional help when needed

---

## 3.2 Project-by-Code Matrix (Empowerment Focus)

Primary codes only, and five projects carry a prose note in place
of codes. This is a record of the coding process, **not** the
theme-assignment record; Table 2's counts are in
`datathon_consolidated_data.md`.

| Project | Primary Empowerment Codes |
|---------|--------------------------|
| AIDO | predicts-future-symptoms, provides-personalized-recommendations, supports-shared-decision-making |
| Algorhythm | predicts-future-symptoms, identifies-modifiable-triggers, enables-proactive-planning |
| ArtificiallyIntelligent | documents-disparities, (future: removes-language-barriers) |
| Bayes Anatomy | provides-personalized-recommendations, tracks-personal-patterns |
| Brachioplexusaurus/Axia | visualizes-health-data, supports-shared-decision-making, generates-clinician-ready-summaries |
| Brunologix | removes-language-barriers, preserves-emotional-nuance, documents-disparities |
| CLaRA | simplifies-medical-language, adjusts-to-reading-level, provides-citations, contextualizes-results |
| CodeDependencies | provides-early-warning, supports-shared-decision-making |
| Curanostics | simplifies-medical-language, adjusts-to-reading-level |
| DA-Med-plus | works-in-low-resource-settings, reduces-cost-barriers, provides-personalized-recommendations |
| DeepDishLearning | tracks-personal-patterns, identifies-risk-windows, supports-shared-decision-making |
| FulldataScientists | reduces-cost-barriers, tracks-personal-patterns |
| Ghanta-Branscom | tracks-personal-patterns, provides-personalized-recommendations |
| GoldenGateGPTs | simplifies-medical-language, contextualizes-results |
| HeartRead | documents-disparities, (future: supports-shared-decision-making) |
| KPopDataHunters | predicts-future-symptoms, enables-proactive-planning |
| Neuron&Co/SynClari | predicts-future-symptoms, identifies-risk-windows, enables-proactive-planning |
| NeurOnCDoc | predicts-future-symptoms, identifies-modifiable-triggers, provides-personalized-recommendations |
| NobelEdge | identifies-modifiable-triggers, quantifies-patient-experience |
| NöroNest | (screening/triage - indirect empowerment) |
| Pythons | supports-shared-decision-making, simplifies-medical-language |
| RxGuardian | (clinician-focused - indirect patient safety) |
| CareBridge | simplifies-medical-language, adjusts-to-reading-level, provides-actionable-next-steps |
| SSOM2 | predicts-future-symptoms, identifies-risk-windows, enables-proactive-planning |
| TLDR | simplifies-medical-language, adjusts-to-reading-level, contextualizes-results |
| StarPeak | tracks-personal-patterns, provides-personalized-recommendations |
| TeamMidBest | (risk stratification - indirect prevention) |
| TheWashingtonPost | (exploratory - biomarker identification) |
| Therayes | provides-early-warning, (clinician decision support) |
| Trifusion | (mortality prediction - indirect through understanding severity) |
| Aforeffort | tracks-personal-patterns, quantifies-patient-experience |

---

## 3.3 Theme Development: Patient Empowerment Through AI

### THEME 1: Empowerment Through Health Literacy & Comprehension
**Definition:** AI tools that translate complex medical information into accessible, understandable formats tailored to individual patient needs.

**Core Idea:** Patients cannot be empowered by information they cannot understand. These projects bridge the gap between clinical documentation (written for providers) and patient comprehension.

**Constituent Codes:**
- simplifies-medical-language
- adjusts-to-reading-level  
- contextualizes-results
- provides-citations
- visualizes-health-data

**Representative Projects** (illustrative, not the full assignment list):
- CLaRA (reading-level-adjustable explanations with citations)
- Curanostics (discharge summary simplification to 6th grade)
- CareBridge (tiered literacy levels)
- TLDR (lab result translation)
- GoldenGateGPTs (radiology report simplification)
- Axia (risk radar visualization)

**Illustrative Quote from Abstracts:**
> "By reducing reliance on unverified sources while prioritizing accessibility, CLaRA empowers patients to take control of their medical literacy" (CLaRA)

**Frequency:** 8 projects (26%)

---

### THEME 2: Empowerment Through Anticipation & Proactive Planning
**Definition:** AI tools that predict future health states, enabling patients to prepare for and potentially mitigate negative outcomes.

**Core Idea:** Uncertainty is disempowering. When patients can anticipate symptoms, flares, or risks, they can plan their lives, prepare interventions, and feel more in control of conditions that otherwise feel unpredictable.

**Constituent Codes:**
- predicts-future-symptoms
- identifies-risk-windows
- enables-proactive-planning
- provides-early-warning

**Representative Projects** (illustrative, not the full assignment list):
- Algorhythm (next-day symptom worsening)
- NeurOnCDoc (IA and epilepsy flare forecasting)
- SSOM2 (menstrual symptom prediction)
- KPopDataHunters (anxiety/depression trajectory)
- Neuron&Co (cognitive fatigue forecasting)
- AIDO (depression risk stratification)

**Illustrative Quote from Abstracts:**
> "AI can provide meaningful support for chronic illness management by reducing uncertainty and highlighting modifiable triggers" (Algorhythm)

> "Reliable short-term forecasts could support anticipatory guidance (e.g., mini-prophylaxis, acute medication readiness, workload planning)" (SSOM2)

**Frequency:** 9 projects (29%)

---

### THEME 3: Empowerment Through Self-Management & Personalized Agency
**Definition:** AI tools that help patients understand their individual patterns, identify factors within their control, and take personalized action.

**Core Idea:** Empowerment requires agency. These projects go beyond prediction to show patients *what they can do* - identifying modifiable triggers, revealing personal patterns, and providing tailored recommendations.

**Constituent Codes:**
- identifies-modifiable-triggers
- supports-lifestyle-decisions
- tracks-personal-patterns
- provides-personalized-recommendations

**Representative Projects** (illustrative, not the full assignment list):
- Algorhythm (sleep, alcohol, coffee as modifiable factors)
- NeurOnCDoc (sleep disturbance, behavioral factors)
- NobelEdge (weather sensitivity awareness)
- StarPeak (sensitivity phenotypes for personalized guidance)
- Ghanta-Branscom (cycle-aware metabolic recommendations)
- Aforeffort (Menstrual Health Index for self-monitoring)

**Illustrative Quote from Abstracts:**
> "Feature importance analysis revealed that variables related to sleep quality, temperature variability, and activity intensity contributed most strongly" (FulldataScientists)

> "The model empowers patients to better understand their symptoms and take proactive steps toward improvement" (AIDO)

**Frequency:** 10 projects (32%)

---

### THEME 4: Empowerment Through Equitable Access & Inclusion
**Definition:** AI tools that extend healthcare capabilities to underserved populations by removing barriers of language, geography, cost, or resource availability.

**Core Idea:** Empowerment is meaningless if tools only serve the privileged. These projects specifically address disparities in who can access quality healthcare information and services.

**Constituent Codes:**
- removes-language-barriers
- works-in-low-resource-settings
- reduces-cost-barriers
- preserves-emotional-nuance
- documents-disparities

**Representative Projects** (illustrative, not the full assignment list):
- Brunologix (emotion-aware medical interpreter)
- DA-Med-plus (Tele-AI for rural Africa, no labs needed)
- ArtificiallyIntelligent (quantifying pain management disparities)
- HeartRead (SDOH integration, disparity documentation)
- FulldataScientists (alternative to expensive LH kits)

**Illustrative Quote from Abstracts:**
> "Most existing machine learning models for diabetes prediction rely on laboratory or wearable devices and are developed in high-income countries, limiting applicability in low-resource settings" (DA-Med-plus)

> "Both race/ethnicity and primary language are independent predictors of delayed analgesic administration... highlighting systemic inequities" (ArtificiallyIntelligent)

**Frequency:** 6 projects (19%)

---

### THEME 5: Empowerment Through Voice & Partnership in Care
**Definition:** AI tools that strengthen patients' ability to participate as partners in their healthcare by facilitating communication with clinicians and validating patient experiences.

**Core Idea:** Patients are empowered when they can speak effectively with their care teams, bring meaningful data to appointments, and have their lived experiences acknowledged and quantified.

**Constituent Codes:**
- supports-shared-decision-making
- generates-clinician-ready-summaries
- quantifies-patient-experience
- provides-actionable-next-steps

**Representative Projects** (illustrative, not the full assignment list):
- Axia (PDF reports for office visits)
- DeepDishLearning (guides patient-clinician discussions)
- NeurOnCDoc (patient-friendly explanations for shared decision-making)
- NobelEdge (validates patient reports of weather sensitivity)
- Aforeffort (quantifies menstrual health as clinical metric)
- CareBridge (actionable next steps tracking)

**Illustrative Quote from Abstracts:**
> "By combining EHR-based ML models with an accessible, patient-centered interface, Axia empowers users to interpret their health data, improves clinical efficiency, and supports value-based care initiatives" (Axia)

> "We hope that creating a data-driven metric will increase patient transparency into medical decision-making" (Aforeffort)

**Frequency:** 8 projects (26%)

---

### THEME 6: Empowerment Through Trustworthy & Transparent AI
**Definition:** AI tools that build patient trust through source verification, acknowledged limitations, and appropriate epistemic humility.

**Core Idea:** Patients can only be empowered by AI they can trust. These projects explicitly address concerns about AI reliability, hallucination, and overconfidence.

**Constituent Codes:**
- uses-verified-sources
- acknowledges-uncertainty
- maintains-human-oversight
- flags-when-to-seek-care

**Representative Projects** (illustrative, not the full assignment list):
- CLaRA (source-restricted to trusted sites, citations provided)
- NöroNest ("models of this type are best viewed as screening or triage aids")
- CareBridge (safety constraints, source verification)
- Curanostics ("readability metrics serve only as proxies for understanding")
- Multiple projects with "limitations acknowledged" and "future validation needed"

**Illustrative Quote from Abstracts:**
> "Our system outputted... citations if prompted in the script, ensuring verifiability" (CLaRA)

> "Future work should include external validation, calibration analysis, and prospective evaluation of decision thresholds to study clinical utility and potential harms (false negatives/false positives) before deployment" (NöroNest)

**Frequency:** Explicitly addressed in 6 projects; implicitly present in 15+ through limitations sections

---

## 3.4 Thematic Map

```
                    PATIENT EMPOWERMENT THROUGH AI
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
   INFORMATION           ANTICIPATION          PARTNERSHIP
        │                     │                     │
   ┌────┴────┐           ┌────┴────┐          ┌────┴────┐
   │         │           │         │          │         │
LITERACY  CONTEXT    PREDICTION  PLANNING   VOICE   DIALOGUE
   │         │           │         │          │         │
   └────┬────┘           └────┬────┘          └────┬────┘
        │                     │                     │
        └──────────┬──────────┴──────────┬─────────┘
                   │                     │
              SELF-MANAGEMENT      EQUITABLE ACCESS
                   │                     │
              ┌────┴────┐           ┌────┴────┐
              │         │           │         │
           TRIGGERS  PATTERNS   LANGUAGE  RESOURCES
              │         │           │         │
              └────┬────┘           └────┬────┘
                   │                     │
                   └──────────┬──────────┘
                              │
                    TRUSTWORTHY & TRANSPARENT AI
                    (Foundation for all empowerment)
```

---

## 3.5 Theme Summary Table

Counts of record are in `datathon_consolidated_data.md`, which is what
`reproducibility/src/s05_projects.py` reads and what Table 2 prints. They are
repeated here for reading convenience only.

| Theme | Table 2 label | N Projects | % |
|-------|---------------|------------|---|
| 1. Health Literacy & Comprehension | Health literacy | 8 | 26% |
| 2. Anticipation & Proactive Planning | Symptom forecasting | 12 | 39% |
| 3. Self-Management & Personalized Agency | Actionable self-management | 10 | 32% |
| 4. Equitable Access & Inclusion | Health equity | 6 | 19% |
| 5. Voice & Partnership in Care | Patient-clinician communication | 8 | 26% |
| 6. Trustworthy & Transparent AI | AI transparency | 6 | 19% |

*Projects often span multiple themes, so percentages do not sum to 100%.
50 assignments across 31 projects, a mean of 1.6.*

> An earlier version of this table gave 9 for theme 2 and "6+" for theme 6,
> which matched neither Table 2 nor the file above. Corrected 2026-09-16.

---

## 3.6 Cross-Cutting Observations

### Women's Health as Empowerment Frontier
- 9 projects (29%) focused on menstrual/reproductive health
- Addresses historically under-researched area
- Leverages novel dataset (mcPHASES) enabling personalized tracking
- Empowerment themes: anticipation, self-management, pattern recognition

### Chronic Disease as Empowerment Paradigm
- 4 projects using Flaredown data (these sit in the Mental Health domain in
  Table 1; "chronic disease" here describes the conditions, not a domain label)
- Chronic conditions particularly suited to empowerment framing (long-term self-management)
- Uncertainty reduction especially valuable for unpredictable conditions

### Health Literacy as Foundational
- 6 projects directly address health literacy
- Implicit in many others (plain-language explanations)
- Recognized as prerequisite for other empowerment mechanisms

### Equity as Ethical Imperative
- Explicit disparity analysis in 4 projects
- Resource-conscious design in 2 projects
- Suggests student awareness of AI ethics concerns

---

# Summary Statistics for Manuscript

## Technical Breadth
- **13** distinct ML/statistical methods employed
- **10+** unique LLM architectures tested
- **4** major dataset ecosystems (MIMIC, mcPHASES, Flaredown, BRFSS)
- **8** output modalities (dashboards, chatbots, summaries, etc.)

## Clinical Diversity
- **10** clinical domains represented (see `datathon_consolidated_data.md`)
- **10** distinct patient populations addressed
- Most common: Women's health (9, 29%); then Mental health and General
  inpatient (4 each, 13%)

## Patient Empowerment Mechanisms
- **6** mechanisms identified
- Most common: Symptom forecasting (12, 39%)
- All 31 projects addressed at least one mechanism
- 50 assignments across 31 projects, a mean of **1.6** per project

> Corrected 2026-09-16. This block previously read "12 clinical domains",
> "Most common: Women's health (29%), Health communication (19%)" — a category
> removed during the first coding round — and "Mean themes per project: 2.3".

---

*Analysis completed following Braun & Clarke (2006) thematic analysis methodology*
*Phase 1: Familiarization - Complete*
*Phase 2: Initial Coding - Complete*
*Phase 3: Searching for Themes - Complete*
*Phase 4: Reviewing Themes - Complete*
*Phase 5: Defining and Naming Themes - Complete*
*Phase 6: Producing Report - This document*
