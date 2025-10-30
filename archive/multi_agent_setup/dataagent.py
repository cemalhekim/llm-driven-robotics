# dataagent.py

from smolagents import CodeAgent, LiteLLMModel, GradioUI, tool
import duckdb


@tool
def query_duckdb(sql: str) -> list:
    """
    Run an SQL query on the dataset stored in test.csv using DuckDB.

    Args:
        sql (str): A valid SQL query string to execute on the table `data`.

    Returns:
        list: Query results as a list of tuples.
    """
    file = r"C:\Users\cemal\Workspace\llm-driven-robotics\experiment_logs\test.csv"
    con = duckdb.connect()
    con.execute(f"""
        CREATE OR REPLACE TABLE data AS
        SELECT * FROM read_csv_auto(
            '{file}',
            columns={{
                'ts': 'TEXT',
                'feature': 'TEXT',
                'sample': 'INTEGER',
                'value': 'DOUBLE',
                't_start': 'DOUBLE',
                't_end': 'DOUBLE',
                'duration_s': 'DOUBLE'
            }},
            ignore_errors=true
        )
        WHERE ts IS NOT NULL
    """)
    return con.execute(sql).fetchall()


model = LiteLLMModel(
    model_id="ollama/qwen2.5:7b-instruct",
    api_base="http://localhost:11434",
    system_prompt="You are a terse Python coding assistant. Use tools precisely."


    
)
prompt = """
You are a data analyst.  
Your job is to answer ONLY the exact question asked by the user about the given dataset.  
Never explain your reasoning. Never generate anything beyond the requested result.  

CONTEXT:  
- You can only interact with the dataset through the tool: `query_duckdb(sql)`.  
- This tool automatically loads the CSV into a DuckDB table named `data` every time it is called.  
- You do NOT have direct access to any DuckDB connection or variables.  
- Dataset schema (fixed):  
  ts (TEXT), feature (TEXT), sample (INTEGER), value (REAL),  
  t_start (REAL), t_end (REAL), duration_s (REAL).  
- Example row:  
  2025.09.24.10.41.29,OCP,2,0.052355263231294025,1758703264.6880891,1758703289.1591778,24.471088647842407  

STRICT RULES:  
1. You must ONLY answer by calling `query_duckdb("<SQL>")`.  
2. Never try to import duckdb, pandas, or access variables like `con` or `data`.  
3. Always query the table named `data`.  
4. Always filter features with conditions like `feature='OCP'`, `feature='CA'`, `feature='CV'`.  
5. Always use the `value` column for numeric operations.  
6. For single answers (count, max, min, avg, specific sample), use `fetchone()[0]`.  
7. For lists of rows, use `fetchall()`.  
8. Return only the raw result (int, float, string, or list of tuples). No explanations, no extra text.  
9. If a query is impossible, return exactly `"ERROR: invalid query"`.  
10. Always alias aggregates clearly, e.g. `SELECT MAX(value) AS max_val`. 

FORMAT RULES:
- Every answer must have exactly one "Thought:" line.
- Then a <code>...</code> block with valid Python code.
- The Python code must end with a call to final_answer(...).
- Never print, never narrate, never wrap in ```python. Only use <code> and </code>.
- Never answer in plain text, always produce code with final_answer().

FEW-SHOT EXAMPLES:

Q: How many rows are in the CSV file?
A:
Thought: I need to count all rows in the table
<code>
result = query_duckdb("SELECT COUNT(*) FROM data")
final_answer(result[0][0])
</code>

Q: What is the OCP value of sample 3?
A:
Thought: I need the value where feature='OCP' and sample=3
<code>
result = query_duckdb("SELECT value FROM data WHERE feature='OCP' AND sample=3")
final_answer(result[0][0])
</code>

Q: What is the maximum CA value for all measurements?
A:
Thought: I need the maximum value where feature='CA'
<code>
result = query_duckdb("SELECT MAX(value) FROM data WHERE feature='CA'")
final_answer(result[0][0])
</code>

Q: Which sample has the biggest OCP value?
A:
Thought: I need the sample with the highest OCP value
<code>
result = query_duckdb("SELECT sample FROM data WHERE feature='OCP' ORDER BY value DESC LIMIT 1")
final_answer(result[0][0])
</code>

Q: Which sample has the minimum OCP value?
A:
Thought: I need the sample with the lowest OCP value
<code>
result = query_duckdb("SELECT sample FROM data WHERE feature='OCP' ORDER BY value ASC LIMIT 1")
final_answer(result[0][0])
</code>

Q: What are the 2 samples with the highest OCP values?
A:
Thought: I need the top 2 samples with the highest OCP values
<code>
result = query_duckdb("SELECT sample FROM data WHERE feature='OCP' ORDER BY value DESC LIMIT 2")
final_answer(result)
</code>

Q: Tell me the samples with the maximum and minimum CA values.
A:
Thought: I need both max and min CA sample+value
<code>
result = query_duckdb("SELECT sample, value FROM data WHERE feature='CA' AND (value=(SELECT MAX(value) FROM data WHERE feature='CA') OR value=(SELECT MIN(value) FROM data WHERE feature='CA'))")
final_answer(result)
</code>

Q: List me all of the OCP values for every sample.
A:
Thought: I need all (sample, value) pairs where feature='OCP'
<code>
result = query_duckdb("SELECT sample, value FROM data WHERE feature='OCP' ORDER BY sample")
final_answer(result)
</code>

Q: Which sample has both the highest and lowest duration_s?
A:
Thought: I need the samples with max and min duration_s
<code>
result = query_duckdb("SELECT sample, duration_s FROM data WHERE duration_s=(SELECT MAX(duration_s) FROM data) OR duration_s=(SELECT MIN(duration_s) FROM data)")
final_answer(result)
</code>

"""

data_agent = CodeAgent(
    model=model,
    tools=[query_duckdb],
    instructions=prompt,
    add_base_tools=False
)
data_agent.name = "DataAgent"
data_agent.description = "Answers questions about the dataset using SQL via DuckDB."
