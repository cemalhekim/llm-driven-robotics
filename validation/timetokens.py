import json

filename = r"C:\Users\chekim\Workspace\llm_robotic_control\validation\validation_results_first150.jsonl"

times, inputs, outputs = [], [], []

with open(filename, "r", encoding="utf-8") as file:
    for line in file:
        data = json.loads(line)
        times.append(float(data["smol_time"]))
        inputs.append(int(data["smol_inputtokens"]))
        outputs.append(int(data["smol_outputtokens"]))

avg_time = sum(times) / len(times)
avg_input = sum(inputs) / len(inputs)
avg_output = sum(outputs) / len(outputs)

print(f"Average smol_time: {avg_time:.4f}s")
print(f"Average smol_inputtokens: {avg_input:.4f}")
print(f"Average smol_outputtokens: {avg_output:.4f}")
