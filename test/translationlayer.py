from robotmotionsimulation import RobotMotionSimulation

class TranslationLayer:
    def __init__(self):
        self.robot = RobotMotionSimulation()

    def execute(self, llm_output: str):
        """
        Map LLM output (0 or 1) to robot actions.
        """
        llm_output = llm_output.strip()

        if llm_output == "1":
            self.robot.move_forward()
        elif llm_output == "0":
            self.robot.move_backward()
        else:
            print(f"⚠️ Unknown LLM output: {llm_output}")
