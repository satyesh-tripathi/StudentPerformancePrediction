# ISSUES.md — Student Performance Prediction System
**Last Updated:** 2026-07-12

## Issue Log

| Issue ID | Description | Root Cause | Severity | Status | Solution | Future Prevention |
|---|---|---|---|---|---|---|
| ISS-001 | `absences` is heavily right-skewed with extreme values (max 75; 15/395 students >20) | Real-world attendance data is naturally skewed — a small number of students with very high absence counts (possibly chronic absenteeism or data entry of unusual real cases) | Medium | Open — to resolve in Phase 4 (Data Cleaning) | TBD — likely IQR-cap or log-transform rather than drop, since these may be genuine (not erroneous) extreme cases; final call logged in decision.md during Phase 4 | For future datasets, always run outlier detection before assuming a numeric column is well-behaved |
| ISS-002 | 38/395 students (9.6%) have `G3` = 0 | Per the dataset's original documentation (Cortez & Silva, 2008), a G3 of 0 is common and typically indicates the student did not sit the final exam, rather than a data error | Low | Open — to resolve in Phase 4/5 | Will keep these records (they are valid, not corrupted) but flag and visualize separately in EDA so they don't silently distort the target distribution or model | Always check whether target=0 is a data artifact or a real, meaningful category before treating as an outlier |
| ISS-003 | Excluding G1/G2 (per D-006) drops correlation with target sharply — strongest remaining predictor (`failures`, r=-0.36) is far weaker than G1/G2 (r=0.80–0.90) | Expected consequence of the user's deliberate "no prior-grade features" framing, not a bug | Low (expected, not a defect) | Resolved — accepted as intentional design tradeoff | Will be explicitly explained in Report Ch.5 so low R² doesn't read as an unexplained failure | Document intentional scope/framing decisions immediately so weaker downstream metrics aren't mistaken for bugs later |

## Anticipated Risk Categories (to watch for, not yet occurred)

These are pre-identified based on the ML lifecycle and this dataset domain —
listed here so nothing is a surprise later, per issues encountered:

- **Missing values** in attendance/assignment columns (common in education data)
- **Data leakage** — e.g., a "final grade letter" column that directly encodes
  the numeric target
- **Overfitting** — especially Decision Tree / untuned boosting models
- **Underfitting** — plain Linear Regression if relationships are non-linear
- **Class/feature imbalance** — less relevant for regression but watch for
  skewed feature distributions (e.g., most students with near-100% attendance)
- **Encoding issues** — categorical features like "gender," "parental education"
  if present in chosen dataset
- **Deployment bugs** — Streamlit app failing to load pickled model due to
  sklearn version mismatch between training and app environment
- **Package/version conflicts** — xgboost/sklearn/streamlit version mismatches
- **Visualization issues** — seaborn/matplotlib rendering differences across
  environments

*Entries will be added here with full Issue ID / Root Cause / Solution detail as
they actually occur during Phases 2–13.*
