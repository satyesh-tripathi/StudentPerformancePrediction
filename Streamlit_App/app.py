import streamlit as st
import pandas as pd
import numpy as np
import joblib
from pathlib import Path

st.set_page_config(
    page_title="Student Performance Predictor",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------------------------------------------------------------------------
# Design system — CSS
# ---------------------------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Sora:wght@600;700;800&display=swap');

html, body, [class*="css"]  {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

:root {
    --bg: #F7F8FA;
    --surface: #FFFFFF;
    --border: #E4E7EC;
    --text-primary: #101828;
    --text-secondary: #667085;
    --accent: #7C3AED;
    --accent-dark: #2E1065;
    --accent-pink: #DB2777;
    --accent-soft: #F3EEFC;
    --highlight: #FBBF24;
    --success: #12805C;
    --success-bg: #E9F7F1;
    --danger: #B42318;
    --danger-bg: #FDEDED;
    --font-display: 'Sora', 'Inter', sans-serif;
}

.stApp { background-color: var(--bg); }

.block-container {
    padding-top: 0;
    padding-bottom: 3rem;
    max-width: 960px;
}

/* Full-bleed shell wrapping navbar + hero — breaks out of Streamlit's
   centered container so it spans the entire viewport width */
.top-shell {
    position: relative;
    left: 50%;
    right: 50%;
    width: 100vw;
    margin-left: -50vw;
    margin-right: -50vw;
    margin-bottom: 40px;
    overflow: hidden;
    border-radius: 0 0 36px 36px;
    box-shadow: 0 12px 32px rgba(16, 24, 40, 0.18);
}

/* Top navbar */
.navbar {
    background: var(--accent-dark);
}
.navbar-inner {
    max-width: 1100px;
    margin: 0 auto;
    padding: 16px 32px;
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.navbar-brand {
    font-family: var(--font-display);
    font-size: 17px;
    font-weight: 700;
    color: #FFFFFF;
    margin: 0;
    letter-spacing: -0.01em;
}
.navbar-meta {
    font-size: 13px;
    color: #D8C6F5;
    margin: 0;
}

/* Hero */
.hero {
    position: relative;
    overflow: hidden;
    text-align: center;
    background-color: var(--accent-dark);
    background-image:
        radial-gradient(rgba(255, 255, 255, 0.09) 1px, transparent 1px),
        linear-gradient(135deg, var(--accent-dark) 0%, var(--accent) 55%, var(--accent-pink) 100%);
    background-size: 22px 22px, cover;
    background-position: 0 0, center;
}
.hero::before, .hero::after {
    content: "";
    position: absolute;
    border-radius: 50%;
    filter: blur(6px);
    pointer-events: none;
}
.hero::before {
    width: 460px;
    height: 460px;
    top: -220px;
    right: -80px;
    background: radial-gradient(circle, rgba(251, 191, 36, 0.35), transparent 70%);
}
.hero::after {
    width: 380px;
    height: 380px;
    bottom: -200px;
    left: -100px;
    background: radial-gradient(circle, rgba(219, 39, 119, 0.35), transparent 70%);
}
.hero-inner {
    position: relative;
    z-index: 1;
    max-width: 720px;
    margin: 0 auto;
    padding: 56px 32px 60px 32px;
}
.eyebrow {
    display: inline-block;
    padding: 6px 16px;
    margin-bottom: 20px;
    border: 1px solid rgba(255, 255, 255, 0.3);
    border-radius: 999px;
    background: rgba(255, 255, 255, 0.1);
    color: #F3EEFC;
    font-size: 11.5px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.12em;
}
.hero h1 {
    font-family: var(--font-display);
    font-size: 38px;
    font-weight: 800;
    color: #FFFFFF;
    letter-spacing: -0.02em;
    margin: 0 0 14px 0;
}
.hero h1 .highlight {
    color: var(--highlight);
}
.hero p {
    font-size: 14px;
    color: #E9DFFB;
    margin: 4px 0;
}
.hero p.tagline {
    font-size: 13px;
    color: #C6AEF0;
    margin-top: 10px;
}

/* Section cards (st.container(border=True)) */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background: var(--surface);
    border: 1px solid var(--border);
    border-left: 4px solid var(--accent);
    border-radius: 12px;
    padding: 0 8px 12px 8px;
    box-shadow: 0 1px 2px rgba(16, 24, 40, 0.04), 0 1px 3px rgba(16, 24, 40, 0.03);
    transition: box-shadow 0.2s ease, transform 0.2s ease;
}
div[data-testid="stVerticalBlockBorderWrapper"]:hover {
    box-shadow: 0 6px 20px rgba(124, 58, 237, 0.14);
    transform: translateY(-2px);
}

.section-box {
    background: var(--accent-soft);
    margin: 0 -8px 20px -8px;
    padding: 18px 24px;
    border-radius: 8px 12px 0 0;
    border-bottom: 1px solid var(--border);
}
.section-box-row {
    display: flex;
    align-items: flex-start;
    gap: 14px;
}
.step-badge {
    flex: none;
    width: 28px;
    height: 28px;
    border-radius: 8px;
    background: var(--accent-dark);
    color: #FFFFFF;
    font-family: var(--font-display);
    font-weight: 700;
    font-size: 13px;
    display: flex;
    align-items: center;
    justify-content: center;
}
h3.section-title {
    font-family: var(--font-display);
    font-size: 14px;
    font-weight: 700;
    color: var(--accent-dark);
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin: 0 0 4px 0;
}
p.section-sub {
    font-size: 12.5px;
    font-weight: 400;
    color: var(--text-secondary);
    text-transform: none;
    letter-spacing: 0;
    margin: 0;
}

/* Result card header box uses the card's own (larger) padding */
.result-card .section-box {
    margin: -28px -32px 20px -32px;
    padding: 22px 32px;
    border-radius: 12px 12px 0 0;
}

label, .stSlider label, .stSelectbox label, .stNumberInput label, .stCheckbox label {
    font-size: 13px !important;
    font-weight: 500 !important;
    color: var(--text-primary) !important;
}

/* Re-tint Streamlit's default red widget accents to match the theme */
div[data-testid="stSlider"] div[role="slider"] {
    background-color: var(--accent) !important;
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 4px rgba(124, 58, 237, 0.18) !important;
}
div[data-testid="stSlider"] div[data-baseweb="slider"] div[style*="background-color: rgb(255, 75, 75)"] {
    background: var(--accent) !important;
}
div[data-testid="stThumbValue"] { color: var(--accent) !important; font-weight: 600 !important; }
div[data-testid="stTickBar"] { display: none; }

div[data-baseweb="select"] > div {
    background: #1E1240 !important;
    border-color: var(--border) !important;
    border-radius: 10px !important;
}
div[data-testid="stNumberInput"] input {
    background: #1E1240 !important;
    color: #FFFFFF !important;
    border-radius: 10px !important;
}
[data-testid="stCheckbox"] label span[data-baseweb="checkbox"] > div:first-child {
    border-color: var(--accent) !important;
}
[data-testid="stCheckbox"] label span[data-baseweb="checkbox"] > div[data-checked="true"] {
    background-color: var(--accent) !important;
    border-color: var(--accent) !important;
}

.stFormSubmitButton button {
    background: linear-gradient(135deg, var(--accent) 0%, var(--accent-pink) 100%);
    color: white;
    border: none;
    border-radius: 8px;
    padding: 10px 20px;
    font-weight: 600;
    font-size: 14px;
    width: 100%;
    box-shadow: 0 4px 14px rgba(124, 58, 237, 0.35);
    transition: box-shadow 0.15s ease, transform 0.15s ease;
}
.stFormSubmitButton button:hover {
    box-shadow: 0 6px 18px rgba(124, 58, 237, 0.45);
    transform: translateY(-1px);
    color: white;
}

/* Result card */
.result-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 28px 32px;
    margin-top: 24px;
    box-shadow: 0 4px 20px rgba(46, 16, 101, 0.08);
}
.result-top {
    display: flex;
    align-items: baseline;
    justify-content: space-between;
    margin-bottom: 18px;
}
.result-score {
    font-family: var(--font-display);
    font-size: 42px;
    font-weight: 800;
    color: var(--text-primary);
    letter-spacing: -0.02em;
}
.result-score span { font-size: 16px; font-weight: 500; color: var(--text-secondary); }
.badge {
    display: inline-block;
    padding: 5px 12px;
    border-radius: 999px;
    font-size: 12px;
    font-weight: 600;
}
.badge-pass { background: var(--success-bg); color: var(--success); }
.badge-warn { background: var(--danger-bg); color: var(--danger); }

.bar-track {
    width: 100%;
    height: 10px;
    background: #EEF1F5;
    border-radius: 999px;
    overflow: hidden;
    margin-top: 6px;
}
.bar-fill { height: 100%; border-radius: 999px; }
.bar-labels {
    display: flex;
    justify-content: space-between;
    font-size: 11px;
    color: var(--text-secondary);
    margin-top: 6px;
}
.result-note {
    font-size: 13px;
    color: var(--text-secondary);
    margin-top: 16px;
    line-height: 1.5;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Navbar + Hero
# ---------------------------------------------------------------------------
st.markdown("""
<div class="top-shell">
    <div class="navbar">
        <div class="navbar-inner">
            <p class="navbar-brand">Student Performance Predictor</p>
            <p class="navbar-meta">AIML Internship 2026 | MNNIT Allahabad</p>
        </div>
    </div>
    <div class="hero">
        <div class="hero-inner">
            <span class="eyebrow">Machine Learning · Academic Analytics</span>
            <h1>Student <span class="highlight">Performance</span> Prediction System</h1>
            <p>Capstone Project 1 | MNNIT Allahabad, Prayagraj</p>
            <p class="tagline">Fill in the student details below to predict academic performance</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Model loading
# ---------------------------------------------------------------------------
@st.cache_resource
def load_pipeline():
    p = Path("Model/student_performance_best_model.pkl")
    return joblib.load(p) if p.exists() else None

pipeline = load_pipeline()
if pipeline is None:
    st.error("Model file not found. Run hyperparameter tuning first to generate `Model/student_performance_best_model.pkl`.")
    st.stop()

# ---------------------------------------------------------------------------
# Input form
# ---------------------------------------------------------------------------
with st.form("input_form"):

    with st.container(border=True):
        st.markdown('<div class="section-box"><div class="section-box-row"><span class="step-badge">1</span><div><h3 class="section-title">Demographics</h3><p class="section-sub">Basic personal details about the student</p></div></div></div>', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        age = c1.slider("Age", 15, 22, 17)
        sex = c2.selectbox("Sex", ["M", "F"])
        famsize = c3.selectbox("Family size", ["GT3", "LE3"], help="GT3 = greater than 3 members, LE3 = 3 or fewer")

    st.write("")

    with st.container(border=True):
        st.markdown('<div class="section-box"><div class="section-box-row"><span class="step-badge">2</span><div><h3 class="section-title">Academic History</h3><p class="section-sub">Study habits, past performance, and school-related factors</p></div></div></div>', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        studytime = c1.slider("Weekly study time", 1, 4, 2, help="1 = under 2h, 2 = 2–5h, 3 = 5–10h, 4 = over 10h")
        failures = c2.slider("Past class failures", 0, 3, 0)
        traveltime = c3.slider("Home-to-school travel time", 1, 4, 1, help="1 = under 15min, 4 = over 1h")
        c4, c5 = st.columns(2)
        absences = c4.number_input("Absences (school days)", min_value=0, max_value=93, value=4)
        c4.caption("Values above 20 are capped before scoring for model stability.")
        higher = c5.checkbox("Wants to pursue higher education", value=True)

    st.write("")

    with st.container(border=True):
        st.markdown('<div class="section-box"><div class="section-box-row"><span class="step-badge">3</span><div><h3 class="section-title">Family Background</h3><p class="section-sub">Parental education, jobs, and home environment</p></div></div></div>', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        Medu = c1.slider("Mother's education", 0, 4, 2, help="0 = none, 4 = higher education")
        Fedu = c2.slider("Father's education", 0, 4, 2, help="0 = none, 4 = higher education")
        famrel = c3.slider("Family relationship quality", 1, 5, 4)
        c4, c5, c6 = st.columns(3)
        Mjob = c4.selectbox("Mother's job", ["other", "health", "services", "teacher", "at_home"])
        Fjob = c5.selectbox("Father's job", ["other", "health", "services", "teacher", "at_home"])
        guardian = c6.selectbox("Guardian", ["mother", "father", "other"])
        c7, c8 = st.columns(2)
        schoolsup = c7.checkbox("Receives school support")
        famsup = c8.checkbox("Receives family support")

    st.write("")

    with st.container(border=True):
        st.markdown('<div class="section-box"><div class="section-box-row"><span class="step-badge">4</span><div><h3 class="section-title">Lifestyle &amp; Wellbeing</h3><p class="section-sub">Free time, social habits, and health</p></div></div></div>', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        freetime = c1.slider("Free time after school", 1, 5, 3)
        goout = c2.slider("Going out with friends", 1, 5, 3)
        health = c3.slider("Current health status", 1, 5, 3)
        c4, c5 = st.columns(2)
        Dalc = c4.slider("Weekday alcohol consumption", 1, 5, 1)
        Walc = c5.slider("Weekend alcohol consumption", 1, 5, 1)
        c7, c8 = st.columns(2)
        activities = c7.checkbox("Extracurricular activities")
        romantic = c8.checkbox("In a romantic relationship")

    st.write("")
    submit = st.form_submit_button("Predict outcome")

# ---------------------------------------------------------------------------
# Prediction
# ---------------------------------------------------------------------------
if submit:
    feat_dict = {
        'age': age, 'traveltime': traveltime, 'studytime': studytime, 'failures': failures,
        'famrel': famrel, 'freetime': freetime, 'goout': goout, 'Dalc': Dalc, 'Walc': Walc, 'health': health,
        'absences': min(absences, 20),
        'schoolsup': 1 if schoolsup else 0, 'famsup': 1 if famsup else 0,
        'activities': 1 if activities else 0, 'higher': 1 if higher else 0,
        'romantic': 1 if romantic else 0,
        'sex_F': 1 if sex == 'F' else 0, 'famsize_GT3': 1 if famsize == 'GT3' else 0,
        'Mjob_health': 1 if Mjob == 'health' else 0, 'Mjob_other': 1 if Mjob == 'other' else 0,
        'Mjob_services': 1 if Mjob == 'services' else 0,
        'Fjob_other': 1 if Fjob == 'other' else 0,
        'Fjob_teacher': 1 if Fjob == 'teacher' else 0,  # fixed: was hardcoded to 0 regardless of selection
        'reason_reputation': 0,  # "reason for choosing school" removed from the UI
        'guardian_mother': 1 if guardian == 'mother' else 0, 'guardian_other': 1 if guardian == 'other' else 0,
        'parental_edu_avg': (Medu + Fedu) / 2.0,
    }

    cols_expected = pipeline.named_steps['scaler'].feature_names_in_
    input_df = pd.DataFrame([feat_dict]).reindex(columns=cols_expected, fill_value=0)

    raw_pred = pipeline.predict(input_df)[0]
    final_score = float(np.clip(raw_pred, 0, 20))
    pct = final_score / 20 * 100
    passed = final_score >= 10

    badge_class = "badge-pass" if passed else "badge-warn"
    badge_text = "Pass threshold met" if passed else "Academic warning zone"
    bar_fill_style = (
        f"background: linear-gradient(90deg, var(--accent), var(--highlight)); width:{pct:.1f}%;"
        if passed else
        f"background: linear-gradient(90deg, #B42318, #F87171); width:{pct:.1f}%;"
    )
    note = (
        "This score sits at or above the pass threshold (10/20) based on the input factors provided."
        if passed else
        "This score falls below the pass threshold (10/20). Study time, absences, and support factors "
        "are the inputs most likely to move it."
    )

    st.markdown(f"""
    <div class="result-card">
        <div class="section-box">
            <h3 class="section-title">Prediction Result</h3>
            <p class="section-sub">Model output based on the details you provided</p>
        </div>
        <div class="result-top">
            <div class="result-score">{final_score:.1f} <span>/ 20</span></div>
            <div class="badge {badge_class}">{badge_text}</div>
        </div>
        <div class="bar-track">
            <div class="bar-fill" style="{bar_fill_style}"></div>
        </div>
        <div class="bar-labels"><span>0</span><span>10 (pass)</span><span>20</span></div>
        <div class="result-note">{note}</div>
    </div>
    """, unsafe_allow_html=True)
