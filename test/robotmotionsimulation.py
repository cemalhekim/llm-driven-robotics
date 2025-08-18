class RobotMotionSimulation:
    def __init__(self):
        self.position = 0  # simple state, mm from home

    def move_forward(self, distance=100):
        self.position += distance
        print(f"Moving forward {distance}mm from home. Current pos: {self.position}mm")

    def move_backward(self, distance=100):
        self.position -= distance
        print(f"Moving backward {distance}mm from home. Current pos: {self.position}mm")
