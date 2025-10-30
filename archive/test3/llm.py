import requests
from robotmotiontest import RobotMotionTest

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
    return "1" if out.startswith("1") else "0"

# --- Agent-style function calling (tool dispatch) ---
def _move_forward(arm, dx=50, speed=100):
    RobotMotionTest.move_forward(arm, dx=dx, speed=speed)

def _move_backward(arm, dx=50, speed=100):
    RobotMotionTest.move_backward(arm, dx=dx, speed=speed)

TOOLS = {
    "1": _move_forward,   # forward
    "0": _move_backward,  # backward
}

def ask_and_call(user_text: str, arm, dx: int = 50, speed: int = 100) -> str:
    """
    Queries the LLM, then directly calls the mapped robot function.
    Returns the normalized decision ('0' or '1') for logging.
    """
    decision = ask_binary(user_text)
    TOOLS[decision](arm, dx=dx, speed=speed)
    return decision
