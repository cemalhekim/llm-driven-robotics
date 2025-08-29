from llm import ask_and_call
from robotmotiontest import RobotMotionTest

if __name__ == "__main__":
    arm = RobotMotionTest.connect()
    RobotMotionTest.go_home(arm)

    while True:
        text = input("You: ")
        if text.lower() in {"quit", "exit"}:
            break
        decision = ask_and_call(text, arm)  # agent does the call internally
        print(f"[LLM decision] {decision}")
