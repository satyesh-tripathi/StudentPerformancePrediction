# DECISION.md — Student Performance Prediction System
**Last Updated:** 2026-07-12

Every non-trivial engineering choice made on this project is logged here at the
time it's made, not retroactively.

---

### D-001 — Deployment Framework: Streamlit vs Flask
**Date:** 2026-07-12
**Problem:** PDF requires deployment via "Streamlit or Flask."
**Options:**
- Streamlit: fast to build, built-in widgets, no separate frontend code needed.
- Flask: more control over UI, but requires manual HTML/CSS/JS and more code.
**Advantages (Streamlit):** faster dev time, less boilerplate, good for a
single-model form-input demo, matches meta-prompt's explicit preference.
**Disadvantages (Streamlit):** less UI customization than a hand-built Flask+HTML app.
**Final Decision:** Streamlit.
**Reason:** Meta-prompt explicitly prefers Streamlit "unless Flask offers a
compelling advantage" — no such advantage exists for this single-form,
single-model use case.
**Future Impact:** All deployment tasks (Phase 11) target Streamlit APIs.

---

### D-002 — Python Version
**Date:** 2026-07-12
**Problem:** Need a stable, widely-compatible Python version for the venv.
**Options:** 3.10, 3.11, 3.12.
**Advantages/Disadvantages:** 3.11 has strong library compatibility (sklearn,
xgboost, streamlit all stable on it) and is mature; 3.12 is newer with some
occasional third-party package lag.
**Final Decision:** Python 3.11 (any 3.10+ acceptable, will pin exact patch
version once environment is built).
**Reason:** Best balance of stability and compatibility with the full ML stack.
**Future Impact:** `requirements.txt` and setup instructions will target 3.11.

---

### D-003 — Documentation-First Workflow
**Date:** 2026-07-12
**Problem:** Meta-prompt requires never jumping into coding before planning is
complete and confirmed.
**Options:** (a) Start coding immediately with docs as an afterthought, (b) Build
full planning docs first and gate coding behind user confirmation.
**Final Decision:** (b) — this response itself.
**Reason:** Explicit instruction: "Never skip planning," "Never jump directly
into coding," "Ask for clarification whenever required."
**Future Impact:** Dataset download and any code will only begin after the user
reviews and confirms this plan (or requests changes).

---

### D-004 — Model Candidate Set for Phase 7
**Date:** 2026-07-12
**Problem:** PDF requires "at least three" regression models; meta-prompt asks
for a broader, portfolio-grade comparison.
**Options:** Minimal set (Linear, RF, XGBoost) vs. extended set (+Ridge, Lasso,
Decision Tree, Gradient Boosting; LightGBM/CatBoost conditionally).
**Advantages (extended set):** stronger comparative analysis for report Chapter
5, demonstrates broader competency, satisfies "do not stop after training one
model."
**Disadvantages:** more training/tuning time.
**Final Decision:** Train 7 models (Linear, Ridge, Lasso, Decision Tree, Random
Forest, Gradient Boosting, XGBoost) by default; add LightGBM/CatBoost only if
the chosen dataset is large/categorical-heavy enough to show a meaningful
difference — otherwise explicitly note why they were skipped.
**Reason:** Balances thoroughness against the meta-prompt's "avoid duplicated
effort" and realistic time budget.
**Future Impact:** Phase 7 task list (T7.2–T7.9) reflects this set.

---

### D-005 — Dataset Selection
**Date:** 2026-07-12
**Problem:** Need a dataset covering attendance, assignment/internal-assessment
scores, previous academic performance, and study hours, that produces a
continuous target for regression, per PDF's "Regression Models" requirement.
**Options considered:**

| Candidate | Source | Rows | Key features | Access |
|---|---|---|---|---|
| **UCI Student Performance (Math + Portuguese)** — Cortez & Silva, 2008 | UCI Repository (mirrored on GitHub) | 395 (Math) + 649 (Portuguese) | `studytime` (study hours, ordinal), `absences` (attendance proxy), `G1`/`G2` (period grades = prior/internal assessment), `G3` (final grade, target), plus 25+ demographic/social features | Directly downloadable in this environment (`raw.githubusercontent.com` is whitelisted) |
| Students Grading Dataset (Kaggle, mahmoudelhemaly) | Kaggle | ~5,000 (reported) | `Attendance`, `Assignments_Avg`, `Midterm_Score`, `Quizzes_Avg`, `Study_Hours_per_Week`, `Total_Score` | `kaggle.com` not in this environment's allowed network domains — would need the user to download manually and upload the CSV |
| Student Exam Scores (Kaggle, mirzayasirabdullah07) | Kaggle | 200 (synthetic) | `study_hours`, `sleep_hours`, `attendance_percentage`, `previous_scores`, `exam_score` | Same Kaggle access restriction; also quite small (200 rows) |

**Advantages (UCI Student Performance):**
- Peer-reviewed, academically citable (strong for Report Chapter 2 — Literature
  Review) — published in Cortez & Silva (2008), "Using Data Mining to Predict
  Secondary School Student Performance."
- Directly and reliably downloadable right now inside this environment (no
  manual upload step needed, no Kaggle auth wall).
- Has genuinely predictive structure: `G1`/`G2` act as internal-assessment /
  prior-performance indicators, `absences` as an attendance proxy, `studytime`
  as a (banded) study-hours indicator, plus rich demographic/social context
  (parental education, family support, internet access, etc.) that supports
  meaningful EDA and feature engineering.
- Two subject variants (Math, Portuguese) can optionally be combined for a
  larger, more robust sample (~1,044 rows) — logged as an option, not yet decided.
- Matches PDF's explicit "UCI Repository" as an acceptable dataset source.

**Disadvantages:**
- `studytime` and `absences` are banded/coarser than a Kaggle dataset with raw
  hourly study-hours or exact attendance %.
- No explicit "assignment score" column — `G1`/`G2` (periodic grades) are used
  to represent internal-assessment-style performance instead, which is a
  reasonable domain substitution but will be explicitly documented as such.
- Well-known dataset — mitigated by building a genuinely original pipeline,
  EDA, and feature engineering rather than copying existing notebooks (also
  required by the PDF's Academic Integrity clause).
- A known risk with this dataset: `G3` correlates very strongly with `G2`/`G1`
  in the source literature — will be explicitly discussed as a modeling choice
  (predict with vs. without G1/G2) rather than treated as silent leakage.

**Final Decision:** Use the **UCI Student Performance Dataset — Math course
(`student-mat.csv`, 395 rows)** as the primary dataset, with the Portuguese
course (`student-por.csv`, 649 rows) available to merge in in Phase 2 if we want
a larger combined sample. This will be confirmed with the user before Phase 3.

**Reason:** Only candidate reliably accessible in this environment right now;
also the strongest academically-grounded option, and satisfies the PDF's named
source list ("Kaggle/UCI Repository").

**Future Impact:** Phase 3 (Dataset Understanding) will treat `G1`/`G2` as the
"previous academic performance / internal assessment" indicators and
`absences` as the attendance indicator — this substitution will be called out
explicitly in project.md §18 and in the Report's Methodology chapter so it's
never presented as if the dataset literally had a column named "attendance %."

---

### D-006 — Dataset Scope & G1/G2 Predictor Decision (User-Confirmed)
**Date:** 2026-07-12
**Problem:** Following D-005, two open questions needed resolving before Phase 3:
(1) use Math course alone, merge with Portuguese, or switch to a Kaggle
dataset; (2) whether to keep `G1`/`G2` (prior period grades) as predictors of
`G3`, given their very strong correlation with the target.
**Options considered:** documented in the prior turn's clarifying question;
user selected directly.
**Final Decision:**
1. **Dataset scope: Math course only** (`student-mat.csv`, 395 rows). Portuguese
   course file remains in `Dataset/` but will not be merged in for this project.
2. **G1/G2 excluded from the feature set.** The model will predict `G3` using
   only genuinely "leading" indicators — `studytime`, `absences`, and the
   demographic/social/support features — not the two prior-period grades.
**Reason:** User's explicit choice — prioritizes a harder, more realistic
early-prediction framing (predicting final performance *before* mid-year
grades exist) over maximizing raw accuracy, which is arguably the more useful
and more interesting version of "student performance prediction" for a
portfolio project. It also sidesteps the near-leakage concern flagged in D-005
entirely rather than needing to caveat it later.
**Future Impact:**
- `G1` and `G2` will be dropped from the feature set (kept in the raw dataset
  file for transparency, but excluded before training).
- Expect materially lower R² than published benchmarks on this dataset (most
  published work on this dataset uses G1/G2 and reports high R²) — this will
  be explained in the Report's Results & Discussion chapter so it reads as an
  intentional framing choice, not an unexplained weak result.
- `studytime` (1–4 ordinal scale) and `absences` (count) become the primary
  "study hours" and "attendance" proxies respectively — will be clearly
  labeled as such throughout (notebook, app UI, report).
- project.md §18 (Dataset Details) and §19 (Model Selection Strategy) will be
  updated to reflect Math-only scope and G1/G2 exclusion.

---

### D-007 — Outlier Treatment for `absences`
**Date:** 2026-07-12
**Problem:** `absences` has 15/395 students beyond the IQR upper bound (20),
up to a max of 75 — flagged as ISS-001 in Phase 3.
**Options:**
- Drop the 15 rows: simple, but loses 3.8% of an already-small (395-row) dataset.
- Log-transform `absences`: reduces skew well but makes the feature less
  directly interpretable in the Streamlit UI ("log-absences" is not something
  a teacher/student can intuitively enter).
- Cap (winsorize) at the IQR upper bound (20): keeps all 395 records, reduces
  the extreme-value influence on distance/gradient-based models, keeps the
  feature in its original, interpretable unit (days absent).
**Final Decision:** Cap `absences` at 20 (the IQR upper bound) rather than
drop or log-transform.
**Reason:** Preserves sample size (important for a 395-row dataset), keeps the
feature human-interpretable for the deployed app, and still meaningfully
reduces the influence of extreme values (75, 56, 54, etc.) on linear/
regularized models.
**Future Impact:** `Dataset/student_mat_cleaned.csv` has `absences` capped at
20. This cap value must be reused at inference time in the Streamlit app (any
user-entered absence count above 20 will be capped the same way) — noted for
Phase 11.

---

### D-008 — Encoding Strategy & Deferred Scaling
**Date:** 2026-07-12
**Problem:** 17 categorical columns need encoding before modeling; numeric
features are on very different scales (e.g., `age` ~15-22 vs `absences` 0-20
vs binary flags 0/1).
**Options (encoding):**
- Label-encode everything: fast, but implies false ordinality for nominal
  columns like `Mjob`/`Fjob`/`reason`/`guardian`.
- One-hot encode everything: correct, but inflates dimensionality
  unnecessarily for genuinely binary columns.
**Final Decision (encoding):** Hybrid — binary yes/no and binary-nominal
columns (school, sex, address, famsize, Pstatus, schoolsup, famsup, paid,
activities, nursery, higher, internet, romantic) mapped to a single 0/1
column each; true multi-category nominal columns (Mjob, Fjob, reason,
guardian) one-hot encoded with `drop_first=True` to avoid the dummy-variable
trap. Result: 395 rows × 40 columns (39 features + target), all numeric.

**Options (scaling):**
- Scale now, before train/test split: simpler code, but leaks test-set
  distribution statistics into training (technically a form of data leakage).
- Scale inside the modeling pipeline, fit only on the training split.
**Final Decision (scaling):** Deferred to Phase 7 — `StandardScaler` will be
fit only on the training data inside an `sklearn.Pipeline`/`ColumnTransformer`,
then applied to the test split and to live app inputs at inference time.
**Reason:** Standard best practice to prevent train/test leakage; also means
tree-based models (which don't need scaling) can reuse the same cleaned CSV
without unnecessary preprocessing.
**Future Impact:** `Dataset/student_mat_cleaned.csv` is unscaled by design.
Phase 7 training scripts must build the scaler inside the pipeline, not
before the split.

---

### D-009 — Skipping Pair Plots; EDA Headline Findings
**Date:** 2026-07-12
**Problem:** Task T5.4 (pair plots) is marked "if appropriate" in the PDF.
With 13 numeric features, a full pairplot is a 13×13 grid — too dense to
extract readable insight from, and largely redundant with the correlation
heatmap + individual scatter plots already produced.
**Options:** Full 13×13 pairplot vs. targeted scatter grid (6 most relevant
features vs. G3) + full correlation heatmap.
**Final Decision:** Skip the full pairplot; keep the targeted scatter grid and
heatmap, which cover the same relationships more legibly.
**Reason:** "If appropriate" in the PDF explicitly allows this judgment call;
a 169-panel grid would not aid interpretation and conflicts with the
meta-prompt's emphasis on genuine insight over checkbox completion.
**Future Impact:** None — T5.4 logged as SKIPPED (not silently omitted) in
task.md with reasoning here.

**EDA headline findings carried into Phase 6 (Feature Engineering):**
- `failures` is the strongest available predictor (r ≈ -0.36) in the
  G1/G2-excluded framing.
- `higher` (aspiration for higher education) is the strongest categorical
  signal: mean G3 = 6.80 (no) vs 10.61 (yes) — a ~4-point gap.
- `schoolsup` shows a lower mean G3 among supported students (9.43 vs 10.56)
  — flagged as confounded (support targets struggling students), not causal;
  will be stated explicitly in the report to avoid a misleading claim.
- `absences` shows minimal linear correlation with G3 even after capping —
  its value, if any, is likely non-linear/interactive rather than direct.
- `Medu`, `Fedu`, `studytime`, `goout` all show weak-but-consistent trends
  worth retaining; combining `Medu`+`Fedu` into a composite is a Phase 6
  candidate feature.

---

*(This log will continue to grow in Phases 6–10 — e.g., feature engineering
choices, final model selection, and every rejected alternative along the way.)*
