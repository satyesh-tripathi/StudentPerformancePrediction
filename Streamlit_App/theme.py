"""Calm morning-light theme for the student-facing app."""

FONTS = (
    "@import url('https://fonts.googleapis.com/css2?family=Hanken+Grotesk:wght@400;500;600;700"
    "&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;0,6..72,600;1,6..72,400&display=swap');"
)

CSS = FONTS + """
:root {
    --mist: #EDF1F0;
    --fog: #DDE6E4;
    --ink: #17313A;
    --slate: #4B6169;
    --leaf: #1F6F6B;
    --sun: #F0B45A;
    --amber-ink: #8A5A12;
    --beam: 0.5;
}

.stApp { background: var(--mist); color: var(--ink); }
.stApp, .stApp p, .stApp label, .stApp button, .stApp input, .stApp [data-baseweb="select"],
.stApp [data-testid="stWidgetLabel"] { font-family: 'Hanken Grotesk', system-ui, sans-serif; }

/* The beam: a soft shaft of morning light that grows with your progress and your result */
.stApp::before {
    content: ""; position: fixed; inset: -20% -15%; z-index: 0; pointer-events: none;
    background: linear-gradient(115deg, transparent 16%,
        rgba(240, 180, 90, calc(0.07 + 0.22 * var(--beam))) 34%,
        rgba(240, 180, 90, calc(0.03 + 0.09 * var(--beam))) 52%, transparent 68%);
    animation: drift 70s ease-in-out infinite alternate;
}
@keyframes drift { from { transform: translateX(-4%); } to { transform: translateX(4%); } }
[data-testid="stMain"] { position: relative; z-index: 1; }
header[data-testid="stHeader"] { background: transparent; }
.block-container { max-width: 760px; padding: 3.2rem 1.5rem 5rem; }

/* Type */
.brand { font-size: 16px; font-weight: 600; color: var(--slate); margin: 0 0 56px; letter-spacing: 0.01em; }
h1.hero-title, h2.q-title, .big-num, .serif { font-family: 'Newsreader', Georgia, serif; }
h1.hero-title { font-size: clamp(34px, 3.9vw, 52px); font-weight: 500; line-height: 1.04; letter-spacing: -0.025em; margin: 0 0 18px; padding: 0; }
h1.hero-title .ln { display: block; }
h1.hero-title > span:not(:first-child) { display: none; }  /* Streamlit's heading link icon */
.hero-tagline { font-family: 'Newsreader', Georgia, serif; font-style: italic; font-size: clamp(22px, 2.4vw, 28px); line-height: 1.25; color: var(--leaf); margin: 0 0 16px; }
#main:focus { outline: none; }
.lede { font-size: 18px; line-height: 1.55; color: var(--slate); max-width: 40ch; margin: 0 0 22px; }
.promises { list-style: none; margin: 0 0 30px; padding: 0; display: grid; gap: 8px; font-size: 16px; color: var(--ink); }
.promises li::before { content: ""; display: inline-block; width: 8px; height: 8px; border-radius: 50%; background: var(--sun); margin-right: 12px; }
.small-note { font-size: 15px; color: var(--slate); margin: 34px 0 8px; }

/* Question screens */
.chapter { font-size: 16px; font-weight: 600; color: var(--leaf); margin: 0 0 6px; }
h2.q-title { font-size: clamp(32px, 5vw, 44px); font-weight: 500; line-height: 1.1; letter-spacing: -0.015em; margin: 0 0 10px; padding: 0; }
.q-sub { font-size: 18px; line-height: 1.5; color: var(--slate); margin: 0 0 28px; max-width: 48ch; }
[data-testid="stMarkdownContainer"] ol.dots { display: flex !important; flex-direction: row; gap: 8px; list-style: none; margin: 0 0 40px; padding: 0; }
[data-testid="stMarkdownContainer"] ol.dots li { display: block; width: 28px; height: 5px; margin: 0; padding: 0; border-radius: 3px; background: var(--fog); }
[data-testid="stMarkdownContainer"] ol.dots li.done { background: var(--leaf); }
[data-testid="stMarkdownContainer"] ol.dots li.now { background: var(--sun); }
.sr-only { position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0 0 0 0); white-space: nowrap; }
.skip { position: absolute; left: -9999px; }
.skip:focus { left: 12px; top: 12px; z-index: 9999; background: var(--ink); color: #fff; padding: 10px 14px; border-radius: 8px; }

.stApp label, [data-testid="stWidgetLabel"] p { font-size: 17px; font-weight: 500; color: var(--ink); }
[data-testid="stCaptionContainer"] p, .stApp small { font-size: 15px; color: var(--slate); }
div[data-baseweb="select"] > div, [data-testid="stNumberInput"] input { background: #F8FAF9; border-radius: 10px; }

/* Buttons */
.stButton > button, [data-testid="stDownloadButton"] button {
    min-height: 48px; border-radius: 12px; font-size: 16px; font-weight: 600; padding: 8px 22px;
    transition: background-color .15s ease, color .15s ease, border-color .15s ease;
}
button[data-testid="stBaseButton-primary"] { background: var(--leaf); color: #fff; border: 1.5px solid var(--leaf); min-height: 52px; padding: 8px 32px; }
button[data-testid="stBaseButton-primary"]:hover { background: #17595A; border-color: #17595A; color: #fff; }
button[data-testid="stBaseButton-secondary"], [data-testid="stDownloadButton"] button { background: transparent; color: var(--ink); border: 1.5px solid var(--slate); }
button[data-testid="stBaseButton-secondary"]:hover, [data-testid="stDownloadButton"] button:hover { background: var(--fog); color: var(--ink); border-color: var(--ink); }
.stButton > button:focus-visible, [data-testid="stDownloadButton"] button:focus-visible { outline: 3px solid var(--sun); outline-offset: 3px; }
button[data-testid="stBaseButton-tertiary"] { color: var(--slate); text-decoration: underline; min-height: 44px; padding-left: 0; justify-content: flex-start; }

[data-testid="stMarkdownContainer"] ul.promises, [data-testid="stMarkdownContainer"] ul.factors { padding-left: 0; margin-left: 0; width: 100%; }
[data-testid="stMarkdownContainer"] ul.promises li, [data-testid="stMarkdownContainer"] ul.factors li { padding-left: 0; margin-left: 0; }

/* Welcome: example result card */
.preview-card { background: rgba(255, 255, 255, .72); border: 1.5px solid var(--fog); border-radius: 22px; padding: 28px 30px 24px; box-shadow: 0 28px 60px -30px rgba(23, 49, 58, .35); }
.preview-tag { font-size: 15px; color: var(--slate); margin: 0 0 14px; }
.preview-num { font-family: 'Newsreader', Georgia, serif; font-size: 92px; font-weight: 400; line-height: 1; letter-spacing: -0.03em; color: var(--ink); }
.preview-card .range-line { font-size: 19px; margin: 6px 0 14px; }
.preview-card .move, .preview-card .move:last-of-type { margin-top: 14px; padding: 14px 0 0; border-bottom: 0; }
.preview-card .move-text { font-size: 17px; }
.preview-card .move-gain { font-size: 26px; }

.move-text, .band-line, .range-line { text-wrap: balance; }

/* Results */
.result-hero { margin: 0 0 8px; }
.result-label { font-size: 17px; color: var(--slate); margin: 0 0 16px; }
.big-num { font-size: clamp(88px, 22vw, 150px); font-weight: 400; line-height: 0.95; letter-spacing: -0.03em; color: var(--ink); }
.big-of { font-size: 22px; color: var(--slate); margin-left: 10px; font-family: 'Hanken Grotesk', sans-serif; letter-spacing: 0; }
.range-line { font-size: 22px; font-weight: 500; margin: 6px 0 4px; }
.band-line { font-size: 19px; line-height: 1.5; color: var(--slate); max-width: 46ch; margin: 0 0 22px; }
.scale { position: relative; height: 10px; background: var(--fog); border-radius: 5px; margin: 10px 0 6px; }
.scale-range { position: absolute; top: 0; bottom: 0; background: rgba(31, 111, 107, .38); border-radius: 5px; }
.scale-pass { position: absolute; top: -5px; bottom: -5px; left: 50%; width: 2px; background: var(--slate); }
.scale-mark { position: absolute; top: -6px; width: 22px; height: 22px; margin-left: -11px; background: var(--sun); border: 3px solid var(--ink); border-radius: 50%; }
.scale-labels { display: flex; justify-content: space-between; font-size: 14px; color: var(--slate); }

h3.sec-title { font-family: 'Newsreader', Georgia, serif; font-size: 30px; font-weight: 500; letter-spacing: -0.01em; margin: 48px 0 6px; padding: 0; }
.sec-note { font-size: 16px; color: var(--slate); margin: 0 0 16px; max-width: 54ch; line-height: 1.5; }
.move { display: flex; align-items: baseline; justify-content: space-between; gap: 18px; padding: 16px 0; border-top: 1.5px solid var(--fog); }
.move:last-of-type { border-bottom: 1.5px solid var(--fog); }
.move-text { font-size: 19px; line-height: 1.4; }
.move-gain { font-family: 'Newsreader', Georgia, serif; font-size: 30px; color: var(--leaf); white-space: nowrap; }
.calm-box { background: rgba(255, 255, 255, .55); border-left: 4px solid var(--sun); padding: 16px 20px; font-size: 18px; line-height: 1.5; border-radius: 0 10px 10px 0; }
.factors { list-style: none; margin: 0; padding: 0; }
.factor { display: grid; grid-template-columns: 1fr 100px 52px; align-items: center; gap: 10px; min-height: 44px; font-size: 17px; border-top: 1.5px solid var(--fog); }
.factor-track { position: relative; height: 10px; }
.factor-track::before { content: ""; position: absolute; left: 50%; top: -4px; bottom: -4px; width: 1px; background: var(--slate); }
.factor-bar { position: absolute; top: 1px; bottom: 1px; border-radius: 3px; }
.factor-bar.up { left: 50%; background: var(--leaf); }
.factor-bar.down { right: 50%; background: var(--amber-ink); }
.factor-val { font-weight: 700; text-align: right; font-variant-numeric: tabular-nums; }
.factor-val.down { color: var(--amber-ink); }
.factor-val.up { color: var(--leaf); }
.try-out { font-size: 20px; line-height: 1.5; padding: 14px 0 4px; }
.fine-print { font-size: 15px; line-height: 1.55; color: var(--slate); margin-top: 52px; max-width: 60ch; border-top: 1.5px solid var(--fog); padding-top: 18px; }

@media (max-width: 600px) {
    .block-container { padding: 2rem 1.1rem 4rem; }
    .brand { margin-bottom: 36px; }
    .factor { grid-template-columns: 1fr 64px 46px; }
    .move { flex-direction: column; gap: 4px; }
}
@media (prefers-reduced-motion: reduce) { .stApp::before { animation: none; } * { transition: none !important; } }
"""


def html(block: str) -> str:
    """Collapse indented HTML so Markdown doesn't treat it as a code block."""
    return " ".join(line.strip() for line in block.splitlines() if line.strip())


def beam(level: float) -> str:
    """Style tag that sets how strong the morning light is (0 to 1)."""
    level = max(0.0, min(1.0, level))
    return f"<style>.stApp {{ --beam: {level:.2f}; }}</style>"
