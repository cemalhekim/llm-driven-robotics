# store.py

import sqlite3, json, time, threading, os
from datetime import datetime
from pathlib import Path
import json, time, os
from collections import OrderedDict
from observation import Observation, to_dict


def get_stamp():
    return datetime.now().strftime("%Y%m%d%H%M%S")

STAMP = get_stamp()

BASE_DIR = Path(os.getenv("LAB_DIR", "experiment_logs")).resolve()
BASE_DIR.mkdir(parents=True, exist_ok=True)
JSONL_PATH = os.getenv("LAB_JSONL", str(BASE_DIR / f"{STAMP}.jsonl"))

def log_observation(obs: Observation):
    rec = to_dict(obs)
    ordered = OrderedDict()
    ordered["ts"] = time.strftime("%Y.%m.%d.%H.%M.%S", time.localtime())
    ordered["step"] = rec.get("step")
    ordered["feature"] = rec.get("feature")
    ordered["sample"] = rec.get("sample")
    ordered["value"] = rec.get("value")
    ordered["metrics"] = rec.get("metrics")
    ordered["t_start"] = rec.get("t_start")
    ordered["t_end"] = rec.get("t_end")
    ordered["duration_s"] = rec.get("duration_s")
    ordered["meta"] = rec.get("meta")  # meta en sona
    with open(JSONL_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(ordered, ensure_ascii=False) + "\n")