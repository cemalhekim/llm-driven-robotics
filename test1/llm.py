# llm.py
import requests

MODEL = "llama3.2"

SYSTEM = (
    "You output ONLY a single character: 1 or 0. No spaces, no text.\n"
    "Rules:\n"
    "- 1 => user wants the robot to move forward.\n"
    "- 0 => user wants the robot to move backward.\n"
    "Examples:\n"
    "User: go forward\nAssistant: 1\n"
    "User: geri git\nAssistant: 0\n"
    "User: ileri\nAssistant: 1\n"
    "User: back up\nAssistant: 0\n"
)

def ask_binary(user_text: str) -> str:
    prompt = f"System: {SYSTEM}\nUser: {user_text}\nAssistant:"
    r = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": MODEL, "prompt": prompt, "stream": False, "options": {"temperature": 0.1}},
        timeout=60,
    )
    r.raise_for_status()
    out = r.json()["response"].strip()
    # hard guard: normalise to '0' or '1'
    return "1" if out.startswith("1") else "0"

if __name__ == "__main__":
    while True:
        text = input("You: ")
        if text.lower() in {"q", "quit", "exit"}:
            break
        print(ask_binary(text))
