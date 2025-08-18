import requests, json

model = "llama3.2"
messages = [
    {"role": "system", "content": "You are an LLM that outputs single word replies."}
]
while True:
    user_input = input("You: ")
    if user_input.lower() in {"quit", "exit"}:
        break

    # Append user turn
    messages.append({"role": "user", "content": user_input})

    # Combine messages into one prompt
    full_prompt = ""
    for msg in messages:
        prefix = "User:" if msg["role"] == "user" else "Assistant:"
        full_prompt += f"{prefix} {msg['content']}\n"

    # Call Ollama
    with requests.post(
        "http://localhost:11434/api/generate",
        json={"model": model, "prompt": full_prompt, "stream": True},
        stream=True,
        timeout=None
    ) as r:
        r.raise_for_status()
        reply = ""
        for line in r.iter_lines(decode_unicode=True):
            if not line:
                continue
            chunk = json.loads(line)
            if "response" in chunk:
                print(chunk["response"], end="", flush=True)
                reply += chunk["response"]
            if chunk.get("done"):
                break
        print()

    # Append assistant turn
    messages.append({"role": "assistant", "content": reply})
