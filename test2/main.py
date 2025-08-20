# main.py
from llm import LLMRobotAgent

if __name__ == "__main__":
    agent = LLMRobotAgent()
    print("Agent ready. Type 'exit' to quit.")
    while True:
        text = input("You: ")
        if text.lower() in {"exit", "quit", "q"}:
            break
        agent.execute_text(text)
