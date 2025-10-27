import os, sys, json, time, io, contextlib, re

# --- PATH SETUP ---
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
QUERIES_PATH = os.path.join(BASE_DIR, "annica.jsonl")
RESULTS_PATH = os.path.join(BASE_DIR, "annica_results.jsonl")

from sdl_agent.labagent import agent

ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')

def run_smol(query: str) -> dict:
    """Run SmolAgent, capture only tool calls, strip ANSI and token stats."""
    t0 = time.time()
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        try:
            result = agent.run(query)
            status = "success"
        except Exception as e:
            result, status = None, f"fail: {e}"
    raw = ansi_escape.sub("", buf.getvalue())

    # --- Extract token stats ---
    token_match = re.search(
        r"Input tokens:\s*([\d,]+)\s*\|\s*Output tokens:\s*([\d,]+)", raw)
    input_tokens = int(token_match.group(1).replace(",", "")) if token_match else 0
    output_tokens = int(token_match.group(2).replace(",", "")) if token_match else 0

    # --- Capture only uppercase tool lines like “OCP 1”, “CV 1”, “B 3”, etc. ---
    trace_lines = []
    for ln in raw.splitlines():
        line = ln.strip()
        if re.match(r"^[A-Z]{1,4}\s*\d?$", line):  # e.g. OCP 1, CV 2, B 5
            trace_lines.append(line)

    smol_trace = "".join(trace_lines).replace(" ", "")  # → OCP1CV1

    return {
        "smol_status": status,
        "smol_trace": smol_trace,
        "smol_inputtokens": input_tokens,
        "smol_outputtokens": output_tokens,
    }

# --- MAIN EXECUTION LOOP ---
results = []
with open(QUERIES_PATH, encoding="utf-8") as f:
    for line in f:
        q = json.loads(line)
        res = run_smol(q["text"])
        results.append({
            "id": q["id"],
            "text": q["text"],
            **res  # unpack dictionary keys directly
        })

# --- SAVE RESULTS ---
with open(RESULTS_PATH, "w", encoding="utf-8") as f:
    for r in results:
        f.write(json.dumps(r) + "\n")

print(f"[✓] Validation complete — results stored at {RESULTS_PATH}")
