# evaluator.py

MAX_RETRIES=2; OCP_LOW=0.30

def decide(state, obs):
    if obs.status!="ok":
        if state["retries"]<MAX_RETRIES:
            return {"action":"retry", "next":(obs.tool, obs.args), "why":"tool error"}
        return {"action":"stop", "why":"max retries"}

    if obs.tool=="ocp_measurement":
        i=obs.args["i"]
        if obs.value < OCP_LOW:   return {"action":"continue", "next":("ca_measurement",{"i":i}), "why":"low OCP"}
        else:                     return {"action":"continue", "next":("cv_measurement",{"i":i}), "why":"ok OCP"}

    if obs.tool in {"cv_measurement","ca_measurement"}:
        return {"action":"stop", "why":"measurement complete"}

    return {"action":"stop", "why":"unknown tool"}
