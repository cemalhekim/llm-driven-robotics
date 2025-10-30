#llm_single.py

import functools, json, re, requests, time
from robotmotion import uFactory_xArm
from tools import *

# ---- LLM config ----
MODEL = "llama3.2"
OLLAMA_URL = "http://localhost:11434/api/generate"

def _ensure_connected():
    if uFactory_xArm.arm is None:
        connect_to_robot()

def requires_connection(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        _ensure_connected()
        return fn(*args, **kwargs)
    return wrapper

TOOLS = {
    "ocp_measurement":          requires_connection(ocp_measurement),
    "cv_measurement":           requires_connection(cv_measurement),
    "ca_measurement":           requires_connection(ca_measurement),
    "go_home":                  requires_connection(go_home),
    "bring_sample_to_user":     requires_connection(bring_sample_to_user),
    "collect_sample_from_user": requires_connection(collect_sample_from_user),
}

FUNCTION_LIST = [
    {"name": "go_home",                   "args": {}},
    {"name": "ocp_measurement",           "args": {"i": "int (1..5)"}},
    {"name": "cv_measurement",            "args": {"i": "int (1..5)"}},
    {"name": "ca_measurement",            "args": {"i": "int (1..5)"}},
    {"name": "bring_sample_to_user",      "args": {"i": "int (1..5)"}},
    {"name": "collect_sample_from_user",  "args": {"i": "int (1..5)"}},

]

# ---- SYSTEM (strict, high-level only) ----
SYSTEM = """
You are a router that outputs EXACTLY ONE JSON object per turn.
Output ONLY:
{"name":"<one of ['go_home','ocp_measurement','cv_measurement','ca_measurement','bring_sample_to_user','collect_sample_from_user']>","arguments":{...}}
No extra text. No code fences. No multiple JSON objects.

Choose ONE tool based on intent:
- "OCP" / "open circuit" / "potential" / "measure ocp" ⇒ "ocp_measurement" with i ∈ [1,5]
- "CV" / "cyclic voltammetry" ⇒ "cv_measurement" with i ∈ [1,5]
- "CA" / "chronoamperometry" / "chrono" ⇒ "ca_measurement" with i ∈ [1,5]
- Bring/give/hand/pass/deliver TO me/user/operator/user area ⇒ "bring_sample_to_user" with i ∈ [1,5]
- Take/get/receive/collect FROM me/user/hand/user area ⇒ "collect_sample_from_user" with i ∈ [1,5]
- Home/reset/base ⇒ "go_home" (no args)

Numbers: map ordinals/cardinals ("first/1st/one/5th/five") to i ∈ [1,5].
If i is omitted but required, default i=1.
Spelling tolerance allowed.
CRITICAL: "name" MUST be exactly one of the six allowed strings above; do not invent new names.
"""

# ---- FEW_SHOT (high-level intents) ----
FEW_SHOT = """
User: measure OCP of sample 3
Assistant: {"name":"ocp_measurement","arguments":{"i":3}}

User: run cyclic voltammetry on five
Assistant: {"name":"cv_measurement","arguments":{"i":5}}

User: do CA for the 2nd sample
Assistant: {"name":"ca_measurement","arguments":{"i":2}}

User: bring me the first sample
Assistant: {"name":"bring_sample_to_user","arguments":{"i":1}}

User: hand over sample four to me
Assistant: {"name":"bring_sample_to_user","arguments":{"i":4}}

User: collect the sample from the user tray
Assistant: {"name":"collect_sample_from_user","arguments":{"i":1}}

User: take sample 3 from me
Assistant: {"name":"collect_sample_from_user","arguments":{"i":3}}

User: back to home
Assistant: {"name":"go_home","arguments":{}}

# NEGATIVE (do NOT emulate):
User: bring me sample 2
Assistant: {"name":"place_sample_to_userarea","arguments":{"i":2}}  # INVALID (mid-level)
User: Correct that.
Assistant: {"name":"bring_sample_to_user","arguments":{"i":2}}
"""

# ---- ARGUMENT NORMALISATION ----
def _coerce_args(name: str, args: dict) -> dict:
    need_i = {"ocp_measurement","cv_measurement","ca_measurement",
              "bring_sample_to_user","collect_sample_from_user"}
    if name in need_i:
        i = args.get("i", 1)
        try:
            i = int(i)
        except Exception:
            # try simple word→number mapping
            WORD2NUM = {"one":1,"first":1,"two":2,"second":2,"three":3,"third":3,
                        "four":4,"fourth":4,"five":5,"fifth":5}
            i = WORD2NUM.get(str(i).strip().lower(), 1)
        i = max(1, min(5, i))
        return {"i": i}
    return {}

def _extract_first_json_obj(s: str) -> dict:
    """Return the first balanced top-level JSON object found in s."""
    start = s.find("{")
    if start == -1:
        raise ValueError(f"No JSON object found: {s!r}")
    depth, in_str, esc = 0, False, False
    for i, ch in enumerate(s[start:], start):
        if in_str:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == '"':
                in_str = False
            continue
        else:
            if ch == '"':
                in_str = True
            elif ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    return json.loads(s[start:i+1])
    raise ValueError(f"Incomplete JSON object: {s!r}")

def _call_llm(user_text: str) -> dict:
    prompt = f"System: {SYSTEM}\n{FEW_SHOT}\nUser: {user_text}\nAssistant:"
    r = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.0,
                "num_ctx": 2048,
                # Ask for strict JSON; Ollama will *encourage* compliance.
                "format": "json"
            },
        },
        timeout=60,
    )
    r.raise_for_status()
    raw = r.json().get("response", "").strip()
    # Be forgiving if the model still emits extra text/newlines:
    obj = _extract_first_json_obj(raw)
    if "name" not in obj or "arguments" not in obj:
        raise ValueError(f"Malformed tool call: {obj!r}")
    return obj

def ask_and_dispatch(user_text: str):
    call = _call_llm(user_text)  # returns {"name": "...", "arguments": {...}}
    name = call.get("name")
    if name not in TOOLS:
        raise KeyError(f"LLM returned invalid tool: {name!r}")
    args = _coerce_args(name, call.get("arguments", {}))
    fn = TOOLS[name]
    return fn(**args) if args else fn()


