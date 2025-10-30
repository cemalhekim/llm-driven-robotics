# observation.py
from dataclasses import dataclass, asdict
from time import time

@dataclass
class Observation:
    step: str
    feature: str | None = None
    sample: int | None = None
    value: float | None = None
    metrics: dict | None = None
    meta: dict | None = None
    t_start: float | None = None
    t_end: float | None = None
    duration_s: float | None = None

def start_obs(step:str, tool:str, args:dict, meta=None) -> Observation:
    m = meta or {}
    m.update({"tool": tool, "args": args, "status": "ok", "error": None})
    return Observation(step=step, meta=m, t_start=time())

def finish_ok(obs:Observation, feature=None, sample=None, value=None, metrics=None, extra_meta=None) -> Observation:
    obs.t_end = time(); obs.duration_s = obs.t_end - (obs.t_start or obs.t_end)
    obs.feature = feature; obs.sample = sample; obs.value = value; obs.metrics = metrics or {}
    if extra_meta: obs.meta.update(extra_meta)
    obs.meta["status"] = "ok"
    obs.meta["error"] = None
    return obs

def finish_err(obs:Observation, err:Exception) -> Observation:
    obs.meta["status"] = "error"
    obs.meta["error"] = str(err)
    obs.t_end = time(); obs.duration_s = obs.t_end - (obs.t_start or obs.t_end)
    return obs

def to_dict(obs:Observation) -> dict:
    return asdict(obs)

