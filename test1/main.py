# main.py
from llm import ask_binary
from translationlayer import TranslationLayer

if __name__ == "__main__":
    tl = TranslationLayer()

    while True:
        text = input("You: ")
        if text.lower() in {"quit", "exit"}:
            break

        # 1) Get 0/1 decision from LLM
        result = ask_binary(text)

        # 2) Pass to translation layer
        tl.execute(result)
