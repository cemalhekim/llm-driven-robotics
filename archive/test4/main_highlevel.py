# main_highlevel.py
from robotmotion import uFactory_xArm
from tools import go_home
from results_store import start_run
from llm_highlevel import ask_and_dispatch, _coerce_args, TOOLS
from llm_planner import _call_llm_plan

def smart_execute(text: str):
    # Try multi-step plan
    try:
        steps = _call_llm_plan(text)              # [{"name":..., "arguments":{...}}, ...]
    except Exception:
        return ask_and_dispatch(text)             # planner failed → strict single-step

    if not steps:
        return

    # If only one step, let the strict router handle coercion/validation
    if len(steps) == 1:
        return ask_and_dispatch(text)

    # Multi-step: validate & execute in order
    last = None
    for k, st in enumerate(steps, 1):
        name = st.get("name")
        if name not in TOOLS:
            raise KeyError(f"Invalid tool in step {k}: {name!r}")
        args = _coerce_args(name, st.get("arguments", {}) or {})
        fn = TOOLS[name]
        last = fn(**args) if args else fn()
    return last

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
