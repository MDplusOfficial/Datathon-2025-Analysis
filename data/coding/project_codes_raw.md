# Thematic Analysis: Systematic Coding of Datathon Abstracts
## Safe Patient Medical AI Datathon

### Phase 2: Initial Coding (Inductive Approach)

---

## 1. AIDO (Depression Risk Stratification)

**Project Summary:** ML model using XGBoost to predict depression improvement/risk, integrated with SHAP explanations and ChatGPT-generated patient feedback for value-based mental healthcare.

**Initial Codes:**
- `risk-stratification` - Core function is stratifying patients by depression risk
- `patient-facing-explanations` - SHAP-informed text alerts to patients
- `interpretability-shap` - Uses SHAP for feature importance
- `llm-explanation-generation` - ChatGPT generates supportive explanations
- `dual-pathway-workflow` - Different interventions for low vs high risk
- `ehr-integration` - Provider alerts within EHR
- `self-management-support` - Directs low-risk patients to self-management resources
- `proactive-outreach` - High-risk patients trigger provider outreach
- `patient-empowerment` - Aims to help patients understand their symptoms
- `value-based-care-alignment` - Explicitly frames around VBHC principles

---

## 2. Algorhythm (Chronic Illness Symptom Prediction)

**Project Summary:** Random Forest model predicting next-day symptom worsening for chronic illness patients using Flaredown data, identifying modifiable factors.

**Initial Codes:**
- `symptom-forecasting` - Predicts next-day symptom worsening
- `chronic-disease-management` - Focus on chronic illness population
- `modifiable-factors-identification` - Identifies actionable triggers (sleep, alcohol, coffee)
- `patient-empowerment` - Aims to reduce uncertainty for patients
- `self-management-support` - Highlights factors patients can modify
- `modest-performance-acknowledged` - Explicitly notes 62.7% accuracy as modest
- `future-patient-tool` - Envisions translation to patient-facing tools
- `lifestyle-factors` - Sleep, alcohol, coffee, water as predictors

---

## 3. ArtificiallyIntelligent (ED Pain Management Disparities)

**Project Summary:** Retrospective analysis of MIMIC-IV showing racial/ethnic and language-based disparities in time to analgesia for severe pain in the ED.

**Initial Codes:**
- `health-equity-analysis` - Core focus on disparities
- `racial-ethnic-disparities` - Black and Hispanic patients experienced delays
- `language-barriers` - Non-English speakers experienced longer delays
- `bias-detection` - Identifies systemic inequities in care delivery
- `clinical-workflow-implications` - Suggests incorporating demographic risk profiles
- `future-ai-decision-support` - Notes potential for AI tools to address disparities
- `no-current-ai-intervention` - Descriptive study, no AI tool deployed yet
- `quantifying-inequity` - Provides specific delay times (8-28 minutes)

---

## 4. Bayes Anatomy (Menstrual Cycle Physiotypes for LLM Personalization)

**Project Summary:** Derives menstrual physiotypes from mcPHASES data and tests whether they meaningfully shift LLM health recommendations.

**Initial Codes:**
- `personalization-via-physiotypes` - Clusters users into physiologic profiles
- `llm-behavior-modulation` - Tests if LLM outputs change based on persona
- `womens-health-focus` - Menstrual cycle tracking
- `wearable-integration` - Fitbit, CGM, hormone data
- `proof-of-concept` - Demonstrates feasibility, not deployment
- `multimodal-data-integration` - Combines physiological signals, hormones, symptoms
- `physiology-aware-ai` - Goal is biologically-grounded personalization
- `limitations-acknowledged` - Notes cluster imbalance, missing data issues

---

## 5. Brachioplexusosaurus / Axia (Diabetes Complication Prediction App)

**Project Summary:** Patient-facing app predicting diabetic complications (neuropathy, nephropathy, retinopathy, CVD) using XGBoost, with risk radar dashboard and gamification.

**Initial Codes:**
- `complication-risk-prediction` - Predicts four major diabetes complications
- `patient-facing-app` - Designed for patient use
- `risk-visualization` - Color-coded "risk radar" dashboard
- `gamification` - Engagement through game elements
- `caregiver-integration` - Supports caregiver access
- `patient-education-links` - Embedded links to ADA resources
- `device-interoperability` - Apple Watch, CGM integration
- `clinician-report-generation` - PDF summaries for office visits
- `variable-model-performance` - Strong for CVD/nephropathy, weak for neuropathy/retinopathy
- `stakeholder-validation` - Interviewed patients, caregivers, clinicians
- `shared-decision-making` - Aims to support patient-clinician dialogue
- `interpretability-shap` - Uses SHAP for feature refinement

---

## 6. Brunologix (Emotion-Aware Medical Interpreter)

**Project Summary:** Real-time speech-to-speech interpreter with emotion detection for multilingual ED communication, paired with MIMIC analysis of language-based utilization disparities.

**Initial Codes:**
- `language-access` - Addresses LEP patient needs
- `health-equity-analysis` - Shows Spanish speakers have higher utilization
- `emotion-preservation` - Maintains emotional nuance in translation
- `real-time-tool` - Live interpretation capability
- `multimodal-ai` - Speech recognition, translation, emotion detection, TTS
- `trust-building` - Emotional tone important for clinical trust
- `ed-focus` - Emergency department context
- `prototype-demonstration` - Functional prototype with demo video
- `disparity-quantification` - Documents utilization differences

---

## 7. ChickensOfOxford / CLaRA (Clinical Literacy and Results Assistant)

**Project Summary:** System providing patients with medical record explanations at chosen reading levels, using source-restricted LLM queries to trusted medical sources.

**Initial Codes:**
- `health-literacy-enhancement` - Core mission to improve understanding
- `reading-level-customization` - Users choose explanation complexity
- `source-restriction` - Only queries trusted sources (Cleveland Clinic, PubMed, etc.)
- `hallucination-mitigation` - Addresses LLM hallucination concerns
- `citation-provision` - Outputs include citations
- `medication-visualization` - Pill images for identification
- `lab-result-contextualization` - Explains labs in patient-specific context
- `interactive-timeline` - Patient journey visualization
- `patient-empowerment` - Helps patients understand their care
- `privacy-considerations` - Plans for dual-model architecture for privacy
- `llm-safety-design` - Explicitly addresses LLM risks

---

## 8. CodeDependencies (Post-AMI Mortality Prediction)

**Project Summary:** ML models predicting 30/90-day mortality after AMI using first 24 hours of ICU lab data, with high-recall screening focus.

**Initial Codes:**
- `mortality-prediction` - Predicts 30 and 90-day death
- `early-warning-system` - First 24 hours of data only
- `interpretability-shap` - SHAP and permutation importance
- `high-recall-prioritization` - 93% recall model for screening
- `lab-based-features` - Uses routine laboratory data
- `immune-inflammatory-markers` - SIRI and inflammatory predictors
- `ehr-integration-potential` - Envisions automated alerts
- `patient-family-communication` - Aims to make prognosis understandable
- `value-based-care-alignment` - Mentions readmission penalties, resource optimization
- `bias-limitation-acknowledged` - Notes potential gender bias in dataset

---

## 9. Curanostics (Discharge Summary Simplification)

**Project Summary:** Medical LLM transforms discharge summaries to sixth-grade reading level, evaluated with readability metrics.

**Initial Codes:**
- `health-literacy-enhancement` - Improves readability of discharge summaries
- `reading-level-targeting` - Aims for sixth-grade level
- `llm-medical-specialized` - Uses JSL-MedLlama-3-8B-v2.0
- `readability-metrics` - Flesch Reading Ease, Gunning Fog Index
- `care-transitions` - Focus on discharge communication
- `model-refusal-documented` - 10/30 summaries refused by model
- `quantitative-improvement` - +17.8 points Flesch, -4.7 grade levels
- `comprehension-not-validated` - Notes readability ≠ understanding
- `future-validation-needed` - Calls for patient comprehension testing

---

## 10. DA-Med-plus (Tele-AI Diabetes for Rural Africa)

**Project Summary:** Low-bandwidth chatbot for diabetes risk assessment in rural Kenya/Nigeria, using logistic regression on non-laboratory features.

**Initial Codes:**
- `low-resource-setting-design` - Targets rural African communities
- `no-laboratory-requirement` - Uses only self-reported data
- `low-bandwidth-compatibility` - Web-based, accessible
- `chatbot-interface` - Gradio-based conversational tool
- `global-health-equity` - Addresses diagnostic access gaps
- `lifestyle-guidance` - Provides personalized recommendations
- `screening-referral` - Directs high-risk users to testing
- `scalability-emphasis` - Designed for population-level deployment
- `external-validation-needed` - Dataset not region-specific
- `digital-literacy-limitation` - Acknowledges access barriers

---

## 11. DeepDishLearning (PMDD Early Detection)

**Project Summary:** Mixed-effects regression linking wearable physiological signals to premenstrual symptoms for PMDD screening, with proposed patient dashboard.

**Initial Codes:**
- `pmdd-screening` - Early PMDD detection focus
- `wearable-physiological-signals` - HR, temperature, sleep, glucose
- `symptom-correlation-analysis` - Links physiology to symptoms
- `patient-dashboard-proposed` - Visualization for patients
- `menstrual-phase-association` - Examines phase-specific patterns
- `prospective-tracking-value` - Improves on retrospective reporting
- `patient-clinician-dialogue` - Aims to guide discussions
- `pilot-rct-referenced` - Cites evidence for app-based tracking benefits

---

## 12. FulldataScientists (Menstrual Cycle Hormone Prediction)

**Project Summary:** Tree-based models predicting hormone levels (LH, estrogen, PdG) from wearable data for non-invasive ovulation tracking.

**Initial Codes:**
- `hormone-prediction` - Predicts LH, estrogen, PdG levels
- `non-invasive-monitoring` - Alternative to urinary LH kits
- `fertility-support` - Aims to help conception
- `wearable-derived-features` - Sleep, temperature, activity
- `cost-barrier-addressed` - LH kits are expensive
- `accessibility-improvement` - Reduces testing burden
- `irregular-cycle-consideration` - Notes need for validation in PCOS
- `patient-empowerment` - Empowers fertility monitoring

---

## 13. Ghanta-Branscom (Metabolic Health & Menstrual Cycle)

**Project Summary:** XGBoost predicting insulin resistance proxies with menstrual phase integration, demonstrating phase-specific models outperform phase-agnostic ones.

**Initial Codes:**
- `metabolic-health-focus` - Insulin resistance prediction
- `menstrual-phase-integration` - Phase improves model performance
- `personalization-biological-rhythm` - Aligns AI with hormonal cycles
- `wearable-cgm-integration` - Fitbit and glucose monitoring
- `chatbot-planned` - Conversational interface for insights
- `health-equity-womens-health` - Notes women underserved by generic tools
- `limited-generalizability-noted` - Small sample, specific subgroups underperform
- `preventive-care-support` - Early metabolic dysfunction detection

---

## 14. KPopDataHunters (Mental Health Trajectory Forecasting)

**Project Summary:** DTW-RAG framework combining retrieval-augmented generation with dynamic time warping to forecast anxiety/depression severity.

**Initial Codes:**
- `mental-health-forecasting` - Predicts anxiety/depression trajectories
- `rag-framework` - Retrieval-augmented generation
- `temporal-pattern-matching` - Dynamic time warping for similar sequences
- `llm-grounded-prediction` - LLM synthesis adds value beyond retrieval
- `interpretability-through-retrieval` - Retrieved cases justify predictions
- `open-source-llm-evaluation` - Compares multiple open-source models
- `personalized-care-support` - Aims for individualized mental health management
- `modest-improvement-documented` - 1.5-5.7% improvement over baseline
- `transparent-evaluation` - Compares across architectures

---

## 15. Neuron&Co / SynClari (Women's Cognitive Health)

**Project Summary:** Multi-output neural network predicting PMDD-related symptoms from physiological data for cognitive fatigue forecasting in women.

**Initial Codes:**
- `cognitive-fatigue-prediction` - Forecasts daily cognitive load states
- `pmdd-pattern-detection` - Identifies PMDD-like symptom escalation
- `womens-health-equity` - Notes women disproportionately affected
- `wearable-derived-prediction` - HR, temperature, sleep patterns
- `personalized-embeddings` - Individualized user modeling
- `performance-optimization-goal` - Aims to help women align decisions with biology
- `cycle-phase-clustering` - PCA shows phase-linked symptom structure
- `future-wearable-vision` - Envisions dedicated device

---

## 16. NobelEdge (Fibromyalgia Weather-Linked Flares)

**Project Summary:** Logistic regression analyzing weather factors (humidity, temperature) predicting fibromyalgia flare days.

**Initial Codes:**
- `chronic-pain-management` - Fibromyalgia focus
- `environmental-trigger-analysis` - Weather as predictor
- `patient-reported-data` - Uses Flaredown symptom logs
- `individual-variability-noted` - Weather sensitivity varies by person
- `psychological-moderators` - Stress/anxiety influence weather-symptom link
- `quality-of-life-impact` - Weather sensitivity linked to worse QoL
- `explainable-findings` - Clear humidity-flare relationship
- `patient-validation` - Aligns with patient self-reports of triggers

---

## 17. NöroNest (Type 2 Diabetes Prediction from BRFSS)

**Project Summary:** Comparison of ML classifiers predicting T2DM from population survey data, identifying age and BMI as top predictors.

**Initial Codes:**
- `population-screening` - BRFSS population-level data
- `model-comparison` - Tests 5 classifier types
- `screening-triage-framing` - Explicitly positions as triage aid, not diagnostic
- `modest-sensitivity-acknowledged` - ~39% recall across models
- `feature-importance-analysis` - Age, BMI, health burden as predictors
- `clinical-utility-limitations` - Notes survey features alone insufficient
- `future-validation-called` - Requests external validation, calibration
- `harm-consideration` - Mentions false negatives/positives before deployment

---

## 18. Pythons (ED Return Visit Prediction & Discharge Education)

**Project Summary:** Logistic regression/XGBoost predicting 30-day ED returns, with diagnosis clustering to inform digital discharge education tool design.

**Initial Codes:**
- `readmission-prediction` - 30-day ED return
- `care-transitions` - Discharge as vulnerable period
- `patient-education-tool` - Digital discharge education planned
- `diagnosis-clustering` - NLP groups conditions for content design
- `health-literacy-tailored` - Literacy-appropriate materials
- `vulnerable-populations` - Notes varied insurance, literacy, access
- `model-refinement-ongoing` - Acknowledges current modest performance
- `ehr-integration-vision` - Future EHR embedding

---

## 19. RxGuardian (Medication Interaction Detection)

**Project Summary:** Timing-aware drug-drug interaction detection using Beers Criteria, with risk model prioritizing high-risk discharges for pharmacist review.

**Initial Codes:**
- `medication-safety` - DDI detection focus
- `timing-aware-detection` - Only flags when administration overlaps
- `alert-fatigue-mitigation` - Reduces noise from non-overlapping meds
- `beers-criteria-alignment` - Evidence-based interaction rules
- `pharmacist-workflow-support` - Helps prioritize review
- `polypharmacy-risk` - Main predictor is number of drugs
- `threshold-tuning` - Allows precision-recall tradeoff adjustment
- `interpretable-model` - Logistic regression chosen for transparency
- `discharge-safety-focus` - Post-discharge medication reconciliation
- `older-adult-focus` - Beers Criteria for ≥65 years

---

## 20. SSOM1 / CareBridge (Adaptive Discharge Summaries)

**Project Summary:** LLM-driven system converting discharge summaries to tiered literacy levels (basic/intermediate/advanced) with safety constraints.

**Initial Codes:**
- `health-literacy-enhancement` - Multi-tier readability
- `llm-safety-constraints` - Source verification, structured output
- `care-transitions` - Discharge summary transformation
- `patient-selectable-complexity` - Users choose literacy level
- `actionable-next-steps` - Tracks patient tasks
- `factuality-evaluation` - NLI entailment scoring
- `relevance-evaluation` - BERT F1 scoring
- `prototype-interface` - UI for patient interaction
- `language-complexity-alignment` - Evaluates output matches target level
- `future-ehr-integration` - Planned EHR embedding

---

## 21. SSOM2 (Menstrual Symptom Forecasting)

**Project Summary:** Comprehensive ML pipeline predicting 7 menstrual symptoms from wearables and hormones, achieving good-to-excellent AUC across symptoms.

**Initial Codes:**
- `symptom-forecasting` - Day-level prediction of 7 symptoms
- `wearable-hormone-integration` - Fitbit + hormone assays
- `temporal-feature-engineering` - Lag features, rolling averages, deltas
- `multiple-model-comparison` - RF, Gradient Boosting, Logistic Regression
- `strong-performance` - AUC 0.66-0.83 across symptoms
- `clinical-utility-framing` - Anticipatory intervention support
- `feature-importance-documented` - Sleep and hormones dominate
- `patient-facing-vision` - Future integration with wearables
- `personalization-need` - Notes individual variation
- `limitations-documented` - Sample size, no birth control users
- `productivity-impact-cited` - References menstrual-related work loss

---

## 22. Staphylococcus Aura / TLDR (Lab Result Translation)

**Project Summary:** Gemini 2.5 Pro generates patient-centered summaries of lab results at basic/advanced reading levels.

**Initial Codes:**
- `health-literacy-enhancement` - Lab report simplification
- `reading-level-customization` - Basic (6th grade) and advanced options
- `llm-gemini` - Uses Gemini 2.5 Pro
- `patient-clinician-dual-use` - Both can use appropriate level
- `context-aware-summaries` - Incorporates diagnoses, demographics
- `treatment-adherence-goal` - Links literacy to adherence
- `prototype-website` - Functional web application
- `readability-validation` - Flesch scores confirm target levels
- `bias-limitation-noted` - Acknowledges LLM biases
- `standardization-requirement` - Needs consistent input data

---

## 23. StarPeak (Menstrual Cycle Sensitivity Phenotypes)

**Project Summary:** Clusters individuals by physiological variability across menstrual phases, identifying distinct sensitivity phenotypes.

**Initial Codes:**
- `personalization-phenotyping` - Clusters into sensitivity groups
- `individual-variability-focus` - Moves beyond population averages
- `wearable-physiological-data` - HRV, temperature, stress, RHR
- `phase-specific-patterns` - Examines within-cycle dynamics
- `sleep-symptom-correlation` - Sleep score inversely related to symptoms
- `consumer-app-potential` - Envisions patient-facing application
- `targeted-intervention-testing` - Suggests testing if interventions differ by group
- `menstrual-health-literacy` - Aims to improve patient understanding

---

## 24. TeamMidBest (ICU Pressure Injury & Comorbidity)

**Project Summary:** Retrospective analysis linking Elixhauser comorbidity scores to ICU-acquired pressure injuries.

**Initial Codes:**
- `risk-stratification` - Identifies high-risk patients
- `comorbidity-integration` - Elixhauser index as predictor
- `pressure-injury-prevention` - Hospital-acquired condition focus
- `multimorbidity-vulnerability` - Complex chronic disease profiles
- `descriptive-analysis` - No predictive model deployed
- `prevention-strategy-implications` - Suggests incorporating comorbidity assessment
- `real-time-integration-proposed` - Future physiologic + comorbidity data fusion
- `icu-focus` - Intensive care setting

---

## 25. TheWashingtonPost (Posture as Clinical Marker)

**Project Summary:** NLP extraction of postural descriptors from MIMIC discharge notes, exploring posture as prognostic factor.

**Initial Codes:**
- `novel-biomarker-exploration` - Posture as unquantified marker
- `nlp-extraction` - Extracts posture terms from notes
- `limited-documentation-finding` - Clinical notes rarely capture posture
- `modest-predictive-value` - Posture features contribute ~25% importance
- `proof-of-concept` - Demonstrates feasibility of approach
- `future-wearable-integration` - Suggests sensors for posture data
- `data-limitation-acknowledged` - ICU population limits generalizability

---

## 26. Therayes (Emergency Orthopedic Surgery Outcomes)

**Project Summary:** ML models predicting adverse outcomes (mortality, readmission, prolonged stay) after non-elective orthopedic surgery.

**Initial Codes:**
- `adverse-outcome-prediction` - 90-day mortality, readmission, LOS
- `emergency-surgery-focus` - Non-elective procedures
- `clinical-complexity-capture` - Comorbidities, procedural complexity
- `early-readmission-sentinel` - Readmission predicts mortality
- `opioid-burden-predictor` - Medication use as risk factor
- `targeted-surveillance-support` - Identifies patients needing monitoring
- `interpretability-shap` - SHAP for feature importance
- `logistic-regression-chosen` - Best performing, interpretable model

---

## 27. Trifusion (In-Hospital Mortality Risk Tool)

**Project Summary:** Comprehensive mortality risk scoring using ICD-10 codes and ML, achieving very high AUROC (0.98).

**Initial Codes:**
- `mortality-prediction` - In-hospital death prediction
- `high-model-performance` - AUROC 0.9846
- `diagnosis-code-based` - Uses billing and ICD-10 codes
- `iterative-refinement` - Progressive model improvement
- `synergy-incorporation` - Considers diagnosis combinations
- `patient-empowerment-framing` - Patients understand severity
- `clinical-decision-support` - Provider tool
- `age-subgroup-consistency` - Performance stable across ages

---

## 28. Aforeffort (Menstrual Health Index)

**Project Summary:** Creates composite Menstrual Health Index integrating hormones, physiology, and symptoms into 0-100 daily score.

**Initial Codes:**
- `composite-health-metric` - Single interpretable index
- `multimodal-integration` - Hormones, wearables, symptoms
- `quantitative-menstrual-tool` - Addresses lack of clinical metrics
- `individual-monitoring-value` - Personalized longitudinal tracking
- `physiologic-stability-measure` - Higher score = more stability
- `patient-transparency-goal` - Increase understanding of health status
- `health-literacy-menstrual` - Entry point to menstrual education
- `small-cohort-limitation` - 42 participants, homogeneous

---

## 29. NeurOnCDoc (Chronic Disease Flare Forecasting)

**Project Summary:** Calibrated LightGBM models for next-day inflammatory arthritis and epilepsy flare prediction with patient-friendly explanations.

**Initial Codes:**
- `flare-forecasting` - Next-day risk prediction
- `calibrated-predictions` - Isotonic calibration for reliable probabilities
- `multi-condition-application` - IA and epilepsy
- `patient-journal-based` - Uses patient-entered symptom logs
- `llm-explanation-generation` - Converts SHAP to plain language
- `interpretability-shap` - Top attributions drive explanations
- `patient-facing-interface` - Journaling app prototype
- `actionable-thresholds` - Risk levels support decision-making
- `self-management-support` - Pacing, self-care guidance
- `shared-decision-making` - Supports patient-clinician dialogue
- `strong-discrimination` - AUROC 0.80-0.91

---

## 30. GoldenGateGPTs (Radiology Report Translation)

**Project Summary:** LLM transforms chest X-ray reports for patient readability, with automated evaluation framework (clinical accuracy, readability, semantic similarity).

**Initial Codes:**
- `radiology-report-simplification` - Chest X-ray reports
- `patient-empowerment` - Counters anxiety from unclear results
- `21st-century-cures-context` - References patient access regulations
- `multi-metric-evaluation` - Clinical accuracy, Flesch-Kincaid, BERTScore
- `variable-performance` - Composite scores 2-4/5, high variability
- `clinical-accuracy-challenge` - Main source of score variation
- `prompt-engineering` - Zero-shot vs one-shot comparison
- `llm-comparison` - Llama 3.1 vs GPT OSS
- `limitations-acknowledged` - Small sample, single center, no manual validation

---

## 31. HeartRead (HF Readmission with SDOH)

**Project Summary:** ML model predicting 30-day heart failure readmission integrating clinical data with NLP-extracted social determinants of health.

**Initial Codes:**
- `readmission-prediction` - 30-day HF readmission
- `sdoh-integration` - Social determinants extracted via NLP
- `health-equity-analysis` - Disparities by race, language, insurance
- `nlp-sdoh-extraction` - Rule-based extraction from notes
- `documentation-gap-identified` - SDOH poorly documented in EHR
- `modest-model-performance` - AUROC 0.647
- `discharge-planning-support` - Equitable discharge planning goal
- `mental-health-sdoh-predictor` - Mental health SDOH independently associated
- `medicaid-predictor` - Insurance type predicts readmission
- `structured-documentation-need` - Calls for better SDOH capture

---

## Initial Code Inventory

Based on the systematic coding above, here is a preliminary inventory of all codes generated:

### Patient-Centered Design & Empowerment
- `patient-empowerment` (11 occurrences)
- `patient-facing-app` / `patient-facing-interface` (8)
- `self-management-support` (5)
- `shared-decision-making` (3)
- `health-literacy-enhancement` (6)
- `reading-level-customization` (4)
- `patient-education-tool` (3)
- `patient-selectable-complexity` (2)
- `actionable-next-steps` (2)

### Interpretability & Explainability
- `interpretability-shap` (8)
- `llm-explanation-generation` (3)
- `patient-facing-explanations` (3)
- `interpretable-model` (2)
- `feature-importance-analysis` (4)
- `explainable-findings` (2)

### Risk Prediction & Stratification
- `risk-stratification` (4)
- `mortality-prediction` (3)
- `readmission-prediction` (3)
- `symptom-forecasting` (4)
- `flare-forecasting` (2)
- `complication-risk-prediction` (2)
- `early-warning-system` (2)
- `screening-triage-framing` (2)

### Health Equity & Access
- `health-equity-analysis` (4)
- `racial-ethnic-disparities` (2)
- `language-barriers` / `language-access` (3)
- `low-resource-setting-design` (1)
- `global-health-equity` (1)
- `sdoh-integration` (2)
- `womens-health-equity` (2)
- `bias-detection` (1)

### Care Transitions & Safety
- `care-transitions` (4)
- `medication-safety` (1)
- `alert-fatigue-mitigation` (1)
- `discharge-safety-focus` (2)
- `ehr-integration` / `ehr-integration-potential` (5)
- `clinical-workflow-implications` (2)

### LLM Safety & Design
- `llm-safety-constraints` (2)
- `hallucination-mitigation` (1)
- `source-restriction` (1)
- `citation-provision` (1)
- `factuality-evaluation` (1)
- `model-refusal-documented` (1)

### Model Performance & Limitations
- `modest-performance-acknowledged` (4)
- `strong-performance` (3)
- `variable-model-performance` (3)
- `limitations-acknowledged` / `limitations-documented` (8)
- `future-validation-needed` (4)
- `bias-limitation-acknowledged` (3)
- `small-cohort-limitation` (2)
- `external-validation-needed` (2)

### Data & Methods
- `wearable-integration` / `wearable-derived-features` (9)
- `multimodal-data-integration` (4)
- `nlp-extraction` (2)
- `temporal-feature-engineering` (2)
- `calibrated-predictions` (1)
- `patient-reported-data` (2)
- `patient-journal-based` (2)

### Clinical Domains
- `chronic-disease-management` (3)
- `mental-health-focus` (3)
- `womens-health-focus` / `menstrual-phase-integration` (10)
- `diabetes-focus` (3)
- `cardiovascular-focus` (2)
- `emergency-department-focus` (2)

### Proof-of-Concept & Future Vision
- `proof-of-concept` (4)
- `prototype-demonstration` (4)
- `future-patient-tool` (3)
- `scalability-emphasis` (1)
- `consumer-app-potential` (2)

---

## Notes for Theme Development

Several potential themes are emerging:

1. **Patient Empowerment Through Transparency** - Many projects aim to make health information accessible and understandable

2. **Interpretability as Safety** - SHAP, plain-language explanations, and source citations as safety mechanisms

3. **Addressing Health Inequities** - Language, race/ethnicity, geography, and gender-based disparities

4. **Bridging Clinical and Patient Worlds** - Care transitions, discharge communication, dual-use tools

5. **Chronic Disease Self-Management** - Symptom prediction, trigger identification, proactive planning

6. **Appropriate Epistemic Humility** - Acknowledging limitations, calling for validation, framing as screening vs diagnosis

7. **Women's Health Innovation** - Notable cluster of menstrual/reproductive health projects

8. **LLM-Specific Safety Considerations** - Hallucination mitigation, source restriction, factuality checking

---

*Document prepared for review before proceeding to Phase 3 (Theme Development)*
