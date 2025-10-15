import json
import os

RESULTS_PATH = r"C:\Users\chekim\Workspace\llm_robotic_control\validation\validation_results.jsonl"
REFERENCES_PATH = r"C:\Users\chekim\Workspace\llm_robotic_control\validation\correct_simulated_outputs.jsonl"

print(f"Reading results from: {RESULTS_PATH}")
print(f"Reading references from: {REFERENCES_PATH}")

BASE_DIR = os.path.dirname(__file__)

def load_jsonl(path):
    data = []
    with open(path, "r", encoding="utf-8-sig") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                data.append(json.loads(line))
            except json.JSONDecodeError as e:
                print(f"[!] Skipped malformed line in {path}: {e}")
    return data


results_data = load_jsonl(RESULTS_PATH)
refs_data = load_jsonl(REFERENCES_PATH)

results = {int(r["id"]): r["smol_trace"].strip().upper() for r in results_data}
refs = {int(r["id"]): r["expected"].strip().upper() for r in refs_data}

# --- Compare ---
total = len(refs)
matches, mismatches = 0, []

for i, exp in refs.items():
    got = results.get(i)
    if got == exp:
        matches += 1
    else:
        mismatches.append({"id": i, "expected": exp, "got": got})

# --- Stats ---
accuracy = (matches / total) * 100 if total else 0

print(f"✅ Total tests: {total}")
print(f"✅ Correct matches: {matches}")
print(f"❌ Mismatches: {len(mismatches)}")
print(f"🎯 Success rate: {accuracy:.2f}%\n")

if mismatches:
    print("Mismatched cases:")
    for m in mismatches:
        print(f"  ID {m['id']:>3}: expected={m['expected']} | got={m['got']}")
