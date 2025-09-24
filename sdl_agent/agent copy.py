from smolagents import CodeAgent, LiteLLMModel, tool

# Model definition
model = LiteLLMModel(
    model_id="ollama/qwen2.5-coder:7b",
    api_base="http://localhost:11434",
    system_prompt="You are a Python coding assistant. Always return clean and working code."
)

@tool
def add_numbers(a: int, b: int) -> int:
    """
    Add two integers.

    Args:
        a (int): The first integer.
        b (int): The second integer.

    Returns:
        int: The sum of the two integers.
    """
    return a + b

# Create agent
agent = CodeAgent(
    model=model,
    tools=[add_numbers],
    add_base_tools=True
)

# Run a query
response = agent.run('a = 3, b = 5, c = "random text", what is b?')
print("Agent response:", response)
