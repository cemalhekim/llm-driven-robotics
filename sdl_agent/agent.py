from smolagents import CodeAgent, LiteLLMModel, tool
import json
import statistics
from pathlib import Path

BASE_DIR = Path("C:/Users/chekim/Workspace/llm-driven-robotics/experiment_logs")
filename = "20250923141408.jsonl"


@tool
def load_json_file(filename: str) -> list[dict]:
    """
    Load and parse a JSON Lines (JSONL) file containing experimental records.

    This function is designed for structured experiment logging pipelines where 
    each line in the file represents a single JSON object (e.g., one measurement, 
    observation, or event). It automatically resolves the file path inside the 
    global `BASE_DIR` directory and reads the file in UTF-8 encoding.

    Typical use cases include:
        - Loading measurement logs for statistical analysis.
        - Retrieving experiment metadata such as tool usage, sample IDs, and timing.
        - Serving as the first step in a chain of tools (e.g., followed by 
          `extract_field` and `analyze_values`).

    Args:
        filename (str):
            The relative name of the file inside the experiment_logs directory.
            Example: "20250923141408.jsonl"

    Returns:
        list[dict]:
            A list of parsed JSON objects, where each object corresponds to one 
            line from the JSONL file. The objects may contain keys such as:
            - "ts": str → timestamp of the record.
            - "step": str → workflow step (e.g., "measurement").
            - "feature": str → measured feature (e.g., "OCP", "CV").
            - "sample": int → sample identifier.
            - "value": float → measurement value.
            - "metrics": dict → additional computed metrics.
            - "meta": dict → metadata about the tool call, arguments, and status.

    Raises:
        FileNotFoundError:
            If the specified file does not exist in BASE_DIR.
        json.JSONDecodeError:
            If a line in the file cannot be parsed as valid JSON.
        UnicodeDecodeError:
            If the file is not UTF-8 encoded.

    Example:
        >>> records = load_json_file("20250923141408.jsonl")
        >>> len(records)
        128
        >>> records[0]["feature"]
        'OCP'

    Notes:
        - The function does not perform semantic validation of the data.
        - To extract specific fields, use the `extract_field` tool.
        - To compute statistics on values, use the `analyze_values` tool.
    """
    file_path = BASE_DIR / filename
    with open(file_path, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f]


@tool
def analyze_values(values: list[float], operation: str = "max", k: int = 2) -> float | list:
    """
    Perform statistical operations on a list of numeric values.

    This function is intended to provide flexible, lightweight analysis of 
    experimental results. It supports both single-value aggregations and 
    list-returning operations such as "top-k" or "bottom-k". It is typically 
    used after extracting measurement values from experiment logs (e.g., via 
    `extract_field`).

    Args:
        values (list[float]):
            A list of numeric values to analyze. Must not be empty.
            Example: [0.65, 0.68, 0.98]

        operation (str, optional):
            The statistical operation to perform. Must be one of:
                - "max"     → Return the maximum value.
                - "min"     → Return the minimum value.
                - "avg"     → Return the arithmetic mean of all values.
                - "median"  → Return the statistical median.
                - "topk"    → Return the k largest values (descending).
                - "bottomk" → Return the k smallest values (ascending).
            Defaults to "max".

        k (int, optional):
            Number of items to return when using "topk" or "bottomk".
            Ignored for other operations. Defaults to 2.

    Returns:
        float | list:
            - For "max", "min", "avg", "median": returns a single float.
            - For "topk" or "bottomk": returns a list of floats.

    Raises:
        ValueError:
            If `values` is empty.
            If `operation` is not one of the supported strings.

    Example:
        >>> analyze_values([0.65, 0.68, 0.98], "avg")
        0.771
        >>> analyze_values([0.65, 0.68, 0.98], "topk", k=2)
        [0.98, 0.68]

    Notes:
        - This function does not perform outlier removal or normalization.
        - For more complex statistics (variance, std, etc.), extend the 
          `operation` parameter as needed.
        - Best used in combination with `extract_field` for feature-specific 
          analysis of experiment logs.
    """
    if not values:
        raise ValueError("Values list cannot be empty.")

    if operation == "max":
        return max(values)
    elif operation == "min":
        return min(values)
    elif operation == "avg":
        return sum(values) / len(values)
    elif operation == "median":
        return statistics.median(values)
    elif operation == "topk":
        return sorted(values, reverse=True)[:k]
    elif operation == "bottomk":
        return sorted(values)[:k]
    else:
        raise ValueError(f"Unknown operation: {operation}")

@tool
def extract_field(records: list[dict], field: str) -> list:
    """
    Extract a specific field (key) from a list of JSON records.

    This function is typically used after loading experiment logs (via 
    `load_json_file`). Each record is expected to be a dictionary representing 
    one measurement or event. The function collects all values associated with 
    the given field and returns them as a list, preserving their order in the 
    input data.

    Args:
        records (list[dict]):
            A list of JSON objects, usually obtained from `load_json_file`.
            Example:
                [
                    {"feature": "OCP", "value": 0.68, "sample": 1},
                    {"feature": "OCP", "value": 0.65, "sample": 2},
                    {"feature": "CV",  "value": 0.15, "sample": 1}
                ]

        field (str):
            The key to extract from each record.
            - Must be a top-level key in the JSON objects.
            - Nested fields (e.g., "meta.tool") are not supported in the current
              version and will need to be handled manually.

    Returns:
        list:
            A list of values corresponding to the requested field.
            - If the field exists in a record, its value is included.
            - If the field is missing, that record is skipped.

            Example:
                >>> extract_field(records, "value")
                [0.68, 0.65, 0.15]

    Raises:
        TypeError:
            If `records` is not a list of dictionaries.
        ValueError:
            If `field` is empty or not a string.

    Example:
        >>> data = load_json_file("20250923141408.jsonl")
        >>> values = extract_field(data, "value")
        >>> len(values)
        3
        >>> values
        [0.6840319979459244, 0.6516, 0.984152]

    Notes:
        - Use this function to prepare data for statistical analysis with 
          `analyze_values`.
        - For nested field extraction, consider extending this function 
          to support dotted paths (e.g., "meta.tool").
        - The function does not alter the type of the values; they are returned 
          exactly as stored in the JSON records.
    """
    return [rec[field] for rec in records if field in rec]


model = LiteLLMModel(
    model_id="ollama/llama3.2",
    api_base="http://localhost:11434",
    system_prompt=(
        "You are a strict data analysis agent. "
        "You are restricted to use ONLY the following tools: "
        "load_json_file, extract_field, analyze_values. "
        "You must never invent or assume new functions, APIs, or data. "
        "\n\n"
        "Your primary workflow is:\n"
        "1. Use load_json_file(filename) to load experimental logs.\n"
        "2. Use extract_field(records, field) to select specific fields (e.g., 'value', 'feature').\n"
        "3. Use analyze_values(values, operation, k) to compute statistics (e.g., max, min, avg).\n"
        "\n"
        "Guidelines:\n"
        "- Always prefer chaining tools rather than reasoning in free text.\n"
        "- If the user asks a natural question (e.g., 'What is the average OCP?'), "
        "translate it into the correct sequence of tool calls.\n"
        "- Return only the results from tools. Do not fabricate numbers.\n"
        "- If a request cannot be fulfilled with the available tools, politely state this.\n"
        "\n"
        "Examples:\n"
        "User: 'Load the experiment data from 20250923141408.jsonl.'\n"
        "Agent: call load_json_file('20250923141408.jsonl')\n"
        "\n"
        "User: 'What is the average value of OCP measurements?'\n"
        "Agent: load_json_file → extract_field(..., 'value') → analyze_values(..., 'avg')\n"
        "\n"
        "User: 'Show me the two highest CV values.'\n"
        "Agent: load_json_file → extract_field(..., 'value') → analyze_values(..., 'topk', k=2)\n"
    )
)

agent = CodeAgent(
    model=model,
    tools=[load_json_file, extract_field, analyze_values],
    additional_authorized_imports=["json", "os"]
)

result = agent.run("Can you tell me the maximum OCP value?")
print(result)