"""Model loading, feature building and prediction for the student-facing app."""
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import streamlit as st

MODEL_PATH = Path(__file__).resolve().parent.parent / "Model" / "student_performance_best_model.pkl"

# Measured with 5-fold cross-validation (5 seeds) of the saved pipeline on the 395 Math-course rows in
# Dataset/student_mat_features.csv (previous-period grades excluded, per decision D-006):
# MAE 2.98, RMSE 3.91, R2 0.27; about 62% of predictions land within 3 points.
DATASET_SIZE = 395
TYPICAL_ERROR = 3.0
CV_R2 = 0.27
PASS_MARK = 10
ABSENCE_CAP = 20  # D-007: absences are capped at the IQR upper bound in training

# Median student in Dataset/student_mat_features.csv (Math course, 395 rows). Used as the "typical student"
# reference when working out what moved a prediction.
REFERENCE = {
    "sex_F": 1, "age": 17, "famsize_GT3": 1, "traveltime": 1, "studytime": 2,
    "failures": 0, "schoolsup": 0, "famsup": 1, "activities": 1, "higher": 1,
    "internet": 1, "romantic": 0, "famrel": 4, "freetime": 3, "goout": 3,
    "Dalc": 1, "Walc": 2, "health": 4, "absences": 4, "Mjob_health": 0,
    "Mjob_other": 0, "Mjob_services": 0, "Fjob_other": 1, "Fjob_teacher": 0,
    "reason_reputation": 0, "guardian_mother": 1, "guardian_other": 0,
    "parental_edu_avg": 2.5,
}

# Each group is a set of model inputs that mean one thing to a teacher.
FACTOR_GROUPS = {
    "Study time": ["studytime"],
    "Past failures": ["failures"],
    "Absences": ["absences"],
    "Wants higher education": ["higher"],
    "Parents' education": ["parental_edu_avg"],
    "School and family help": ["schoolsup", "famsup"],
    "Going out and free time": ["goout", "freetime"],
    "Alcohol use": ["Dalc", "Walc"],
    "Health": ["health"],
    "Home life": ["famrel", "famsize_GT3", "guardian_mother", "guardian_other"],
    "Parents' jobs": ["Mjob_health", "Mjob_other", "Mjob_services", "Fjob_other", "Fjob_teacher"],
    "Internet at home": ["internet"],
    "Age and sex": ["age", "sex_F"],
    "Travel and school choice": ["traveltime", "reason_reputation"],
    "Activities and relationships": ["activities", "romantic"],
}

# Factor groups shown to students: things they can relate to and act on or reflect on.
# Family and background groups are deliberately left out of the student-facing breakdown.
STUDENT_FACTORS = [
    "Study time", "Past failures", "Absences", "Wants higher education",
    "Going out and free time", "Alcohol use", "Health",
]

DEFAULTS = {
    "age": 17, "sex": "F", "famsize": "GT3", "studytime": 2, "failures": 0,
    "traveltime": 1, "absences": 4, "higher": True, "Medu": 3, "Fedu": 2,
    "famrel": 4, "Mjob": "other", "Fjob": "other", "guardian": "mother",
    "schoolsup": False, "famsup": True, "internet": True, "reason": "course",
    "freetime": 3, "goout": 3, "health": 4, "Dalc": 1, "Walc": 2,
    "activities": True, "romantic": False,
}

PRESETS = {
    "A balanced week": {},
    "Lots to juggle": {
        "age": 18, "failures": 2, "studytime": 1, "absences": 12, "higher": False,
        "Medu": 1, "Fedu": 1, "famrel": 3, "schoolsup": True, "famsup": False,
        "internet": False, "goout": 5, "health": 2, "Dalc": 3, "Walc": 4,
    },
    "A strong routine": {
        "age": 16, "studytime": 4, "absences": 0, "Medu": 4, "Fedu": 4, "famrel": 5,
        "famsup": True, "reason": "reputation", "goout": 2, "health": 5, "Dalc": 1, "Walc": 1,
    },
}

STUDY_LABELS = {1: "Under 2 hours", 2: "2 to 5 hours", 3: "5 to 10 hours", 4: "Over 10 hours"}
TRAVEL_LABELS = {1: "Under 15 min", 2: "15 to 30 min", 3: "30 min to 1 hour", 4: "Over 1 hour"}
EDU_LABELS = {0: "None", 1: "Primary school", 2: "Lower secondary", 3: "Upper secondary", 4: "Higher education"}
REASON_LABELS = {"course": "Course on offer", "reputation": "School reputation", "home": "Close to home", "other": "Another reason"}
JOB_LABELS = {"at_home": "At home", "health": "Health care", "services": "Civil services", "teacher": "Teacher", "other": "Other"}


@st.cache_resource
def load_pipeline():
    return joblib.load(MODEL_PATH) if MODEL_PATH.exists() else None


def features_from_state(s) -> dict:
    return {
        "sex_F": int(s["sex"] == "F"), "age": s["age"], "famsize_GT3": int(s["famsize"] == "GT3"),
        "traveltime": s["traveltime"], "studytime": s["studytime"], "failures": s["failures"],
        "schoolsup": int(s["schoolsup"]), "famsup": int(s["famsup"]), "activities": int(s["activities"]),
        "higher": int(s["higher"]), "internet": int(s["internet"]), "romantic": int(s["romantic"]),
        "famrel": s["famrel"], "freetime": s["freetime"], "goout": s["goout"], "Dalc": s["Dalc"],
        "Walc": s["Walc"], "health": s["health"], "absences": min(s["absences"], ABSENCE_CAP),
        "Mjob_health": int(s["Mjob"] == "health"), "Mjob_other": int(s["Mjob"] == "other"),
        "Mjob_services": int(s["Mjob"] == "services"), "Fjob_other": int(s["Fjob"] == "other"),
        "Fjob_teacher": int(s["Fjob"] == "teacher"), "reason_reputation": int(s["reason"] == "reputation"),
        "guardian_mother": int(s["guardian"] == "mother"), "guardian_other": int(s["guardian"] == "other"),
        "parental_edu_avg": (s["Medu"] + s["Fedu"]) / 2.0,
    }


def predict_rows(rows: list) -> np.ndarray:
    """Predict a grade (clipped to 0-20) for each feature dict, in one model call."""
    pipeline = load_pipeline()
    frame = pd.DataFrame(rows).reindex(columns=list(pipeline.feature_names_in_)).astype(float)
    return np.clip(pipeline.predict(frame), 0, 20)


def predict_with_drivers(feats: dict):
    """Predict once, then re-predict with each factor group set to the typical student."""
    rows = [feats]
    for cols in FACTOR_GROUPS.values():
        rows.append({**feats, **{c: REFERENCE[c] for c in cols}})
    preds = predict_rows(rows)
    base = float(preds[0])
    drivers = {name: base - float(p) for name, p in zip(FACTOR_GROUPS, preds[1:])}
    return base, drivers
