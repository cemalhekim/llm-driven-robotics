# translationlayer.py
from robotmotiontest import RobotMotionTest

class TranslationLayer:
    def __init__(self):
        self.arm = RobotMotionTest.connect()
        RobotMotionTest.go_home(self.arm)

    def execute(self, llm_output: str):
        if llm_output == "1":
            RobotMotionTest.move_forward(self.arm, dx=50)
        elif llm_output == "0":
            RobotMotionTest.move_backward(self.arm, dx=50)
        else:
            print(f"⚠ Unknown LLM output: {llm_output}")
