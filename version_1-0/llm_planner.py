# llm_planner.py

# Multi-step / multi-sample planner + executor
import json, requests, time
from typing import List, Dict, Any, Iterable

# Reuse strict utilities & tool registry from your router
from llm_single import (
    _extract_first_json_obj, _coerce_args, TOOLS, MODEL, OLLAMA_URL
)

ALLOWED = list(TOOLS.keys())
TOOLS_REQUIRING_I = {
    "ocp_measurement", "cv_measurement", "ca_measurement",
    "bring_sample_to_user", "collect_sample_from_user",
}
I_MIN, I_MAX = 1, 5

SYSTEM_PLAN = f"""
You are a planner. Output EXACTLY ONE JSON object:
{{"plan":[{{"name":"...","arguments":{{...}}}}, ...]}}
Rules:
- Use ONLY these tools: {ALLOWED}.
- Interpret multi-commands in order: words like "then", "after", "and".
- Map ordinals/cardinals (first/1st/one/five/5th) to i in [{I_MIN},{I_MAX}].
- If user says "1 and 2", "1,2", "1-3", "1..3", or "all samples", represent it with "i" as a list (e.g., "i":[1,2]) or a compact range string "i":"1-3". The executor will expand.
- If a later step omits the sample but clearly refers to the last one, reuse the last i.
- Arguments must be under "arguments". For tools that do not require a sample, use an empty object {{}}
- No prose. No code fences. One JSON only.
"""

FEW_SHOT_PLAN = """
User: do ocp for sample 1 then cv for sample 1
Assistant: {"plan":[
  {"name":"ocp_measurement","arguments":{"i":1}},
  {"name":"cv_measurement","arguments":{"i":1}}
]}
User: bring me the 5th, then go home
Assistant: {"plan":[
  {"name":"bring_sample_to_user","arguments":{"i":5}},
  {"name":"go_home","arguments":{}}
]}
User: do ocp for the 1st and 2nd sample then do cv for the 1st sample and ca for the 3rd
Assistant: {"plan":[
  {"name":"ocp_measurement","arguments":{"i":[1,2]}},
  {"name":"cv_measurement","arguments":{"i":1}},
  {"name":"ca_measurement","arguments":{"i":3}}
]}
User: do ocp for all samples then go home
Assistant: {"plan":[
  {"name":"ocp_measurement","arguments":{"i":"all"}},
  {"name":"go_home","arguments":{}}
]}
"""

def _call_llm_plan(user_text: str) -> List[Dict[str, Any]]:
    prompt = f"System: {SYSTEM_PLAN}\n{FEW_SHOT_PLAN}\nUser: {user_text}\nAssistant:"
    r = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0.0, "num_ctx": 4096, "format": "json"},
        },
        timeout=60,
    )
    r.raise_for_status()
    raw = r.json().get("response", "").strip()
    obj = _extract_first_json_obj(raw)
    plan = obj.get("plan")
    if not isinstance(plan, list) or not plan:
        raise ValueError(f"Malformed plan: {obj!r}")
    return plan

# ---- Expansion & normalisation ---------------------------------------------

_WORD2NUM = {
    "one":1,"first":1,"1st":1,
    "two":2,"second":2,"2nd":2,
    "three":3,"third":3,"3rd":3,
    "four":4,"fourth":4,"4th":4,
    "five":5,"fifth":5,"5th":5,
}

def _clamp_i(v: int) -> int:
    return max(I_MIN, min(I_MAX, int(v)))

def _parse_i_token(tok: Any) -> Iterable[int]:
    """
    Accept ints, numeric strings, words, lists, ranges '1-3'/'1..3', or 'all'.
    Yields a sequence of valid indices within [I_MIN, I_MAX].
    """
    if tok is None:
        return []
    if isinstance(tok, int):
        return [_clamp_i(tok)]
    if isinstance(tok, (list, tuple)):
        out = []
        for x in tok:
            out.extend(_parse_i_token(x))
        return out
    s = str(tok).strip().lower()
    if s == "all" or "all sample" in s:
        return list(range(I_MIN, I_MAX + 1))
    if s in _WORD2NUM:
        return [_clamp_i(_WORD2NUM[s])]
    # comma-separated list "1,2,4"
    if "," in s:
        out = []
        for part in s.split(","):
            out.extend(_parse_i_token(part))
        return out
    # range "1-3" or "1..3"
    if "-" in s or ".." in s:
        sep = "-" if "-" in s else ".."
        a, b = s.split(sep, 1)
        try:
            start = _clamp_i(int(a))
            end = _clamp_i(int(b))
            if start <= end:
                return list(range(start, end + 1))
            else:
                return list(range(end, start + 1))
        except ValueError:
            pass
    # bare number string
    try:
        return [_clamp_i(int(s))]
    except ValueError:
        return []

def _needs_i(name: str) -> bool:
    return name in TOOLS_REQUIRING_I

def _expand_list_steps(steps: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    For any step with i resolving to multiple indices, duplicate the step per i.
    Also propagates missing i from previous step when required.
    """
    out: List[Dict[str, Any]] = []
    last_i: int | None = None

    for st in steps:
        name = st.get("name")
        args = st.get("arguments", {}) or {}

        if name not in ALLOWED:
            raise KeyError(f"Invalid tool name in plan: {name!r}")

        # Resolve i candidates
        raw_i = args.get("i", None)
        i_list = list(_parse_i_token(raw_i))

        # Propagate last_i if needed and missing
        if _needs_i(name) and not i_list:
            if last_i is None:
                # Let final coercion try, but keep a safe default path
                i_list = []
            else:
                i_list = [last_i]

        # If still empty and needed, default to 1
        if _needs_i(name) and not i_list:
            i_list = [1]

        # If tool doesn't need i, normalise to single call with empty args
        if not _needs_i(name):
            out.append({"name": name, "arguments": {}})
            continue

        # Duplicate per i
        for iv in i_list:
            # Reuse strict coercion from your router to stay consistent
            coerced = _coerce_args(name, {"i": iv})
            out.append({"name": name, "arguments": coerced})
            last_i = coerced.get("i", last_i)

    return out

def parse_plan(user_text: str) -> List[Dict[str, Any]]:
    """LLM → validated, expanded, execution-ready plan."""
    rough = _call_llm_plan(user_text)
    # Accept both explicit single-steps and grouped i; expand & normalise
    expanded = _expand_list_steps(rough)
    if not expanded:
        raise ValueError("Empty plan after expansion.")
    return expanded

# ---- Executor ----------------------------------------------------------------

def execute_plan(user_text: str, barrier_s: float = 0.05):
    """
    Build and run the plan in order. Returns the last tool's return.
    """
    steps = parse_plan(user_text)
    last = None
    for k, step in enumerate(steps, 1):
        name = step["name"]
        args = step.get("arguments", {}) or {}
        fn = TOOLS[name]
        last = fn(**args) if args else fn()
        if barrier_s:
            time.sleep(barrier_s)
    return last
