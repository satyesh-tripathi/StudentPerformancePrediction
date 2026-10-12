import streamlit as st

from model_io import DEFAULTS, MODEL_PATH, load_pipeline
from theme import CSS
from views import questions, results, welcome

st.set_page_config(page_title="Student Performance Predictor", page_icon=":material/wb_sunny:", layout="centered")
st.markdown(f"<style>{CSS}</style>", unsafe_allow_html=True)
st.markdown('<a class="skip" href="#main">Skip to content</a>', unsafe_allow_html=True)

if load_pipeline() is None:
    st.error(f"Model file not found at `{MODEL_PATH}`. Run hyperparameter tuning to create it.")
    st.stop()

# Answers live in session state. Re-assigning each run keeps answers for widgets that are
# not on screen right now (Streamlit otherwise drops state for unrendered widgets).
for key, value in DEFAULTS.items():
    st.session_state[key] = st.session_state.get(key, value)
for key, value in {"stage": "welcome", "step": 0, "skipped": False}.items():
    st.session_state.setdefault(key, value)
for key, source in {"play_study": "studytime", "play_goout": "goout", "play_dalc": "Dalc"}.items():
    st.session_state[key] = st.session_state.get(key, DEFAULTS[source])

{"welcome": welcome, "questions": questions, "results": results}[st.session_state["stage"]]()
