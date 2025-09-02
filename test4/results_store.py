# results_store.py
import sqlite3, json, time, threading, os
from datetime import datetime
from pathlib import Path

STAMP = datetime.now().strftime("%Y%m%d%H%M%S")  # local date+time

BASE_DIR = Path(os.getenv("LAB_DIR", "experiment_logs")).resolve()
DB_DIR   = BASE_DIR / "experiment_logs_db"
DB_DIR.mkdir(parents=True, exist_ok=True)
BASE_DIR.mkdir(parents=True, exist_ok=True)

DB_PATH    = os.getenv("LAB_DB",    str(DB_DIR  / f"{STAMP}.db"))
JSONL_PATH = os.getenv("LAB_JSONL", str(BASE_DIR / f"{STAMP}.jsonl"))

_lock = threading.Lock()
_current_run = None

def _utcnow(): return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

def _prep_fs():
    Path(DB_PATH).parent.mkdir(parents=True, exist_ok=True)
    Path(JSONL_PATH).parent.mkdir(parents=True, exist_ok=True)

def _conn():
    _prep_fs()
    c = sqlite3.connect(DB_PATH, check_same_thread=False)
    c.execute("PRAGMA journal_mode=WAL;")
    c.execute("PRAGMA synchronous=NORMAL;")
    return c

def init():
    with _conn() as c:
        c.executescript("""
        CREATE TABLE IF NOT EXISTS runs(
          run_id TEXT PRIMARY KEY,
          started_at TEXT NOT NULL,
          notes TEXT
        );
        CREATE TABLE IF NOT EXISTS measurements(
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          ts TEXT NOT NULL,
          run_id TEXT,
          sample INTEGER,
          measurement TEXT,
          value REAL,
          meta TEXT
        );
        CREATE INDEX IF NOT EXISTS idx_m ON measurements(measurement,sample,ts);
        """)
init()

def start_run(notes=""):
    global _current_run
    rid = time.strftime("%Y%m%d%H%M%S")
    with _conn() as c:
        c.execute("INSERT INTO runs(run_id,started_at,notes) VALUES(?,?,?)", (rid, _utcnow(), notes))
    _current_run = rid
    return rid

def set_current_run(run_id):  # optional
    global _current_run; _current_run = run_id

def current_run(): return _current_run

def log_measurement(measurement, sample, value, meta=None, run_id=None):
    """Tolerates both 'sample' and 'sample_id' consumers and always appends JSONL."""
    rid = run_id or _current_run or start_run("auto")
    s = int(sample)
    rec = {
        "ts": _utcnow(),
        "run_id": rid,
        "measurement": str(measurement),
        "value": float(value),
        "sample": s,
        "sample_id": s,                 # <-- added alias to avoid KeyError
        "meta": (meta or {})
    }
    with _lock:
        with _conn() as c:
            c.execute(
                "INSERT INTO measurements(ts,run_id,sample,measurement,value,meta) VALUES(?,?,?,?,?,?)",
                (rec["ts"], rec["run_id"], rec["sample"], rec["measurement"], rec["value"], json.dumps(rec["meta"]))
            )
        # JSONL is best-effort; never block DB insert
        try:
            with open(JSONL_PATH, "a", encoding="utf-8") as f:
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        except Exception as e:
            print(f"[warn] JSONL append failed: {e}")
    return rec

def history(sample, measurement, limit=50):
    with _conn() as c:
        cur = c.execute(
            "SELECT ts, run_id, value, meta FROM measurements WHERE sample=? AND measurement=? ORDER BY ts DESC LIMIT ?",
            (int(sample), str(measurement), int(limit))
        )
        return [{"ts": ts, "run_id": rid, "value": val, "meta": json.loads(meta)} for ts, rid, val, meta in cur.fetchall()]