import functools, json, re, requests
from robotmotion import uFactory_xArm
from tools import (
    go_home, connect_to_robot,
    pick_sample_from_bed, place_sample_to_bed,
    pick_sample_from_userarea, place_sample_to_userarea,
)

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
    "go_home":                    requires_connection(go_home),
    "pick_sample_from_bed":      requires_connection(pick_sample_from_bed),
    "place_sample_to_bed":       requires_connection(place_sample_to_bed),
    "pick_sample_from_userarea": requires_connection(pick_sample_from_userarea),
    "place_sample_to_userarea":  requires_connection(place_sample_to_userarea),
}

FUNCTION_LIST = [
    {"name": "go_home",                    "args": {}},
    {"name": "pick_sample_from_bed",       "args": {"i": "int (1..5)"}},
    {"name": "place_sample_to_bed",        "args": {"i": "int (1..5)"}},
    {"name": "pick_sample_from_userarea",  "args": {}},
    {"name": "place_sample_to_userarea",   "args": {}},
]

# --- SYSTEM: remove the leading f (keep braces literal)
# ---- SYSTEM (strict, no f-string) ----
SYSTEM = """
You are a router that outputs EXACTLY ONE JSON object per turn.
Output ONLY:
{"name":"<one of ['go_home','pick_sample_from_bed','place_sample_to_bed','pick_sample_from_userarea','place_sample_to_userarea']>","arguments":{...}}
No extra text. No code fences. No multiple JSON objects.

Rules (choose ONE tool):
- Bed → place: verbs like put/place/return/drop/set TO a bed slot/position ⇒ "place_sample_to_bed".
- Bed → pick:  verbs like pick/take/grab/get FROM bed/slot ⇒ "pick_sample_from_bed".
- User area → place (to the user): bring/give/hand/pass/deliver/return TO me/user/operator/user area ⇒ "place_sample_to_userarea".
- User area → pick (from the user): take/get/receive/collect FROM me/user/hand/user area ⇒ "pick_sample_from_userarea".
- Home/reset/base ⇒ "go_home".

Numbers: map ordinals/cardinals ("first/1st/one/5th/five") to i ∈ [1,5]. If i omitted but required, reuse last i; else default i=1.
Pronouns ("it/that/same one") refer to last sample index.
Spelling tolerance: "recieve" ⇒ "receive", etc.

CRITICAL:
- The "name" MUST be **exactly** one of the five allowed strings above. Do not invent new names.
"""

# ---- FEW_SHOT (covers "bring it to the user area" + variants) ----
FEW_SHOT = """
User: bring it to the user area
Assistant: {"name":"place_sample_to_userarea","arguments":{}}

User: give it to me
Assistant: {"name":"place_sample_to_userarea","arguments":{}}

User: hand the sample to the operator
Assistant: {"name":"place_sample_to_userarea","arguments":{}}

User: take this sample from me
Assistant: {"name":"pick_sample_from_userarea","arguments":{}}

User: receive it from my hand
Assistant: {"name":"pick_sample_from_userarea","arguments":{}}

User: collect the sample from the user tray
Assistant: {"name":"pick_sample_from_userarea","arguments":{}}

User: grab sample four from the bed
Assistant: {"name":"pick_sample_from_bed","arguments":{"i":4}}

User: pick the 1st sample
Assistant: {"name":"pick_sample_from_bed","arguments":{"i":1}}

User: take sample five off the bed
Assistant: {"name":"pick_sample_from_bed","arguments":{"i":5}}

User: put it in slot three
Assistant: {"name":"place_sample_to_bed","arguments":{"i":3}}

User: place the sample in the 2nd position
Assistant: {"name":"place_sample_to_bed","arguments":{"i":2}}

User: drop it to bed slot one
Assistant: {"name":"place_sample_to_bed","arguments":{"i":1}}

User: back to home
Assistant: {"name":"go_home","arguments":{}}

# NEGATIVE EXAMPLES (do NOT emulate the names)
User: bring it to the user area
Assistant: {"name":"bring_it_to_userarea","arguments":{}}  # INVALID
User: Correct that.
Assistant: {"name":"place_sample_to_userarea","arguments":{}}
"""


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

def _coerce_args(name: str, args: dict) -> dict:
    # Normalise i; clamp to [1,5].
    if name in ("pick_sample_from_bed","place_sample_to_bed"):
        i = args.get("i", 1)
        try:
            i = int(i)
        except Exception:
            i = 1
        i = max(1, min(5, i))
        return {"i": i}
    return {}

def ask_and_dispatch(user_text: str):
    call = _call_llm(user_text)  # returns {"name": "...", "arguments": {...}}
    name = call.get("name")
    if name not in TOOLS:
        raise KeyError(f"LLM returned invalid tool: {name!r}")
    args = _coerce_args(name, call.get("arguments", {}))
    fn = TOOLS[name]
    return fn(**args) if args else fn()


