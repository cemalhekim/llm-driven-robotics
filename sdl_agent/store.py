import csv, json, os, time
from datetime import datetime
from pathlib import Path
from collections import OrderedDict
from observation import Observation, to_dict

def get_stamp():
    return datetime.now().strftime("%Y%m%d%H%M%S")

STAMP = get_stamp()
BASE_DIR = Path(os.getenv("LAB_DIR", "experiment_logs")).resolve()
BASE_DIR.mkdir(parents=True, exist_ok=True)

CSV_PATH = os.getenv("LAB_CSV", str(BASE_DIR / f"{STAMP}.csv"))

FEATURE_TO_COL = {
    "OCP": "value_ocp",
    "CA":  "value_ca",
    "CV":  "value_cv",
}

FIELDNAMES = [
    "ts", "step", "feature", "sample",
    "value_ocp", "value_ca", "value_cv",
    "t_start", "t_end", "duration_s",
    "metrics", "meta",
]

def _ensure_header():
    if not os.path.exists(CSV_PATH) or os.path.getsize(CSV_PATH) == 0:
        with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
            csv.DictWriter(f, fieldnames=FIELDNAMES).writeheader()

def log_observation(obs: Observation):
    rec = to_dict(obs)
    ts_str = time.strftime("%Y.%m.%d.%H.%M.%S", time.localtime())
    feature = (rec.get("feature") or "").upper()

    # Initialise empty value columns
    row = {
        "ts": ts_str,
        "step": rec.get("step"),
        "feature": feature,
        "sample": rec.get("sample"),
        "value_ocp": None,
        "value_ca": None,
        "value_cv": None,
        "t_start": rec.get("t_start"),
        "t_end": rec.get("t_end"),
        "duration_s": rec.get("duration_s"),
        "metrics": json.dumps(rec.get("metrics") or {}, ensure_ascii=False),
        "meta": json.dumps(rec.get("meta") or {}, ensure_ascii=False),
    }

    # Route numeric value into the correct column
    col = FEATURE_TO_COL.get(feature)
    if col is not None:
        row[col] = rec.get("value")

    _ensure_header()
    with open(CSV_PATH, "a", newline="", encoding="utf-8") as f:
        csv.DictWriter(f, fieldnames=FIELDNAMES).writerow(row)
