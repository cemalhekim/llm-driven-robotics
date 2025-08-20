# llm.py
import json
import requests
from robotmotiontest import RobotMotionTest

MODEL = "llama3.2"

SYSTEM = """You are a function-calling controller for an xArm6.
Output ONLY one JSON object, nothing else, matching:
{"tool":"<move_forward|move_backward|go_home|stop>", "args":{ ... }}

Rules:
- move_forward/backward require {"dx": <mm, number>} and optional {"speed": <mm/s>}.
- go_home optional {"speed": <mm/s>}.
- stop has {}.
- Never add text before/after JSON. No comments.
Examples:
User: go forward 20 cm fast
{"tool":"move_forward","args":{"dx":200,"speed":200}}
User: geri 5 cm
{"tool":"move_backward","args":{"dx":50}}
"""

# --- Safety clamps ---
MIN_DX, MAX_DX = 1, 300          # mm
MIN_SPEED, MAX_SPEED = 20, 300    # mm/s

def _clamp(v, lo, hi, default):
    try:
        v = float(v)
    except Exception:
        return default
    return max(lo, min(hi, v))

class LLMRobotAgent:
    def __init__(self):
        self.arm = RobotMotionTest.connect()
        RobotMotionTest.go_home(self.arm)

    def _ask_tool(self, user_text: str) -> dict:
        prompt = f"System: {SYSTEM}\nUser: {user_text}\nAssistant:"
        r = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False,
                "format": "json",            # forces JSON if supported
                "options": {"temperature": 0.0}
            },
            timeout=60,
        )
        r.raise_for_status()
        raw = r.json()["response"].strip()
        # Extract first JSON object defensively
        s, e = raw.find("{"), raw.rfind("}")
        raw = raw[s:e+1] if s != -1 and e != -1 else raw
        try:
            return json.loads(raw)
        except Exception:
            return {"tool": "stop", "args": {}}

    def _handle(self, tool: str, args: dict):
        if tool == "move_forward":
            dx = _clamp(args.get("dx", 50), MIN_DX, MAX_DX, 50)
            sp = _clamp(args.get("speed", 100), MIN_SPEED, MAX_SPEED, 100)
            RobotMotionTest.move_forward(self.arm, dx=dx, speed=sp)
        elif tool == "move_backward":
            dx = _clamp(args.get("dx", 50), MIN_DX, MAX_DX, 50)
            sp = _clamp(args.get("speed", 100), MIN_SPEED, MAX_SPEED, 100)
            RobotMotionTest.move_backward(self.arm, dx=dx, speed=sp)
        elif tool == "go_home":
            sp = _clamp(args.get("speed", 100), MIN_SPEED, MAX_SPEED, 100)
            RobotMotionTest.go_home(self.arm, speed=sp)
        elif tool == "stop":
            self.arm.set_state(4)  # pause
        else:
            print(f"⚠ Unknown tool: {tool}")

    def execute_text(self, user_text: str):
        toolcall = self._ask_tool(user_text)
        self._handle(toolcall.get("tool", "stop"), toolcall.get("args", {}))
