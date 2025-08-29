import json, re, requests
from robotmotion import uFactory_xArm
from tools import go_home, pick_sample_from_bed, place_sample_to_bed

MODEL = "llama3.2"
OLLAMA_URL = "http://localhost:11434/api/generate"

# ---- Tool registry ----
TOOLS = {
    "go_home":          lambda: (uFactory_xArm.arm is None and connect_to_robot()) or go_home(),
    "pick_sample_from_bed": lambda i: (uFactory_xArm.arm is None and connect_to_robot()) or pick_sample_from_bed(i),
    "place_sample_to_bed":  lambda i: (uFactory_xArm.arm is None and connect_to_robot()) or place_sample_to_bed(i),
    "pick_sample_to_bed":   lambda i: (uFactory_xArm.arm is None and connect_to_robot()) or place_sample_to_bed(i),
}

FUNCTION_LIST = [
    {"name":"go_home","args":{}},
    {"name":"pick_sample_from_bed","args":{"i":"int (1..5)"}},
    {"name":"place_sample_to_bed","args":{"i":"int (1..5)"}}
]

SYSTEM = f"""
You are a router that maps user requests to EXACTLY ONE function call.
Return ONLY a JSON object: {{"name": "<one of {[f['name'] for f in FUNCTION_LIST]}>", "arguments": {{...}}}}
No prose, no code fences.

Rules:
- Choose the single best function.
- If the intent is to return/put back/place/drop a sample on the bed → "place_sample_to_bed".
- If the intent is to pick/grab/take/hold a sample from the bed → "pick_sample_from_bed".
- "home", "reset", "return to base" → "go_home".
- Map number words (one..five) or digits to integer i ∈ [1,5]. If unspecified but required, infer the most likely i.
- Arguments MUST match the function schema. Do not invent unknown fields.
"""

FEW_SHOT = """
Assistant: {"name":"pick_sample_from_bed","arguments":{"i":3}}
User: hold the first sample
Assistant: {"name":"pick_sample_from_bed","arguments":{"i":1}}
User: put it to second slot
Assistant: {"name":"place_sample_to_bed","arguments":{"i":2}}
User: drop it to 1st slot
Assistant: {"name":"place_sample_to_bed","arguments":{"i":1}}
User: place it to 4th place
Assistant: {"name":"place_sample_to_bed","arguments":{"i":4}}
User: go to offset home
Assistant: {"name":"go_home","arguments":{}}
User: back to home
Assistant: {"name":"go_home","arguments":{}}
"""

def _call_llm(user_text: str) -> dict:
    prompt = f"System: {SYSTEM}\n{FEW_SHOT}\nUser: {user_text}\nAssistant:"
    r = requests.post(
        OLLAMA_URL,
        json={"model": MODEL, "prompt": prompt, "stream": False, "options": {"temperature": 0.0}},
        timeout=60,
    )
    r.raise_for_status()
    raw = r.json().get("response", "").strip()

    # Extract first JSON object robustly (handles accidental prose/fences)
    m = re.search(r"\{.*\}", raw, flags=re.DOTALL)
    if not m:
        raise ValueError(f"LLM did not return JSON: {raw!r}")
    obj = json.loads(m.group(0))
    if "name" not in obj or "arguments" not in obj:
        raise ValueError(f"Malformed tool call: {obj!r}")
    return obj

def _coerce_args(name: str, args: dict) -> dict:
    # Normalise i; clamp to [1,5].
    if name in ("pick_sample_from_bed","place_sample_to_bed","pick_sample_to_bed"):
        i = args.get("i", 1)
        try:
            i = int(i)
        except Exception:
            i = 1
        i = max(1, min(5, i))
        return {"i": i}
    return {}

def ask_and_dispatch(user_text: str):
    call = _call_llm(user_text)
    name = call["name"]
    # alias safety
    if name == "pick_sample_to_bed":
        name = "place_sample_to_bed"
    if name not in TOOLS:
        raise KeyError(f"Unknown tool: {name}")
    args = _coerce_args(name, call.get("arguments", {}))

    # Execute
    fn = TOOLS[name]
    return fn(**args) if args else fn()

