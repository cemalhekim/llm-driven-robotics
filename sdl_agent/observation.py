# observation.py
from dataclasses import dataclass, asdict
from time import time

@dataclass
class Observation:
    step: str
    tool: str
    args: dict
    status: str          # "ok" | "error"
    value: float | None = None
    metrics: dict | None = None
    meta: dict | None = None
    error: str | None = None
    t_start: float | None = None
    t_end: float | None = None
    duration_s: float | None = None

def start_obs(step:str, tool:str, args:dict, meta=None) -> Observation:
    return Observation(step=step, tool=tool, args=args, status="ok", meta=meta or {}, t_start=time())

def finish_ok(obs:Observation, value=None, metrics=None, extra_meta=None) -> Observation:
    obs.t_end = time(); obs.duration_s = obs.t_end - (obs.t_start or obs.t_end)
    obs.value = value; obs.metrics = metrics or {}
    if extra_meta: obs.meta.update(extra_meta)
    return obs

def finish_err(obs:Observation, err:Exception) -> Observation:
    obs.status = "error"; obs.error = str(err)
    obs.t_end = time(); obs.duration_s = obs.t_end - (obs.t_start or obs.t_end)
    return obs

def to_dict(obs:Observation) -> dict:
    return asdict(obs)
