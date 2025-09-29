from smolagents import CodeAgent, LiteLLMModel, tool
import csv

model = LiteLLMModel(
    model_id="ollama/qwen2.5-coder:7b",
    api_base="http://localhost:11434",
    system_prompt="You are a terse Python coding assistant. Use tools precisely."
)

@tool
def csv_feature_stats(path: str, feature: str) -> dict:
    """
    Compute stats for a feature from a CSV file.

    Args:
        path (str): Full path to the CSV file.
        feature (str): One of 'OCP','CA','CV'.

    Returns:
        dict: {"count": int, "min": float, "max": float, "mean": float}
    """
    feature = feature.upper()
    col = {"OCP":"value_ocp","CA":"value_ca","CV":"value_cv"}.get(feature)
    if not col:
        raise ValueError("feature must be OCP, CA, or CV")

    n = 0; s = 0.0; mn = None; mx = None
    with open(path, newline="", encoding="utf-8") as f:
        rdr = csv.DictReader(f)
        for row in rdr:
            v = row.get(col)
            if v is None or v == "":
                continue
            x = float(v)
            n += 1; s += x
            mn = x if mn is None else min(mn, x)
            mx = x if mx is None else max(mx, x)

    return {"count": n, "min": mn, "max": mx, "mean": (s/n if n else None)}

agent = CodeAgent(
    model=model,
    tools=[csv_feature_stats],
    add_base_tools=False,
)

# Usage with your absolute path
response = agent.run(
    r"Call csv_feature_stats on C:\Users\chekim\Workspace\llm-driven-robotics\experiment_logs\20250924104104.csv for OCP"
)
print(response)
