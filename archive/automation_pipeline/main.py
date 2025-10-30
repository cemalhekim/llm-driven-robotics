# main.py

from robotmotion import uFactory_xArm
from tools import *
from results_store import *
from llm_single import *
from llm_planner import *

# Smart executor: try plan+execute, else ask+dispatch
def smart_execute(text: str):
    try:
        return execute_plan(text)   
    except Exception:
        return ask_and_dispatch(text)  

# Main loop, user interaction
if __name__ == "__main__":
    start_run("highlevel")                         # logs to DB/JSONL
    uFactory_xArm.connect()
    uFactory_xArm.move_to(uFactory_xArm.offsethome)
    go_home()
    uFactory_xArm.gripper_close()
    print("Type 'exit' to quit.")
    while True:
        try:
            text = input("You: ").strip()
            if text.lower() in {"quit", "exit"}:
                break
            if not text:
                continue
            smart_execute(text)                   # e.g., “ocp then cv for sample 1”
            print("[OK]")
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"[Error] {e}")
