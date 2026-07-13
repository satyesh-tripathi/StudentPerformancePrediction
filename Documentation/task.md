# TASK.md — Student Performance Prediction System
**Legend — Status:** `TODO` | `IN-PROGRESS` | `BLOCKED` | `DONE`
**Owner for all tasks:** Claude (unless noted)
**Last Updated:** 2026-07-12

---

## PHASE 0 — Planning

| Task ID | Title | Priority | Dependencies | Est. Time | Status | Notes |
|---|---|---|---|---|---|---|
| T0.1 | Read & extract requirements from guideline PDF | High | — | 1h | DONE | See project.md §5–15 |
| T0.2 | Create project.md | High | T0.1 | 1h | DONE | v1.0 created |
| T0.3 | Create task.md | High | T0.1 | 1h | IN-PROGRESS | this file |
| T0.4 | Create decision.md | High | T0.1 | 0.5h | TODO | |
| T0.5 | Create issues.md | High | T0.1 | 0.5h | TODO | |
| T0.6 | Get user confirmation on plan before coding | High | T0.2–T0.5 | — | TODO | **blocking gate — do not code before this** |

## PHASE 1 — Problem Understanding

| Task ID | Title | Priority | Dependencies | Est. Time | Status | Notes |
|---|---|---|---|---|---|---|
| T1.1 | Define business problem statement | High | — | 0.5h | DONE | project.md §2 |
| T1.2 | Define objectives & success criteria | High | T1.1 | 0.5h | DONE | project.md §3–4 |
| T1.3 | Identify target variable type (regression, continuous) | High | T1.1 | 0.5h | DONE | confirmed regression per PDF |

## PHASE 2 — Dataset Selection

| Task ID | Title | Priority | Dependencies | Est. Time | Status | Notes |
|---|---|---|---|---|---|---|
| T2.1 | Search Kaggle/UCI for candidate datasets | High | Phase 0 gate | 1h | DONE | 6+ candidates found (Kaggle + UCI) |
| T2.2 | Compare candidates on feature coverage & quality | High | T2.1 | 0.5h | DONE | see decision.md D-005 |
| T2.3 | Recommend + document final dataset choice | High | T2.2 | 0.5h | DONE | UCI Student Performance (Math+Por) — decision.md D-005 |
| T2.4 | Download dataset into `Dataset/` | High | T2.3 | 0.25h | DONE | student-mat.csv + student-por.csv fetched, pending user confirmation |
| T2.5 | Verify dataset integrity (row count, columns match source) | Medium | T2.4 | 0.25h | DONE | 395 rows (Math), 649 rows (Por), 33 columns each, matches UCI spec |

## PHASE 3 — Dataset Understanding

| Task ID | Title | Priority | Dependencies | Est. Time | Status | Notes |
|---|---|---|---|---|---|---|
| T3.1 | Profile columns & dtypes | High | T2.5 | 0.5h | DONE | 33 cols: 17 categorical (object), 16 numeric (incl. G1/G2/G3) |
| T3.2 | Missing value analysis | High | T2.5 | 0.5h | DONE | 0 missing values anywhere — clean dataset |
| T3.3 | Duplicate detection | High | T2.5 | 0.25h | DONE | 0 duplicate rows |
| T3.4 | Descriptive statistics (mean/median/std/min/max) | High | T2.5 | 0.5h | DONE | G3: mean 10.4, std 4.58, range 0–20 |
| T3.5 | Target variable distribution check | High | T2.5 | 0.5h | DONE | roughly bell-shaped, but 38/395 students (~9.6%) have G3=0 — needs EDA visual + discussion, not necessarily an error (likely dropouts/no-shows per source docs) |
| T3.6 | Feature type classification (numeric/categorical/ordinal) | Medium | T3.1 | 0.5h | DONE | 17 categorical (mostly binary yes/no or nominal), 13 usable numeric features (excl. G1/G2/G3), several are ordinal-coded (studytime 1–4, Medu/Fedu 0–4, famrel/freetime/goout/Dalc/Walc/health 1–5) |
| T3.7 | Document data quality issues found | Medium | T3.1–T3.6 | 0.5h | DONE | `absences` has heavy right-skew/outliers (max 75, 15 students >20 absences) — logged in issues.md; no missing/duplicate issues |

## PHASE 4 — Data Cleaning

| Task ID | Title | Priority | Dependencies | Est. Time | Status | Notes |
|---|---|---|---|---|---|---|
| T4.1 | Handle missing values (impute/drop, documented strategy) | High | Phase 3 | 1h | DONE | none present — no action needed |
| T4.2 | Remove/handle duplicates | High | Phase 3 | 0.25h | DONE | none present — no action needed |
| T4.3 | Outlier detection (IQR/Z-score) | High | Phase 3 | 0.5h | DONE | `absences` upper bound = 20, 15 students beyond it |
| T4.4 | Outlier treatment (cap/remove/keep + reason) | High | T4.3 | 0.5h | DONE | capped at 20 — decision.md D-007 |
| T4.5 | Fix wrong/invalid datatypes | Medium | Phase 3 | 0.25h | DONE | all dtypes already correct |
| T4.6 | Encode categorical features | High | T4.1–T4.5 | 0.5h | DONE | hybrid binary-map + one-hot — decision.md D-008 |
| T4.7 | Scale/normalize numeric features | High | T4.6 | 0.5h | DONE (deferred) | intentionally deferred to Phase 7 pipeline — decision.md D-008 |
| T4.8 | Leakage review (drop any post-outcome features) | High | T4.1–T4.7 | 0.5h | DONE | G1/G2 dropped per D-006 |
| T4.9 | Save cleaned dataset to `Dataset/` | Medium | T4.8 | 0.25h | DONE | `Dataset/student_mat_cleaned.csv` (395 × 40) |

## PHASE 5 — Exploratory Data Analysis

| Task ID | Title | Priority | Dependencies | Est. Time | Status | Notes |
|---|---|---|---|---|---|---|
| T5.1 | Univariate analysis (histograms/distribution plots, all features) | High | Phase 4 | 1h | DONE | `Notebook/eda.ipynb` §2, `figures/02_univariate_numeric.png` |
| T5.2 | Bivariate analysis (feature vs target scatter plots) | High | Phase 4 | 1h | DONE | `Notebook/eda.ipynb` §4, `figures/04_bivariate_scatter.png` |
| T5.3 | Correlation matrix + heatmap | High | Phase 4 | 0.5h | DONE | `Notebook/eda.ipynb` §5, `figures/05_correlation_heatmap.png` |
| T5.4 | Pair plots (if feature count allows) | Low | Phase 4 | 0.5h | SKIPPED | 13 numeric features → pairplot too dense to be readable; heatmap + scatter grid covers the same ground more clearly — logged as a deliberate skip, not an omission |
| T5.5 | Boxplots per feature (outlier visualization) | Medium | Phase 4 | 0.5h | DONE | `Notebook/eda.ipynb` §6, `figures/06_absences_outliers.png` (before/after capping) |
| T5.6 | Target distribution plot | Medium | Phase 4 | 0.25h | DONE | `Notebook/eda.ipynb` §1, `figures/01_target_distribution.png` |
| T5.7 | Write insight notes after every chart | High | T5.1–T5.6 | 1h | DONE | markdown insight cell after every visualization, verified against actual computed output |

## PHASE 6 — Feature Engineering

| Task ID | Title | Priority | Dependencies | Est. Time | Status | Notes |
|---|---|---|---|---|---|---|
| T6.1 | Brainstorm derived features (e.g., attendance×study-hours interaction) | Medium | Phase 5 | 0.5h | TODO | |
| T6.2 | Implement new features | Medium | T6.1 | 0.5h | TODO | |
| T6.3 | Feature importance / correlation-based selection | High | T6.2 | 0.5h | TODO | |
| T6.4 | Remove low-value/redundant features | Medium | T6.3 | 0.25h | TODO | |
| T6.5 | Document every add/remove decision | High | T6.1–T6.4 | 0.5h | TODO | feeds decision.md |

## PHASE 7 — Model Development

| Task ID | Title | Priority | Dependencies | Est. Time | Status | Notes |
|---|---|---|---|---|---|---|
| T7.1 | Train/test split | High | Phase 6 | 0.25h | TODO | |
| T7.2 | Train Linear Regression (baseline) | High | T7.1 | 0.25h | TODO | |
| T7.3 | Train Ridge Regression | Medium | T7.1 | 0.25h | TODO | |
| T7.4 | Train Lasso Regression | Medium | T7.1 | 0.25h | TODO | |
| T7.5 | Train Decision Tree Regressor | Medium | T7.1 | 0.25h | TODO | |
| T7.6 | Train Random Forest Regressor | High | T7.1 | 0.25h | TODO | |
| T7.7 | Train Gradient Boosting Regressor | Medium | T7.1 | 0.25h | TODO | |
| T7.8 | Train XGBoost Regressor | High | T7.1 | 0.25h | TODO | |
| T7.9 | Evaluate LightGBM/CatBoost fit-for-purpose (add only if justified) | Low | T7.1 | 0.25h | TODO | decision logged either way |

## PHASE 8 — Hyperparameter Tuning

| Task ID | Title | Priority | Dependencies | Est. Time | Status | Notes |
|---|---|---|---|---|---|---|
| T8.1 | Select top 2–3 models from Phase 7 for tuning | High | Phase 7 | 0.25h | TODO | |
| T8.2 | GridSearchCV / RandomizedSearchCV per selected model | High | T8.1 | 1h | TODO | |
| T8.3 | K-fold cross-validation scoring | High | T8.2 | 0.5h | TODO | |
| T8.4 | Log every experiment (params tried, scores) | High | T8.2–T8.3 | 0.5h | TODO | feeds decision.md |

## PHASE 9 — Model Evaluation

| Task ID | Title | Priority | Dependencies | Est. Time | Status | Notes |
|---|---|---|---|---|---|---|
| T9.1 | Compute MAE/MSE/RMSE/R² for all tuned models | High | Phase 8 | 0.5h | TODO | |
| T9.2 | Residual analysis plots | Medium | T9.1 | 0.5h | TODO | |
| T9.3 | Learning curves (top model) | Low | T9.1 | 0.5h | TODO | |
| T9.4 | Build comparison summary table | High | T9.1 | 0.25h | TODO | |
| T9.5 | Select & justify final model | High | T9.4 | 0.5h | TODO | logged in decision.md |

## PHASE 10 — Model Saving

| Task ID | Title | Priority | Dependencies | Est. Time | Status | Notes |
|---|---|---|---|---|---|---|
| T10.1 | Save trained model (joblib) | High | Phase 9 | 0.25h | TODO | |
| T10.2 | Save scaler | High | Phase 9 | 0.25h | TODO | |
| T10.3 | Save encoder | High | Phase 9 | 0.25h | TODO | |
| T10.4 | Save feature list / version metadata (JSON) | Medium | Phase 9 | 0.25h | TODO | |

## PHASE 11 — Deployment

| Task ID | Title | Priority | Dependencies | Est. Time | Status | Notes |
|---|---|---|---|---|---|---|
| T11.1 | Build Streamlit UI skeleton (inputs for all features) | High | Phase 10 | 1h | TODO | |
| T11.2 | Wire up prediction pipeline (load model+scaler+encoder) | High | T11.1 | 1h | TODO | |
| T11.3 | Add input validation (ranges, types) | High | T11.2 | 0.5h | TODO | |
| T11.4 | Add interpretation/confidence messaging | Medium | T11.2 | 0.5h | TODO | |
| T11.5 | Style/polish UI | Low | T11.1–T11.4 | 0.5h | TODO | |
| T11.6 | (Optional) Deploy to Streamlit Community Cloud | Low | T11.5 | 0.5h | TODO | needs user's GitHub if wanted |

## PHASE 12 — Testing

| Task ID | Title | Priority | Dependencies | Est. Time | Status | Notes |
|---|---|---|---|---|---|---|
| T12.1 | Test model load & predict programmatically | High | Phase 11 | 0.25h | TODO | |
| T12.2 | Test Streamlit app happy path | High | Phase 11 | 0.25h | TODO | |
| T12.3 | Test edge cases (0 attendance, max scores, blank fields) | High | Phase 11 | 0.5h | TODO | |
| T12.4 | Test invalid inputs (negative numbers, out-of-range) | High | Phase 11 | 0.5h | TODO | |
| T12.5 | Log all bugs found & fixes | High | T12.1–T12.4 | 0.5h | TODO | feeds issues.md |

## PHASE 13 — Documentation (continuous, not a single task block)

| Task ID | Title | Priority | Dependencies | Est. Time | Status | Notes |
|---|---|---|---|---|---|---|
| T13.1 | Keep project.md updated after every phase | High | ongoing | ongoing | TODO | |
| T13.2 | Keep task.md updated after every phase | High | ongoing | ongoing | TODO | |
| T13.3 | Keep decision.md updated after every decision | High | ongoing | ongoing | TODO | |
| T13.4 | Keep issues.md updated after every bug | High | ongoing | ongoing | TODO | |
| T13.5 | Write README.md | High | Phase 11 | 1h | TODO | |

## PHASE 14 — Project Report

| Task ID | Title | Priority | Dependencies | Est. Time | Status | Notes |
|---|---|---|---|---|---|---|
| T14.1 | Draft Chapter 1: Introduction | High | Phases 1–2 | 1h | TODO | |
| T14.2 | Draft Chapter 2: Literature Review | Medium | — | 1.5h | TODO | needs 4–6 sourced studies |
| T14.3 | Draft Chapter 3: Methodology | High | Phases 2–4 | 1.5h | TODO | |
| T14.4 | Draft Chapter 4: Implementation | High | Phases 5–7 | 2h | TODO | |
| T14.5 | Draft Chapter 5: Results & Discussion | High | Phase 9 | 1.5h | TODO | |
| T14.6 | Draft Chapter 6: Conclusion & Future Scope | Medium | all | 1h | TODO | |
| T14.7 | Compile References | Medium | T14.2 | 0.5h | TODO | |
| T14.8 | Format as Word doc (docx skill), check 15–25 page length | High | T14.1–T14.7 | 1h | TODO | |

## PHASE 15 — Presentation

| Task ID | Title | Priority | Dependencies | Est. Time | Status | Notes |
|---|---|---|---|---|---|---|
| T15.1 | Build 10–15 slide deck per PDF structure | High | Phase 14 | 1.5h | TODO | pptx skill |
| T15.2 | Add demo screenshots from Streamlit app | Medium | Phase 11 | 0.5h | TODO | |
| T15.3 | Prep 10-min talk track + 5-min demo flow | Medium | T15.1 | 0.5h | TODO | |

## PHASE 16 — Final Packaging

| Task ID | Title | Priority | Dependencies | Est. Time | Status | Notes |
|---|---|---|---|---|---|---|
| T16.1 | Assemble final folder structure exactly as mandated | High | all | 0.5h | TODO | |
| T16.2 | Zip as `ProjectName_TeamLeaderName.zip` | High | T16.1 | 0.25h | TODO | needs team leader name from user |
| T16.3 | Final QA pass against Quality Checklist | High | T16.1–T16.2 | 0.5h | TODO | |

---

**Next Immediate Action:** Complete T0.4 (decision.md) and T0.5 (issues.md), then
present the full plan to the user for confirmation (T0.6) before any dataset
download or code is written.
