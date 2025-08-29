#robotmotiontest.py
from xarm.wrapper import XArmAPI
import time

class RobotMotionTest:
    IP = "192.168.1.197"          # ayarlayınız
    HOME = dict(x=309.5, y=-2.4, z=7.4)  # mm

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
        r = -179.9
        p = -15
        yaw = 0
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
        
    @staticmethod
    def _grip_move(arm, pos, speed=800, timeout=2.0):
        arm.set_gripper_enable(True)
        arm.set_gripper_mode(0)          # position mode
        arm.set_gripper_speed(speed)     # ↑ speed
        arm.set_gripper_position(pos, speed=speed, wait=False)
        t0 = time.time()
        while time.time() - t0 < timeout:
            code, cur = arm.get_gripper_position()  # varsa
            if code in (0, None) and abs((cur or 0) - pos) < 10:
                break
            time.sleep(0.02)

    @staticmethod
    def gripper_open(arm, pos=850, speed=2000):   # tam 850 yerine daha kısa strok
        RobotMotionTest._grip_move(arm, pos, speed)

    @staticmethod
    def gripper_close(arm, pos=0, speed=2000):  # 0 yerine yeterli kapanış
        RobotMotionTest._grip_move(arm, pos, speed)

        
    # ---- New unified function ----
    @staticmethod
    def pick_and_place(arm, pick, place, dz=60, speed=120):
        def move_lin(x,y,z,r,p,yaw):
            arm.set_position(x=x,y=y,z=z,roll=r,pitch=p,yaw=yaw,speed=speed,wait=True)
        
        # --- Pick ---
        RobotMotionTest.gripper_open(arm)
        time.sleep(0.2)
        x,y,z,r,p,yaw = pick
        move_lin(x,y,z+dz,r,p,yaw)
        move_lin(x,y,z,   r,p,yaw)
        RobotMotionTest.gripper_close(arm)
        time.sleep(0.2)
        move_lin(x,y,z+dz,r,p,yaw)

        # --- Place ---
        x,y,z,r,p,yaw = place
        move_lin(x,y,z+dz,r,p,yaw)
        move_lin(x,y,z,   r,p,yaw)
        RobotMotionTest.gripper_open(arm)
        time.sleep(0.2)
        move_lin(x,y,z+dz,r,p,yaw)
        RobotMotionTest.gripper_close(arm)
        time.sleep(0.2)

    # --- Wrapper with data ---
    @staticmethod
    def pickandplace1(arm):
        pick  = [425.1, -154.3, 10, -179.5, 0.6, 52.4]
        place = [410.8, -329, 4.7, -179.2, 0.9, 33.6]

        RobotMotionTest.pick_and_place(arm, pick, place)

'''
if __name__ == "__main__":
    arm = RobotMotionTest.connect()
    
    RobotMotionTest.go_home(arm)
    RobotMotionTest.move_forward(arm, dx=50)   # +50 mm X
    time.sleep(1)
    RobotMotionTest.move_backward(arm, dx=50)  # -50 mm X
'''

if __name__ == "__main__":
    arm = RobotMotionTest.connect()
    RobotMotionTest.go_home(arm)
    RobotMotionTest.pickandplace1(arm)
    RobotMotionTest.go_home(arm)
