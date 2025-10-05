# toolsfake.py

def ocp_measurement(i: int):
    print("FAKE: Performing OCP measurement for sample", i)

def ca_measurement(i: int):
    print("FAKE: Performing CA measurement for sample", i)

def cv_measurement(i: int):
    print("FAKE: Performing CV measurement for sample", i)

def bring_sample_to_user(i: int):
    print("FAKE: Bringing sample #", i, "to user")

def collect_sample_from_user(i: int):
    print("FAKE: Collecting sample #", i, "from user")

def go_home():
    print("FAKE: Going home")