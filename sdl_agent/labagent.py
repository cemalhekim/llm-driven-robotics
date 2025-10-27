# labagent.py

from smolagents import CodeAgent, LiteLLMModel, GradioUI, tool
import toolsfake


@tool
def ocp_measurement(i: int) -> str:
    """
    Perform an OCP measurement on a given sample.

    Args:
        i (int): The sample index to measure.
    """
    result = toolsfake.ocp_measurement(i)   # prints
    return f"OCP measurement called for sample {i}"


@tool
def ca_measurement(i: int) -> str:
    """
    Perform a Chronoamperometry (CA) measurement on a given sample.

    Args:
        i (int): The sample index to measure.
    """
    result = toolsfake.ca_measurement(i)   # prints
    return f"CA measurement called for sample {i}"


@tool
def cv_measurement(i: int) -> str:
    """
    Perform a Cyclic Voltammetry (CV) measurement on a given sample.

    Args:
        i (int): The sample index to measure.
    """
    result = toolsfake.cv_measurement(i)   # prints
    return f"CV measurement called for sample {i}"


@tool
def bring_sample_to_user(i: int) -> str:
    """
    Bring a sample to the user.

    Args:
        i (int): The sample index to bring.
    """
    result = toolsfake.bring_sample_to_user(i)   # prints
    return f"Sample {i} brought to user"


@tool
def collect_sample_from_user(i: int) -> str:
    """
    Collect a sample from the user.

    Args:
        i (int): The sample index to collect.
    """
    result = toolsfake.collect_sample_from_user(i)   # prints
    return f"Sample {i} collected from user"


@tool
def go_home() -> str:
    """
    Send the robot to its home position.
    """
    result = toolsfake.go_home()   # prints
    return "Robot returned home"


model = LiteLLMModel(
    model_id="ollama/qwen2.5:7b-instruct",
    api_base="http://localhost:11434",
    system_prompt="You are a robotic lab assistant. Use ONLY the provided tools."
)


prompt = """
You are a laboratory robotic assistant.  
Your job is to directly execute the correct tool calls for the user’s request.  

RULES:
1. You may ONLY use the following tools:
   - ocp_measurement(i: int)
   - ca_measurement(i: int)
   - cv_measurement(i: int)
   - bring_sample_to_user(i: int)
   - collect_sample_from_user(i: int)
   - go_home()

2. Mapping rules:
   - "OCP" / "open circuit" / "potential" / "measure ocp" ⇒ ocp_measurement(i=...)
   - "CV" / "cyclic voltammetry" ⇒ cv_measurement(i=...)
   - "CA" / "chronoamperometry" / "chrono" ⇒ ca_measurement(i=...)
   - "bring/give/hand/pass/deliver TO me/user/operator" ⇒ bring_sample_to_user(i=...)
   - "take/get/receive/collect FROM me/user/hand/user area" ⇒ collect_sample_from_user(i=...)
   - "home/reset/base/park" ⇒ go_home()

3. Argument rules:
   - All tools except go_home require argument "i" (sample index).
   - Sample indices are integers in [1,5].
   - Interpret ordinals/cardinals: "first"=1, "second"=2, "third"=3, etc.
   - Accept ranges ("1-3", "1..3") or lists ("1 and 2", "1,2").
   - "all samples" ⇒ loop over [1,2,3,4,5].
   - If a later step omits the sample but clearly refers to the last one, reuse the last i.

4. Sequencing rules:
   - Parse connectors like "then", "after", "and".
   - Call the tools in order, one after another.

5. Output format:
   - Every answer must have exactly one `Thought:` line.
   - Then a `<code>...</code>` block with Python code.
   - Inside the code, call the tools step by step.
   - Always end with `final_answer("Done")` after executing the last step.
   - No JSON, no prose, no explanations outside the code.

EXAMPLES:

Q: do ocp for sample 1 then cv for sample 1  
A:
Thought: I need to run OCP for sample 1 and then CV for sample 1
<code>
ocp_measurement(i=1)
cv_measurement(i=1)
final_answer("Done")
</code>

Q: bring me the 5th, then go home  
A:
Thought: I need to bring sample 5 to the user and then send the robot home
<code>
bring_sample_to_user(i=5)
go_home()
final_answer("Done")
</code>

Q: do ocp for the 1st and 2nd sample then do cv for the 1st sample and ca for the 3rd  
A:
Thought: I need to run OCP for samples 1 and 2, then CV for sample 1, and CA for sample 3
<code>
ocp_measurement(i=1)
ocp_measurement(i=2)
cv_measurement(i=1)
ca_measurement(i=3)
final_answer("Done")
</code>

Q: do ocp for all samples then go home  
A:
Thought: I need to run OCP for all samples, then send the robot home
<code>
for i in [1,2,3,4,5]:
    ocp_measurement(i=i)
go_home()
final_answer("Done")
</code>
"""

agent = CodeAgent(
    model=model,
    tools=[ocp_measurement, ca_measurement, cv_measurement,
           bring_sample_to_user, collect_sample_from_user, go_home],
    instructions=prompt,
    add_base_tools=False
)


GradioUI(agent).launch()