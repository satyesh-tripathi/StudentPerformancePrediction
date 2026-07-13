# PROJECT.md — Student Performance Prediction System
**AIML Summer Internship 2026 — IIHMF, MNNIT Allahabad, Prayagraj**
**Project 1 of 4 (Capstone)**
**Status:** Planning Complete — Awaiting Build Approval
**Last Updated:** 2026-07-12 (Plan v1.0)

---

## 1. Project Overview

The Student Performance Prediction System is a regression-based Machine Learning
application that predicts a student's academic performance (a continuous score,
e.g., final exam marks / GPA-equivalent) using academic and behavioral indicators
such as attendance, assignment scores, internal assessment marks, prior academic
performance, and study hours.

This is being built to the standard of a **client-delivered software product**, not
a one-off assignment — with full lifecycle documentation, reproducible pipelines,
a deployed interactive app, a formal report, and a presentation deck.

## 2. Problem Statement

Educational institutions need an early-warning, data-driven way to estimate how a
student will perform, using indicators available *before* final results are out
(attendance, internals, assignments, study habits). Manual estimation by faculty
is subjective and doesn't scale. A predictive system lets institutions intervene
early for at-risk students.

## 3. Objectives

1. Build a clean, leakage-free regression pipeline that predicts a student
   performance score/grade from academic + behavioral features.
2. Compare ≥3 regression algorithms (mandatory) and select the best via
   cross-validated metrics — plan targets up to 6–7 models for a portfolio-grade
   comparison (Linear, Ridge, Lasso, Decision Tree, Random Forest, Gradient
   Boosting, XGBoost — LightGBM/CatBoost only if dataset size justifies it).
3. Deliver an interactive Streamlit app that accepts real student inputs and
   returns a prediction with interpretation.
4. Produce a 15–25 page report and a 10–15 slide deck matching the PDF's exact
   required structure.
5. Maintain complete engineering documentation (this file + task.md +
   decision.md + issues.md) throughout, not written retroactively.

## 4. Success Criteria

- [ ] All 8 phases in the guideline PDF are demonstrably completed.
- [ ] Folder structure matches the mandated structure exactly (Section 9).
- [ ] ≥3 models trained, compared, and justified with metrics (MAE/MSE/RMSE/R²).
- [ ] Final model + scaler/encoder pipeline saved and loaded successfully in the app.
- [ ] Streamlit app runs end-to-end with input validation and no crashes on edge cases.
- [ ] Report is 15–25 pages, follows the 6-chapter structure exactly.
- [ ] PPT is 10–15 slides, follows the suggested 12-point structure.
- [ ] Every engineering decision and every bug encountered is logged.
- [ ] Final zip follows `ProjectName_TeamLeaderName.zip` naming convention.

## 5. Functional Requirements

| ID | Requirement |
|----|-------------|
| FR-1 | System shall ingest a structured dataset with student academic/behavioral features |
| FR-2 | System shall clean data (missing values, duplicates, outliers, encoding, scaling) |
| FR-3 | System shall perform EDA (univariate, bivariate, correlation, target distribution) |
| FR-4 | System shall engineer and select features |
| FR-5 | System shall train and compare ≥3 regression models |
| FR-6 | System shall tune hyperparameters via GridSearch/RandomizedSearch + CV |
| FR-7 | System shall evaluate models on MAE, MSE, RMSE, R², and residual analysis |
| FR-8 | System shall persist the best model + preprocessing pipeline (joblib/pickle) |
| FR-9 | System shall expose a Streamlit UI accepting all input features with validation |
| FR-10 | System shall return a predicted performance value + human-readable interpretation |
| FR-11 | System shall handle invalid/edge-case inputs gracefully (no crash, clear message) |

## 6. Non-Functional Requirements

- **Reproducibility:** fixed random seeds, requirements.txt, documented environment.
- **Code quality:** PEP-8, modular functions, no notebook-only "spaghetti" logic in
  the final pipeline (notebook is for exploration; production code is scripted).
- **Portfolio quality:** clean README, clear commit-worthy folder structure, docs
  written for a stranger (e.g., a recruiter or future teammate) to understand.
- **Performance:** app prediction latency should be near-instant (<1s) since model
  is a lightweight tabular regressor.
- **Maintainability:** config-driven (feature list, paths) rather than hardcoded
  magic values scattered across files.

## 7. Machine Learning Pipeline (High Level)

```
Raw Dataset (CSV)
   → Data Cleaning (missing values, duplicates, outliers, dtype fixes)
   → Encoding (categorical → numeric) + Scaling (numeric features)
   → EDA (univariate / bivariate / correlation / target distribution)
   → Feature Engineering & Selection
   → Train/Test Split (stratify on binned target if useful)
   → Model Training (7 candidate regressors)
   → Hyperparameter Tuning (GridSearchCV / RandomizedSearchCV, k-fold CV)
   → Model Evaluation & Comparison (MAE, MSE, RMSE, R², residuals)
   → Best Model Selection + Justification
   → Persist Model + Scaler + Encoder + Feature List (joblib)
   → Streamlit App (loads pipeline, takes input, predicts, displays result)
```

## 8. Technology Stack

| Layer | Choice | Notes |
|---|---|---|
| Language | Python 3.11 | stable, wide library support |
| Env mgmt | `venv` | lightweight, no extra tooling needed |
| Data handling | pandas, numpy | standard |
| Visualization | matplotlib, seaborn | required chart types (histograms, boxplots, scatter, heatmaps) |
| ML | scikit-learn | Linear/Ridge/Lasso/DecisionTree/RandomForest/GradientBoosting |
| Boosting | xgboost | mandatory-adjacent per PDF; LightGBM/CatBoost added only if dataset is large/categorical-heavy enough to justify |
| Tuning | scikit-learn GridSearchCV / RandomizedSearchCV | with k-fold CV |
| Model persistence | joblib | model + scaler + encoder + metadata |
| Deployment | Streamlit | per PDF preference over Flask |
| Version control | git (local; user can push to GitHub) | |

**Python Version:** 3.11 (any 3.10+ is fine; will pin exact version in `requirements.txt`)

## 9. Folder Structure (Mandated by PDF — must match exactly)

```
StudentPerformancePrediction_<TeamLeaderName>/
│
├── Dataset/                # raw + cleaned data
├── Notebook/                # exploration, EDA, experimentation notebooks
├── Model/                   # saved model, scaler, encoder (joblib files)
├── Streamlit_App/           # app.py + supporting modules
├── Documentation/           # project.md, task.md, decision.md, issues.md, report, ppt
└── README.md
```

Internally, `Streamlit_App/` and a `src/` (or `pipeline/`) area will hold modular
scripts (`data_cleaning.py`, `feature_engineering.py`, `train_models.py`,
`evaluate.py`, `predict.py`) so the Streamlit app just imports functions rather
than duplicating logic — this is an *implied* requirement (professional code
reuse) not explicitly named in the PDF but necessary to satisfy "clean, modular,
production-quality" coding rules.

## 10. Architecture

- **Batch/offline layer:** Jupyter notebooks + scripts for EDA, training, tuning —
  produces the persisted model artifact.
- **Serving layer:** Streamlit app loads the persisted artifact once (cached),
  accepts form inputs, runs the same preprocessing pipeline used in training,
  and returns a prediction.
- **No database/API layer needed** — scope is a single-model batch-trained,
  form-input inference app, consistent with PDF's deployment ask.

## 11. Timeline (Suggested — Adjustable)

| Phase | Deliverable | Est. Effort |
|---|---|---|
| 1. Problem Understanding | This document | 0.5 day |
| 2. Dataset Sourcing | Dataset chosen + justified | 0.5–1 day |
| 3. Dataset Understanding | Data profiling notebook | 0.5 day |
| 4. Data Cleaning | Clean dataset + cleaning script | 1 day |
| 5. EDA | EDA notebook + insights | 1–1.5 days |
| 6. Feature Engineering | Feature set + rationale | 1 day |
| 7. Model Development | 7 trained models | 1–1.5 days |
| 8. Hyperparameter Tuning | Tuned best 2–3 models | 1 day |
| 9. Model Evaluation | Comparison table + chosen model | 0.5 day |
| 10. Model Saving | Persisted artifacts | 0.5 day |
| 11. Deployment | Working Streamlit app | 1–1.5 days |
| 12. Testing | Edge case test log | 0.5 day |
| 13. Documentation | Continuous (parallel to all phases) | ongoing |
| 14. Report | 15–25 page report | 1.5–2 days |
| 15. Presentation | 10–15 slide deck | 0.5–1 day |

Total: roughly **10–14 working days** at a careful, portfolio-grade pace.

## 12. Deliverables Checklist

- [ ] Source Code (.zip) in mandated folder structure
- [ ] Cleaned + raw dataset in `Dataset/`
- [ ] Jupyter notebook(s) in `Notebook/`
- [ ] Saved model + scaler + encoder in `Model/`
- [ ] Streamlit app in `Streamlit_App/`
- [ ] Project Report (PDF, 15–25 pages, 6 chapters + references)
- [ ] Presentation (PPT/PDF, 10–15 slides)
- [ ] README.md
- [ ] Deployment link (if hosted, e.g. Streamlit Community Cloud)
- [ ] project.md / task.md / decision.md / issues.md (this documentation set)

## 13. Deployment Plan

- Primary: local Streamlit app (`streamlit run app.py`), always demoable offline
  for the live demo requirement.
- Stretch (optional, recommended for portfolio): deploy to **Streamlit Community
  Cloud** (free) so the "Deployment Link" field in submission guidelines is
  filled with a real public URL. Will flag this as optional-but-recommended.

## 14. Report Plan (maps directly to PDF's required chapters)

1. **Introduction** — Background, Problem Statement, Objectives
2. **Literature Review** — existing academic-performance-prediction approaches,
   brief survey of 4–6 relevant studies/methods
3. **Methodology** — Dataset Description, Preprocessing, Algorithms Used
4. **Implementation** — EDA, Feature Engineering, Model Development (with figures)
5. **Results and Discussion** — metrics table, comparative analysis, best model
6. **Conclusion and Future Scope**
7. **References**

Target: 15–25 pages, will draft in Markdown → convert to Word/PDF at Phase 13–14
using the docx skill for professional formatting (headings, ToC, page numbers).

## 15. PPT Plan (maps directly to PDF's suggested structure, 10–15 slides)

1. Title
2. Problem Statement
3. Objectives
4. Dataset Description
5. Methodology
6. Data Preprocessing
7. EDA (key charts)
8. Models Used
9. Results (comparison table + best model highlight)
10. Demo Screenshots
11. Conclusion
12. Future Scope

Built with the pptx skill at Phase 15.

## 16. Future Scope (draft — refine after results are in)

- Extend to classification (pass/fail or grade-band prediction) as a companion model.
- Add explainability (SHAP) for per-student interpretation.
- Incorporate longitudinal/time-series attendance trends instead of a single
  aggregate attendance %.
- Deploy with a lightweight database for institutions to log predictions over time.

## 17. Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| No single "official" dataset named in PDF for Project 1 | High | Medium | Compare 2–3 candidate Kaggle datasets, document choice in decision.md |
| Data leakage (e.g., using a feature that encodes the target) | Medium | High | Explicit leakage review before modeling; documented in decision.md |
| Overfitting with boosting models on small dataset | Medium | Medium | Cross-validation, regularization, learning curves |
| Streamlit deployment/environment issues | Low–Medium | Medium | Pin versions in requirements.txt; test in clean venv |
| Report/PPT drifting from PDF's exact structure | Low | High (grading risk) | Structure locked to PDF verbatim in Sections 14–15 above |
| Scope creep (adding unrequired complexity) | Medium | Low–Medium | Every addition logged with justification in decision.md |

## 18. Dataset Details — CONFIRMED (D-005, D-006)

**Source:** UCI Student Performance Dataset (Cortez & Silva, 2008), Math course
only — `student-mat.csv`, 395 rows, 33 columns, 0 missing values, 0 duplicates.

**Target:** `G3` (final grade, 0–20 scale) — continuous, suitable for
regression per PDF requirement.

**Feature set (30 columns, `G1`/`G2` deliberately excluded per D-006):**
- *Numeric (13):* age, Medu, Fedu, traveltime, studytime, failures, famrel,
  freetime, goout, Dalc, Walc, health, absences — several are ordinal-coded
  (e.g., studytime 1–4, Medu/Fedu 0–4, famrel/freetime/goout/Dalc/Walc/health 1–5)
- *Categorical (17):* school, sex, address, famsize, Pstatus, Mjob, Fjob,
  reason, guardian, schoolsup, famsup, paid, activities, nursery, higher,
  internet, romantic — mostly binary yes/no, a few nominal (Mjob, Fjob, reason,
  guardian)

**Mapping to PDF's required indicator types:**
| PDF asks for | Mapped to |
|---|---|
| Attendance | `absences` (inverse proxy — higher = more absent) |
| Study Hours | `studytime` (banded 1–4, not raw hours) |
| Assignment Scores / Internal Assessment | *not present as a standalone column — deliberately excluded (G1/G2 would have served this role but were dropped per D-006)* |
| Previous Academic Performance | *same — G1/G2 excluded per D-006* |
| Other meaningful academic indicators | failures, Medu/Fedu (parental education), school support, family support, romantic status, going out, alcohol consumption, health, etc. |

**Known data characteristics (from Phase 3 profiling):**
- Clean: no missing values, no duplicate rows.
- `absences`: right-skewed, max 75, 15/395 students with >20 absences — flagged
  for outlier treatment in Phase 4 (ISS-001).
- `G3` = 0 for 38/395 students (9.6%) — per source documentation this
  typically means the student did not sit the exam, not a data error
  (ISS-002) — will be visualized/handled distinctly, not silently dropped.
- Correlation with `G3` (excluding G1/G2): strongest is `failures` (r = -0.36),
  followed by `Medu` (0.22), `Fedu` (0.15), `studytime` (0.10) — materially
  weaker than G1/G2 would have been (0.80–0.90), which is the expected and
  accepted consequence of the D-006 framing choice (ISS-003).

**Portuguese course variant** (`student-por.csv`, 649 rows) was downloaded and
retained in `Dataset/` but is not used in this project's scope, per D-006.

## 19. Model Selection Strategy

Train the full candidate set (Linear, Ridge, Lasso, Decision Tree, Random Forest,
Gradient Boosting, XGBoost) under identical CV folds and preprocessing, rank by
cross-validated RMSE and R², shortlist top 2–3 for hyperparameter tuning, then
pick the final model balancing accuracy, interpretability, and overfitting risk
(train vs. test gap). Every step and rejection reason documented in decision.md.

## 20. Evaluation Strategy

- Primary ranking metric: **RMSE** (penalizes larger errors, standard for grade
  prediction).
- Secondary: **R²** (variance explained, easy to communicate to non-technical
  stakeholders), **MAE** (interpretable "average points off").
- Residual plots and learning curves for the top 2 models to check bias/variance
  and homoscedasticity assumptions.
- Final comparison presented as a single summary table in report Chapter 5.

---

*This document is the single source of truth for project scope and will be
updated at the end of every phase. It is not final until Phase 2 (dataset
selection) is completed and confirmed with the user.*
