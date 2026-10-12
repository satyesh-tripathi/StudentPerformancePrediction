"""What-if levers: habits a student controls, and what the model says changing them could do.

The model finds patterns in the dataset; these are associations, not guarantees. Only habits
a student can change are offered. Age, sex, family, parents, past failures, `schoolsup`
(confounded, see D-009), `higher` and `internet` are excluded.

Validated against all 649 students in Dataset/student_mat_features.csv (see decision D-010):
- study time (+1 band) and weekday alcohol (down to 1) give a consistent positive signal.
- absences, going out, weekend alcohol and activities averaged about 0 with mixed signs, so
  they are NOT offered as advice even though they are plausible-sounding habits.
- predicted gains of 2 points or more equal the model's typical error and were seen only as
  tree-model artifacts, so they are hidden.
"""
from dataclasses import dataclass

from model_io import predict_rows

MIN_GAIN = 0.3  # points; smaller predicted gains are not worth showing
MAX_GAIN = 2.0  # points; larger ones are treated as model artifacts
MAX_MOVES = 2


@dataclass(frozen=True)
class Lever:
    key: str
    change: callable  # feats -> dict of changed feature values, or {} if not applicable


def _studytime(f):
    return {"studytime": f["studytime"] + 1} if f["studytime"] < 4 else {}


def _weekday_alcohol(f):
    return {"Dalc": 1} if f["Dalc"] > 1 else {}


LEVERS = [
    Lever("studytime", _studytime),
    Lever("Dalc", _weekday_alcohol),
]


def lever_gains(feats: dict) -> dict:
    """Predicted grade change for each applicable lever, applied one at a time."""
    applicable = {lv.key: lv.change(feats) for lv in LEVERS}
    applicable = {k: v for k, v in applicable.items() if v}
    if not applicable:
        return {}
    preds = predict_rows([feats] + [{**feats, **chg} for chg in applicable.values()])
    return {k: float(p - preds[0]) for k, p in zip(applicable, preds[1:])}


def best_moves(feats: dict):
    """Top moves (key, gain) worth showing, plus the joint gain of making all of them."""
    gains = lever_gains(feats)
    moves = sorted(((k, g) for k, g in gains.items() if MIN_GAIN <= g < MAX_GAIN), key=lambda kv: -kv[1])[:MAX_MOVES]
    if not moves:
        return [], 0.0
    combined = {}
    for key, _ in moves:
        combined.update(next(lv for lv in LEVERS if lv.key == key).change(feats))
    base, after = predict_rows([feats, {**feats, **combined}])
    return moves, float(after - base)


def has_applicable(feats: dict) -> bool:
    """True if the student could still change at least one offered habit."""
    return any(lv.change(feats) for lv in LEVERS)
