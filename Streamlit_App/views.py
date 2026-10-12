"""The three screens: welcome, questions, results."""
import streamlit as st

from levers import MAX_GAIN, best_moves, has_applicable
from model_io import (
    ABSENCE_CAP, DATASET_SIZE, DEFAULTS, EDU_LABELS, JOB_LABELS, PASS_MARK, PRESETS,
    REASON_LABELS, STUDENT_FACTORS, STUDY_LABELS, TRAVEL_LABELS, TYPICAL_ERROR, CV_R2,
    features_from_state, predict_rows, predict_with_drivers,
)
from theme import beam, html

SKIPPED_NOTE = "You skipped some questions, so the typical value for each was used instead."


# ---------------------------------------------------------------------------
# Navigation
# ---------------------------------------------------------------------------
def go(stage: str, step: int = 0):
    st.session_state["stage"] = stage
    st.session_state["step"] = step
    if stage == "results":
        st.session_state["play_study"] = st.session_state["studytime"]
        st.session_state["play_dalc"] = st.session_state["Dalc"]


def use_example(name: str):
    st.session_state.update({**DEFAULTS, **PRESETS[name]})
    st.session_state["skipped"] = False
    go("results")


def skip_rest(from_step: int):
    for step in STEPS[from_step:]:
        for key in step["keys"]:
            st.session_state[key] = DEFAULTS[key]
    st.session_state["skipped"] = True
    go("results")


def start_over():
    st.session_state.update(DEFAULTS)
    st.session_state["skipped"] = False
    go("welcome")


# ---------------------------------------------------------------------------
# Question steps (one or two ideas per screen; the sensitive ones come last)
# ---------------------------------------------------------------------------
def q_study():
    st.select_slider("How much do you study each week?", [1, 2, 3, 4], key="studytime", format_func=STUDY_LABELS.get)
    st.slider("Classes you have failed in the past", 0, 3, key="failures")


def q_school_days():
    st.number_input("School days you missed this year", 0, 93, key="absences")
    st.caption(f"Counted up to {ABSENCE_CAP} days, the most the model learned from.")
    st.checkbox("I plan to continue to higher education", key="higher")


def q_about_you():
    c1, c2 = st.columns(2)
    c1.slider("Your age", 15, 22, key="age")
    c2.selectbox("Sex", ["F", "M"], format_func={"F": "Female", "M": "Male"}.get, key="sex")
    st.select_slider("How long is your trip to school?", [1, 2, 3, 4], key="traveltime", format_func=TRAVEL_LABELS.get)


def q_support():
    st.selectbox("Why did you choose your school?", list(REASON_LABELS), key="reason", format_func=REASON_LABELS.get)
    st.checkbox("My school gives me extra help", key="schoolsup")
    st.checkbox("My family helps with my studies", key="famsup")
    st.checkbox("I have internet at home", key="internet")


def q_outside():
    c1, c2 = st.columns(2)
    c1.slider("Free time after school", 1, 5, key="freetime", help="1 is very little, 5 is a lot")
    c2.slider("Time out with friends", 1, 5, key="goout", help="1 is very little, 5 is a lot")
    st.slider("How is your health?", 1, 5, key="health", help="1 is very poor, 5 is very good")
    st.checkbox("I take part in activities outside class", key="activities")


def q_home():
    c1, c2 = st.columns(2)
    c1.select_slider("Your mother's education", [0, 1, 2, 3, 4], key="Medu", format_func=EDU_LABELS.get)
    c2.select_slider("Your father's education", [0, 1, 2, 3, 4], key="Fedu", format_func=EDU_LABELS.get)
    c3, c4 = st.columns(2)
    c3.selectbox("Who looks after you most?", ["mother", "father", "other"], key="guardian", format_func=str.capitalize)
    c4.selectbox("Your household", ["GT3", "LE3"], key="famsize",
                 format_func={"GT3": "More than 3 people", "LE3": "3 people or fewer"}.get)


def q_parents():
    c1, c2 = st.columns(2)
    c1.selectbox("Your mother's job", list(JOB_LABELS), key="Mjob", format_func=JOB_LABELS.get)
    c2.selectbox("Your father's job", list(JOB_LABELS), key="Fjob", format_func=JOB_LABELS.get)
    st.slider("How are things at home?", 1, 5, key="famrel", help="1 is very difficult, 5 is excellent")


def q_life():
    c1, c2 = st.columns(2)
    c1.slider("Drinking on school days", 1, 5, key="Dalc", help="1 is none, 5 is a lot")
    c2.slider("Drinking at weekends", 1, 5, key="Walc", help="1 is none, 5 is a lot")
    st.checkbox("I'm in a relationship", key="romantic")


STEPS = [
    dict(chapter="Your study life", title="How do you study?", sub="Answer honestly. The result is only useful if it's true.",
         render=q_study, keys=["studytime", "failures"]),
    dict(chapter="Your study life", title="Showing up and aiming ahead", sub="Missed days and future plans both matter.",
         render=q_school_days, keys=["absences", "higher"]),
    dict(chapter="Your school days", title="A little about you", sub="Just the basics.",
         render=q_about_you, keys=["age", "sex", "traveltime"]),
    dict(chapter="Your school days", title="Your school and support", sub="Who and what helps you along.",
         render=q_support, keys=["reason", "schoolsup", "famsup", "internet"]),
    dict(chapter="Outside class", title="Life outside class", sub="Time, friends, and how you're feeling.",
         render=q_outside, keys=["freetime", "goout", "health", "activities"]),
    dict(chapter="Home and life", title="Your home", sub="These are optional. Skip any time and typical values are used.",
         render=q_home, keys=["Medu", "Fedu", "guardian", "famsize"]),
    dict(chapter="Home and life", title="Your family", sub="Also optional.",
         render=q_parents, keys=["Mjob", "Fjob", "famrel"]),
    dict(chapter="Home and life", title="The personal bit", sub="Last one, and optional. Nothing is saved or shared.",
         render=q_life, keys=["Dalc", "Walc", "romantic"]),
]
FIRST_OPTIONAL = 5


# ---------------------------------------------------------------------------
# Welcome
# ---------------------------------------------------------------------------
def welcome():
    st.markdown(beam(0.45), unsafe_allow_html=True)
    st.markdown(html(f"""
        <p class="brand">Student Performance Predictor</p>
        <div id="main" tabindex="-1"><h1 class="hero-title">Where is your term heading?</h1></div>
        <p class="lede">Answer a few questions about how you study and live. Get a likely grade range, and the
        habits that could move it.</p>
        <ul class="promises">
            <li>Takes about two minutes</li>
            <li>Nothing you enter is saved</li>
            <li>Built from the records of {DATASET_SIZE} real students</li>
        </ul>
    """), unsafe_allow_html=True)
    st.button("Start", type="primary", key="start", on_click=go, args=("questions", 0))
    st.markdown('<p class="small-note">Want to see how it works first? Try an example.</p>', unsafe_allow_html=True)
    cols = st.columns(len(PRESETS))
    for col, name in zip(cols, PRESETS):
        col.button(name, key=f"ex_{name}", on_click=use_example, args=(name,), use_container_width=True)


# ---------------------------------------------------------------------------
# Questions
# ---------------------------------------------------------------------------
def questions():
    step = st.session_state["step"]
    info = STEPS[step]
    st.markdown(beam(0.25 + 0.55 * (step + 1) / len(STEPS)), unsafe_allow_html=True)
    dots = "".join(
        f'<li class="{"done" if i < step else "now" if i == step else ""}"></li>' for i in range(len(STEPS))
    )
    st.markdown(html(f"""
        <p class="brand">Student Performance Predictor</p>
        <ol class="dots" role="img" aria-label="Question {step + 1} of {len(STEPS)}">{dots}</ol>
        <p class="chapter">{info["chapter"]}</p>
        <div id="main" tabindex="-1"><h2 class="q-title">{info["title"]}</h2></div>
        <p class="q-sub">{info["sub"]}</p>
    """), unsafe_allow_html=True)

    info["render"]()

    st.write("")
    back, nxt, _ = st.columns([1, 1.4, 2])
    back.button("Back", key="back", on_click=go,
                args=("welcome", 0) if step == 0 else ("questions", step - 1))
    last = step == len(STEPS) - 1
    nxt.button("See my result" if last else "Next", type="primary", key="next", on_click=go,
               args=("results", 0) if last else ("questions", step + 1))
    if step >= FIRST_OPTIONAL:
        st.button("Skip the rest", key="skip", type="tertiary", on_click=skip_rest, args=(step,))


# ---------------------------------------------------------------------------
# Results
# ---------------------------------------------------------------------------
def band_line(score: float) -> str:
    if score < 8:
        return "There's real room to move this up."
    if score < PASS_MARK:
        return "You're close to the pass mark, and a small push could tip it."
    if score < 14:
        return "You're on a steady track. Keep what's working."
    return "You're in a strong position. Protect your routine."


def range_for(score: float):
    return max(0, round(score - TYPICAL_ERROR)), min(20, round(score + TYPICAL_ERROR))


def move_text(key: str, feats: dict) -> str:
    if key == "studytime":
        cur = int(feats["studytime"])
        return f"Aim to study {STUDY_LABELS[cur + 1].lower()} a week, up from {STUDY_LABELS[cur].lower()}"
    return "Cut back on drinking on school days"


def summary_file(score, low, high, moves, joint) -> str:
    lines = "".join(f"<li>{move_text(k, feats_cache())} (about +{g:.1f} points)</li>" for k, g in moves) or \
        "<li>Your study and weekday habits already look like the ones linked with better grades.</li>"
    return (
        "<!doctype html><meta charset='utf-8'><title>My grade estimate</title>"
        "<body style='font-family:Georgia,serif;max-width:560px;margin:40px auto;color:#17313A;line-height:1.5'>"
        f"<h1>My likely final grade: {low} to {high} out of 20</h1><p>Most likely around {score:.0f}.</p>"
        f"<h2>Habits worth changing</h2><ul>{lines}</ul>"
        f"<p style='color:#4B6169;font-size:14px'>An estimate from patterns in {DATASET_SIZE} students, typically about "
        f"{TYPICAL_ERROR:.0f} points off. Not a guarantee.</p></body>"
    )


def feats_cache() -> dict:
    return features_from_state(st.session_state)


def results():
    feats = features_from_state(st.session_state)
    score, drivers = predict_with_drivers(feats)
    low, high = range_for(score)
    shown = int(round(score))
    st.markdown(beam(score / 20), unsafe_allow_html=True)

    st.markdown(html(f"""
        <p class="brand">Student Performance Predictor</p>
        <div class="result-hero">
            <p class="sr-only" role="status">Your likely final grade is {low} to {high} out of 20, most likely around {shown}.</p>
            <p class="result-label" id="main" tabindex="-1">Your likely final grade</p>
            <div class="big-num" aria-hidden="true">{shown}<span class="big-of">out of 20</span></div>
            <p class="range-line">Most likely between {low} and {high}</p>
            <p class="band-line">{band_line(score)}</p>
            <div class="scale" aria-hidden="true">
                <span class="scale-range" style="left:{low / 20 * 100:.1f}%; width:{(high - low) / 20 * 100:.1f}%"></span>
                <span class="scale-pass"></span>
                <span class="scale-mark" style="left:{score / 20 * 100:.1f}%"></span>
            </div>
            <div class="scale-labels" aria-hidden="true"><span>0</span><span>10 is a pass</span><span>20</span></div>
        </div>
    """), unsafe_allow_html=True)

    if st.session_state.get("skipped"):
        st.caption(SKIPPED_NOTE)

    # --- Habits worth changing -------------------------------------------------
    moves, joint = best_moves(feats)
    st.markdown('<h3 class="sec-title">Habits worth changing</h3>', unsafe_allow_html=True)
    if moves:
        rows = "".join(
            f'<div class="move"><span class="move-text">{move_text(k, feats)}</span>'
            f'<span class="move-gain" aria-label="about {g:.1f} points more">+{g:.1f}</span></div>'
            for k, g in moves
        )
        st.markdown(html(f"""
            <p class="sec-note">Students with a similar profile who made these changes tended to score a little higher.
            These are patterns, not promises.</p>{rows}
        """), unsafe_allow_html=True)
        if len(moves) > 1:
            st.caption(f"Both together: up to about +{min(joint, MAX_GAIN):.1f} points.")
    elif has_applicable(feats):
        st.markdown(html("""
            <div class="calm-box">The data doesn't show a clear grade gain from changing your study time or school-day
            drinking. Grades depend on a lot a model can't see, like how you learn and the help you get. If a subject feels
            hard, a teacher or someone you trust is a better next step than a number.</div>
        """), unsafe_allow_html=True)
    else:
        st.markdown(html("""
            <div class="calm-box">You're already in the top study band with no school-day drinking, the two habits the
            data links most reliably with better grades. Keep your routine steady.</div>
        """), unsafe_allow_html=True)

    # --- What shaped it --------------------------------------------------------
    shaped = sorted(((n, drivers[n]) for n in STUDENT_FACTORS), key=lambda kv: abs(kv[1]), reverse=True)
    shaped = [kv for kv in shaped if abs(kv[1]) >= 0.1][:4]
    st.markdown('<h3 class="sec-title">What shaped your estimate</h3>', unsafe_allow_html=True)
    if shaped:
        scale = max([abs(v) for _, v in shaped] + [1.0])
        rows = "".join(
            f'<li class="factor"><span>{n}<span class="sr-only"> {"lifts" if v > 0 else "holds back"} your estimate by {abs(v):.1f} points</span></span>'
            f'<span class="factor-track" aria-hidden="true"><span class="factor-bar {"up" if v > 0 else "down"}" style="width:{abs(v) / scale * 50:.1f}%"></span></span>'
            f'<span class="factor-val {"up" if v > 0 else "down"}" aria-hidden="true">{v:+.1f}</span></li>'
            for n, v in shaped
        )
        st.markdown(html(f"""
            <p class="sec-note">Compared with a typical student in the data. Teal lifts your estimate, amber holds it back.</p>
            <ul class="factors">{rows}</ul>
        """), unsafe_allow_html=True)
    else:
        st.markdown('<p class="sec-note">You look close to a typical student on every one of these.</p>', unsafe_allow_html=True)

    # --- Try it ----------------------------------------------------------------
    st.markdown('<h3 class="sec-title">Try a different week</h3>', unsafe_allow_html=True)
    st.markdown('<p class="sec-note">Move these and see how your range responds.</p>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    play_study = c1.select_slider("Weekly study time", [1, 2, 3, 4], key="play_study", format_func=STUDY_LABELS.get)
    play_dalc = c2.slider("Drinking on school days", 1, 5, key="play_dalc", help="1 is none, 5 is a lot")
    new_score = float(predict_rows([{**feats, "studytime": play_study, "Dalc": play_dalc}])[0])
    nl, nh = range_for(new_score)
    delta = new_score - score
    if abs(delta) < 0.3:
        change = "That barely changes your estimate."
    else:
        change = f"That moves your estimate by about {delta:+.1f} points."
    st.markdown(f'<p class="try-out">New range: <b>{nl} to {nh}</b>. {change}</p>', unsafe_allow_html=True)

    # --- Take it with you ------------------------------------------------------
    st.write("")
    left, right = st.columns(2)
    left.download_button("Download my summary", data=summary_file(score, low, high, moves, joint),
                         file_name="my-grade-estimate.html", mime="text/html", use_container_width=True)
    right.button("Change my answers", key="change", on_click=go, args=("questions", 0), use_container_width=True)
    st.button("Start over", key="over", type="tertiary", on_click=start_over)

    st.markdown(html(f"""
        <p class="fine-print">This is an estimate from patterns in {DATASET_SIZE} students' school records. It's typically about
        {TYPICAL_ERROR:.0f} grade points off, and it explains roughly {CV_R2:.0%} of the differences between students. It deliberately
        ignores earlier term grades, so it can be used before they exist. It can't know your teachers, your effort this week or
        your plans. Use it as a prompt to think, not a prediction you have to live up to or down to.</p>
    """), unsafe_allow_html=True)
