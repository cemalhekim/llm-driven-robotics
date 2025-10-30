# instruments.py

import random

class instruments:

    @staticmethod
    def ocp_measurement_step():
        v = random.uniform(0, 1)
        print("Open Circuit Potential measurement started...")
        print(f"OCP measurement done. Result: {v:.3f} V")
        return v

    @staticmethod
    def ca_measurement_step():
        v = random.uniform(0, 1)
        print("Chronoamperometry measurement started...")
        print(f"CA measurement done. Result: {v:.3f} A")
        return v

    @staticmethod
    def cv_measurement_step():
        import random
        v = random.uniform(0, 1)
        print("Cyclic Voltammetry measurement started...")
        print(f"CV measurement done. Result: {v:.3f} V")
        return v
