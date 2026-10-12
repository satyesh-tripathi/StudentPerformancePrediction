# Student Performance Predictor

AIML Summer Internship 2026 capstone, IIHMF, MNNIT Allahabad, Prayagraj.

**Live app:** https://studentperformanceprediction-kbnar9atvbm9bfjbzrzrsa.streamlit.app/

A machine learning web app that gives a student a likely final grade (0 to 20) and the habits linked with moving it. It is built for students: a short, calm question flow, then a result with a grade range, habits worth changing, and a "try a different week" what-if.

## What it does

- Predicts the final maths grade (`G3`) from study habits, school life, and home background.
- Deliberately leaves out the earlier term grades (`G1`, `G2`), so it can be used before those exist. This makes the problem harder and the accuracy lower than published results that use them.
- Shows a likely range, not a single number.
- Suggests only habits that held up in testing: study time, going out less, and weekday alcohol. When nothing shows a clear gain, it says so.

## How accurate is it

| Measure | Value |
|---|---|
| Held-out test (20% of students) | MAE 3.21, RMSE 3.92, R² 0.251 |
| 5-fold cross-validation (5 seeds) | MAE 2.98, RMSE 3.91, R² 0.27 |
| Predictions within 3 grade points | about 62% |

The typical error is about 3 grade points. The model is a guide for thinking about habits, not a prediction to live up or down to. Habit suggestions are patterns in 395 students' records, not guarantees. Details are in `Documentation/decision.md` (D-010, D-011).

## Data

UCI Student Performance dataset, Math course (Cortez and Silva, 2008): 395 students, 33 columns, no missing values. `Dataset/student-mat.csv` is the Math file used here. `Dataset/student-por.csv` is the Portuguese course file, kept for reference and not used.

## Project structure

```
Dataset/         raw data, cleaned data, and engineered features
Notebook/        exploratory data analysis
src/             data_cleaning.py, feature_engineering.py, hyperparameter_tuning.py
Model/           student_performance_best_model.pkl (scaler + XGBoost pipeline)
Streamlit_App/   the web app (app.py, views.py, model_io.py, levers.py, theme.py)
Documentation/   project.md, task.md, decision.md, issues.md,
                 Student_Performance_Prediction_Report.pdf,
                 Student_Performance_Prediction_PPT.pptx
.streamlit/      theme settings
```

## Run it

Run everything from the project root (the folder containing this file). Tested with Python 3.13; `requirements.txt` pins the exact package versions, and scikit-learn and xgboost must match because the saved model was trained with them.

```
pip install -r requirements.txt
streamlit run Streamlit_App/app.py
```

To rebuild the data and model from the raw file:

```
python src/data_cleaning.py
python src/feature_engineering.py
python src/hyperparameter_tuning.py
```

`hyperparameter_tuning.py` overwrites `Model/student_performance_best_model.pkl`.

## Documentation

- `Documentation/project.md`: scope, requirements, and plan
- `Documentation/decision.md`: every engineering decision and why
- `Documentation/issues.md`: problems found and how they were resolved
- `Documentation/task.md`: task tracker
