from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import streamlit as st

MODEL_PATH = Path(__file__).resolve().parent.parent / "Model" / "student_performance_best_model.pkl"

# Measured with 5-fold cross-validation of the saved pipeline on the 395-student
# dataset (previous-period grades excluded, per decision D-006).
TYPICAL_ERROR = 2.0
CV_R2 = 0.26
PASS_MARK = 10
ABSENCE_CAP = 20  # D-007: absences are capped at the IQR upper bound in training

# Median student in Dataset/student_mat_features.csv. Used as the "typical student"
# reference when working out what moved a prediction.
REFERENCE = {
    "sex_F": 1, "age": 17, "famsize_GT3": 1, "traveltime": 1, "studytime": 2,
    "failures": 0, "schoolsup": 0, "famsup": 1, "activities": 0, "higher": 1,
    "internet": 1, "romantic": 0, "famrel": 4, "freetime": 3, "goout": 3,
    "Dalc": 1, "Walc": 2, "health": 4, "absences": 2, "Mjob_health": 0,
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

DEFAULTS = {
    "age": 17, "sex": "F", "famsize": "GT3", "studytime": 2, "failures": 0,
    "traveltime": 1, "absences": 2, "higher": True, "Medu": 2, "Fedu": 2,
    "famrel": 4, "Mjob": "other", "Fjob": "other", "guardian": "mother",
    "schoolsup": False, "famsup": True, "internet": True, "reason": "course",
    "freetime": 3, "goout": 3, "health": 4, "Dalc": 1, "Walc": 2,
    "activities": False, "romantic": False,
}

PRESETS = {
    "Typical student": {},
    "Needs support": {
        "age": 18, "failures": 2, "studytime": 1, "absences": 12, "higher": False,
        "Medu": 1, "Fedu": 1, "famrel": 3, "schoolsup": True, "famsup": False,
        "internet": False, "goout": 5, "health": 2, "Dalc": 3, "Walc": 4,
    },
    "Strong profile": {
        "age": 16, "studytime": 4, "absences": 0, "Medu": 4, "Fedu": 4, "famrel": 5,
        "famsup": True, "reason": "reputation", "goout": 2, "health": 5, "Dalc": 1, "Walc": 1,
    },
}

STUDY_LABELS = {1: "Under 2 hours", 2: "2 to 5 hours", 3: "5 to 10 hours", 4: "Over 10 hours"}
TRAVEL_LABELS = {1: "Under 15 min", 2: "15 to 30 min", 3: "30 min to 1 hour", 4: "Over 1 hour"}
EDU_LABELS = {0: "None", 1: "Primary school", 2: "Lower secondary", 3: "Upper secondary", 4: "Higher education"}
REASON_LABELS = {"course": "Course on offer", "reputation": "School reputation", "home": "Close to home", "other": "Another reason"}
JOB_LABELS = {"at_home": "At home", "health": "Health care", "services": "Civil services", "teacher": "Teacher", "other": "Other"}

st.set_page_config(page_title="Student Performance Predictor", page_icon=":material/school:", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,400;12..96,500;12..96,700;12..96,800&family=Caveat:wght@600;700&display=swap');

:root {
    --paper: #F3F6FB;
    --rule: #D6E2F5;
    --line: #C3D1E8;
    --ink: #14213D;
    --muted: #55657F;
    --pen: #D1343B;
}

.stApp, .stApp p, .stApp label, .stApp button, .stApp input, .stApp textarea,
.stApp [data-baseweb="select"], .stApp [data-testid="stWidgetLabel"] {
    font-family: 'Bricolage Grotesque', system-ui, sans-serif;
}
.stApp { color: var(--ink); }
header[data-testid="stHeader"] { background: transparent; }
.block-container { max-width: 1180px; padding: 2.6rem 2rem 4rem; }

/* Page title */
.page-title { font-size: 40px; font-weight: 800; line-height: 1.05; letter-spacing: -0.025em; margin: 0 0 10px; }
.page-lede { font-size: 16px; line-height: 1.55; color: var(--muted); max-width: 56ch; margin: 0 0 28px; }

/* Form sections: separated by rules, not boxed */
.sec { border-top: 2px solid var(--ink); margin: 34px 0 14px; padding-top: 10px; }
.sec h2 { font-size: 20px; font-weight: 700; letter-spacing: -0.01em; margin: 0; padding: 0; }
.sec p { font-size: 15px; color: var(--muted); margin: 3px 0 0; }
.sec-first { margin-top: 18px; }

.stApp label, [data-testid="stWidgetLabel"] p { font-size: 15px; font-weight: 500; }
.stButton > button {
    background: #fff; color: var(--ink); border: 1.5px solid var(--ink); border-radius: 6px;
    font-weight: 600; font-size: 15px; padding: 6px 14px; min-height: 44px;
    transition: background-color .12s ease, color .12s ease;
}
.stButton > button:active { background: #D6E2F5; color: var(--ink); }
.stButton > button:hover { background: var(--ink); color: #fff; border-color: var(--ink); }
.stButton > button:focus-visible { outline: 3px solid var(--pen); outline-offset: 2px; }

/* The marking page: sticky ruled sheet beside the form */
div[data-testid="stColumn"]:has(.marking-anchor) { position: sticky; top: 1.2rem; align-self: flex-start; }
.sheet {
    position: relative; background-color: #fff; border: 1.5px solid var(--ink); border-radius: 4px;
    box-shadow: 5px 5px 0 var(--ink);
    background-image: repeating-linear-gradient(to bottom, transparent 0 31px, var(--rule) 31px 32px);
    background-position: 0 14px; padding: 22px 24px 20px 62px; margin-bottom: 20px;
}
.sheet::before { content: ""; position: absolute; top: 0; bottom: 0; left: 40px; width: 2px; background: var(--pen); opacity: .75; }
.sheet-label { font-size: 15px; font-weight: 500; color: var(--muted); margin: 0; }
.grade-row { display: flex; align-items: center; gap: 14px; margin: 4px 0 2px; }
.grade-wrap { position: relative; width: 150px; height: 96px; flex: none; }
.grade-wrap::before { content: ""; position: absolute; inset: 2px 0 6px; border: 3.5px solid var(--pen);
    border-radius: 52% 48% 55% 45% / 58% 50% 50% 42%; transform: rotate(-4deg); border-right-color: transparent; }
.grade-wrap::after { content: ""; position: absolute; inset: 5px 3px 3px; border: 3px solid var(--pen);
    border-radius: 47% 53% 44% 56% / 48% 55% 45% 52%; transform: rotate(5deg); border-left-color: transparent; border-bottom-color: transparent; }
.grade { position: absolute; inset: 0; display: flex; align-items: center; justify-content: center;
    font-family: 'Caveat', cursive; font-weight: 700; font-size: 74px; line-height: 1; color: var(--pen); }
.grade-of { font-size: 16px; color: var(--muted); }
.remark { font-family: 'Caveat', cursive; font-weight: 700; font-size: 31px; line-height: 1.05; color: var(--pen); margin: 0; }
.range-line { font-size: 15px; font-weight: 500; margin: 8px 0 10px; }

.scale { position: relative; height: 12px; background: #E8EEF8; border-radius: 3px; margin: 8px 0 6px; }
.scale-range { position: absolute; top: 0; bottom: 0; background: rgba(209, 52, 59, .28); border-radius: 3px; }
.scale-pass { position: absolute; top: -4px; bottom: -4px; left: 50%; width: 2px; background: var(--ink); }
.scale-mark { position: absolute; top: -5px; width: 4px; height: 22px; margin-left: -2px; background: var(--pen); border-radius: 2px; }
.scale-labels { display: flex; justify-content: space-between; font-size: 13px; color: var(--muted); }

.sheet h3 { font-size: 15px; font-weight: 700; margin: 18px 0 2px; }
.sheet .note { font-size: 14px; color: var(--muted); margin: 0 0 8px; line-height: 1.4; }
.drivers { list-style: none; margin: 0; padding: 0; min-height: 180px; }
.sr-only { position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0 0 0 0); white-space: nowrap; }
.skip { position: absolute; left: -9999px; }
.skip:focus { left: 12px; top: 12px; z-index: 9999; background: var(--ink); color: #fff; padding: 10px 14px; border-radius: 6px; }
.sheet:focus { outline: 3px solid var(--pen); outline-offset: 4px; }
@media (pointer: coarse) { [data-testid="stCheckbox"] label { min-height: 44px; align-items: center; } }
.drv { display: grid; grid-template-columns: 1fr 74px 40px; align-items: center; gap: 8px; min-height: 30px; font-size: 15px; }
.drv-track { position: relative; height: 10px; }
.drv-track::before { content: ""; position: absolute; left: 50%; top: -3px; bottom: -3px; width: 1px; background: var(--muted); }
.drv-bar { position: absolute; top: 1px; bottom: 1px; border-radius: 2px; }
.drv-bar.up { left: 50%; background: var(--ink); }
.drv-bar.down { right: 50%; background: var(--pen); }
.drv-val { font-weight: 700; text-align: right; font-variant-numeric: tabular-nums; }
.drv-val.down { color: var(--pen); }

.compare { margin-top: 16px; padding: 8px 12px; background: #FFF6BF; border-left: 3px solid var(--ink); font-size: 14px; }

@media (max-width: 900px) {
    div[data-testid="stColumn"]:has(.marking-anchor) { position: static; }
    .page-title { font-size: 32px; }
    .sheet { padding-left: 54px; }
    .sheet::before { left: 34px; }
}
@media (max-width: 600px) {
    .block-container { padding-left: 1rem; padding-right: 1rem; }
    .sheet { padding: 18px 14px 16px 44px; }
    .sheet::before { left: 28px; }
    .drv { grid-template-columns: 1fr 48px 36px; gap: 6px; }
    .grade-wrap { width: 128px; height: 84px; }
    .grade { font-size: 64px; }
}
@media (prefers-reduced-motion: reduce) { * { transition: none !important; } }
</style>
""", unsafe_allow_html=True)


def html(block: str) -> str:
    """Collapse indented HTML so Markdown doesn't treat it as a code block."""
    return " ".join(line.strip() for line in block.splitlines() if line.strip())


@st.cache_resource
def load_pipeline():
    return joblib.load(MODEL_PATH) if MODEL_PATH.exists() else None


pipeline = load_pipeline()
if pipeline is None:
    st.error(f"Model file not found at `{MODEL_PATH}`. Run hyperparameter tuning to create it.")
    st.stop()
FEATURES = list(pipeline.feature_names_in_)

for key, value in DEFAULTS.items():
    st.session_state.setdefault(key, value)


def apply_preset(name: str):
    st.session_state.update({**DEFAULTS, **PRESETS[name]})


def save_comparison():
    st.session_state["baseline"] = st.session_state.get("_last_score")


def clear_comparison():
    st.session_state["baseline"] = None


def section(title: str, sub: str, first: bool = False):
    cls = "sec sec-first" if first else "sec"
    st.markdown(html(f'<div class="{cls}"><h2>{title}</h2><p>{sub}</p></div>'), unsafe_allow_html=True)


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


def predict_with_drivers(feats: dict):
    """Predict once, then re-predict with each factor group set to the typical student."""
    rows = [feats]
    for cols in FACTOR_GROUPS.values():
        rows.append({**feats, **{c: REFERENCE[c] for c in cols}})
    frame = pd.DataFrame(rows).reindex(columns=FEATURES).astype(float)
    preds = np.clip(pipeline.predict(frame), 0, 20)
    base = float(preds[0])
    drivers = {name: base - float(p) for name, p in zip(FACTOR_GROUPS, preds[1:])}
    return base, drivers


# ---------------------------------------------------------------------------
# Page
# ---------------------------------------------------------------------------
st.markdown(html("""
<a class="skip" href="#result">Skip to prediction</a>
<h1 class="page-title">Student Performance Predictor</h1>
<p class="page-lede">Estimates a student's final maths grade out of 20 from study habits and home background,
before any term grades exist. Built for the AIML Internship 2026 capstone at MNNIT Allahabad.</p>
"""), unsafe_allow_html=True)

form_col, result_col = st.columns([3, 2], gap="large")

with form_col:
    st.markdown("**Start from an example**")
    preset_cols = st.columns(len(PRESETS))
    for col, name in zip(preset_cols, PRESETS):
        col.button(name, key=f"preset_{name}", on_click=apply_preset, args=(name,), use_container_width=True)

    section("About the student", "Basic personal details.")
    c1, c2, c3 = st.columns(3)
    c1.slider("Age", 15, 22, key="age")
    c2.selectbox("Sex", ["F", "M"], format_func={"F": "Female", "M": "Male"}.get, key="sex")
    c3.selectbox("Household size", ["GT3", "LE3"], key="famsize",
                 format_func={"GT3": "More than 3 people", "LE3": "3 people or fewer"}.get)

    section("Study habits", "How the student spends time on school.")
    c1, c2 = st.columns(2)
    c1.select_slider("Weekly study time", [1, 2, 3, 4], key="studytime", format_func=STUDY_LABELS.get)
    c2.select_slider("Travel time to school", [1, 2, 3, 4], key="traveltime", format_func=TRAVEL_LABELS.get)
    c3, c4 = st.columns(2)
    c3.slider("Classes failed before", 0, 3, key="failures")
    c4.number_input("Days absent this year", 0, 93, key="absences")
    c4.caption(f"Counted up to {ABSENCE_CAP} days, the most the model was trained on.")
    c5, c6 = st.columns(2)
    c5.selectbox("Reason for choosing this school", list(REASON_LABELS), key="reason", format_func=REASON_LABELS.get)
    c6.write("")
    c6.checkbox("Plans to continue to higher education", key="higher")

    section("Family and home", "Parents, guardians and support at home.")
    c1, c2 = st.columns(2)
    c1.select_slider("Mother's education", [0, 1, 2, 3, 4], key="Medu", format_func=EDU_LABELS.get)
    c2.select_slider("Father's education", [0, 1, 2, 3, 4], key="Fedu", format_func=EDU_LABELS.get)
    c3, c4, c5 = st.columns(3)
    c3.selectbox("Mother's job", list(JOB_LABELS), key="Mjob", format_func=JOB_LABELS.get,
                 help="The model tells health care, civil services and other apart. Teacher and at home count as other.")
    c4.selectbox("Father's job", list(JOB_LABELS), key="Fjob", format_func=JOB_LABELS.get,
                 help="The model tells teacher and other apart. Other jobs count the same.")
    c5.selectbox("Main guardian", ["mother", "father", "other"], key="guardian", format_func=str.capitalize)
    st.slider("Family relationships", 1, 5, key="famrel", help="1 is poor, 5 is excellent")
    c6, c7, c8 = st.columns(3)
    c6.checkbox("Extra help from school", key="schoolsup")
    c7.checkbox("Help from family", key="famsup")
    c8.checkbox("Internet at home", key="internet")

    section("Life outside class", "Free time, health and habits.")
    c1, c2, c3 = st.columns(3)
    c1.slider("Free time after school", 1, 5, key="freetime", help="1 is very little, 5 is a lot")
    c2.slider("Time out with friends", 1, 5, key="goout", help="1 is very little, 5 is a lot")
    c3.slider("Health", 1, 5, key="health", help="1 is very poor, 5 is very good")
    c4, c5 = st.columns(2)
    c4.slider("Alcohol on school days", 1, 5, key="Dalc", help="1 is none, 5 is a lot")
    c5.slider("Alcohol at weekends", 1, 5, key="Walc", help="1 is none, 5 is a lot")
    c6, c7 = st.columns(2)
    c6.checkbox("Takes part in extracurricular activities", key="activities")
    c7.checkbox("In a romantic relationship", key="romantic")

    with st.expander("How accurate is this?"):
        st.markdown(
            f"On the 395 students in the dataset, predictions are typically **{TYPICAL_ERROR:.0f} grade points** off "
            f"(5-fold cross-validation; the model explains about {CV_R2:.0%} of the variation in final grades). "
            "It deliberately ignores earlier term grades so it can flag students before those exist, which makes the task much "
            "harder. Use the estimate to start a conversation about support, not to make a decision about a student."
        )

with result_col:
    score, drivers = predict_with_drivers(features_from_state(st.session_state))
    st.session_state["_last_score"] = score

    shown = int(round(score))
    low, high = max(0, round(score - TYPICAL_ERROR)), min(20, round(score + TYPICAL_ERROR))
    if score < 8:
        remark, line = "Needs support soon", "Well under the pass mark of 10."
    elif score < PASS_MARK:
        remark, line = "Close to the pass mark", "Just under the pass mark of 10."
    elif score < 14:
        remark, line = "On track", "At or above the pass mark of 10."
    else:
        remark, line = "Doing well", "Comfortably above the pass mark of 10."

    ranked = sorted(drivers.items(), key=lambda kv: abs(kv[1]), reverse=True)
    ranked = [kv for kv in ranked if abs(kv[1]) >= 0.05][:6]
    scale = max([abs(v) for _, v in ranked] + [1.0])
    driver_rows = "".join(
        f'<li class="drv"><span>{name}<span class="sr-only"> {"raises" if v > 0 else "lowers"} the grade by {abs(v):.1f} points</span></span>'
        f'<span class="drv-track" aria-hidden="true"><span class="drv-bar {"up" if v > 0 else "down"}" style="width:{abs(v) / scale * 50:.1f}%"></span></span>'
        f'<span class="drv-val {"" if v > 0 else "down"}" aria-hidden="true">{v:+.1f}</span></li>'
        for name, v in ranked
    ) or '<li class="drv"><span>Close to a typical student on every factor.</span></li>'

    baseline = st.session_state.get("baseline")
    compare = ""
    if baseline is not None:
        diff = score - baseline
        word = "higher" if diff > 0.05 else "lower" if diff < -0.05 else "the same"
        amount = "" if word == "the same" else f"{abs(diff):.1f} points "
        compare = f'<div class="compare">Saved estimate: {baseline:.1f}. This one is {amount}{word}.</div>'

    st.markdown(html(f"""
    <span class="marking-anchor"></span>
    <section class="sheet" id="result" tabindex="-1" aria-label="Prediction result">
        <p class="sr-only" role="status">Predicted final grade {shown} out of 20, likely range {low} to {high}. {remark}.</p>
        <p class="sheet-label">Predicted final grade</p>
        <div class="grade-row">
            <div class="grade-wrap" role="img" aria-label="Predicted grade {shown} out of 20">
                <span class="grade">{shown}</span>
            </div>
            <div><span class="grade-of">out of 20</span><p class="remark">{remark}</p></div>
        </div>
        <p class="range-line">Likely range {low} to {high}. {line}</p>
        <div class="scale" aria-hidden="true">
            <span class="scale-range" style="left:{low / 20 * 100:.1f}%; width:{(high - low) / 20 * 100:.1f}%"></span>
            <span class="scale-pass"></span>
            <span class="scale-mark" style="left:{score / 20 * 100:.1f}%"></span>
        </div>
        <div class="scale-labels"><span>0</span><span>10 pass</span><span>20</span></div>
        <h3>What moved this grade</h3>
        <p class="note">Each factor against a typical student in the dataset, in grade points. Factors are tested one at a time.</p>
        <ul class="drivers">{driver_rows}</ul>
        {compare}
    </section>
    """), unsafe_allow_html=True)

    if baseline is None:
        st.button("Save this estimate to compare", on_click=save_comparison)
    else:
        st.button("Clear saved estimate", on_click=clear_comparison)
