from xarm.wrapper import XArmAPI
import time

class RobotMotionTest:
    IP = "192.168.1.197"          # ayarlayınız
    HOME = dict(x=360, y=-220, z=110)  # mm

    @staticmethod
    def connect():
        arm = XArmAPI(RobotMotionTest.IP, is_radian=False)
        arm.clean_warn(); arm.clean_error()
        arm.motion_enable(True)
        arm.set_mode(0); arm.set_state(0)
        return arm

    @staticmethod
    def get_pose(arm):
        code, pose = arm.get_position(is_radian=False)
        if code not in (0, None):
            raise RuntimeError(f"get_position error: {code}")
        return pose  # [x,y,z, roll,pitch,yaw, ...]

    @staticmethod
    def go_home(arm, speed=100):
        # Mevcut RPY'yi koru
        r, p, yaw = RobotMotionTest.get_pose(arm)[3:6]
        arm.set_position(x=RobotMotionTest.HOME["x"],
                         y=RobotMotionTest.HOME["y"],
                         z=RobotMotionTest.HOME["z"],
                         roll=r, pitch=p, yaw=yaw,
                         speed=speed, wait=True)

    @staticmethod
    def move_forward(arm, dx=50, speed=100):
        x,y,z, r,p,yaw = RobotMotionTest.get_pose(arm)[:6]
        arm.set_position(x=x+dx, y=y, z=z, roll=r, pitch=p, yaw=yaw,
                         speed=speed, wait=True)

    @staticmethod
    def move_backward(arm, dx=50, speed=100):
        x,y,z, r,p,yaw = RobotMotionTest.get_pose(arm)[:6]
        arm.set_position(x=x-dx, y=y, z=z, roll=r, pitch=p, yaw=yaw,
                         speed=speed, wait=True)

if __name__ == "__main__":
    arm = RobotMotionTest.connect()
    
    RobotMotionTest.go_home(arm)
    RobotMotionTest.move_forward(arm, dx=50)   # +50 mm X
    time.sleep(1)
    RobotMotionTest.move_backward(arm, dx=50)  # -50 mm X
