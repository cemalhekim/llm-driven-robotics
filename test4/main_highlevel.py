#main_highlevel.py
from llm_highlevel import ask_and_dispatch
from robotmotion import uFactory_xArm
from tools import go_home
from results_store import start_run
if __name__ == "__main__":
    start_run("highlevel")
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
            ask_and_dispatch(text)   # e.g., "grab sample four", "put it back"
            print("[OK]")
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"[Error] {e}")