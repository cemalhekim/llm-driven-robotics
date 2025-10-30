#robotmotion.py

from xarm.wrapper import XArmAPI
import time

class uFactory_xArm:
    IP = "192.168.1.197"
    arm = None

    #-----POSITIONS-----
    home = [310, -2.5, 7.5, -180, -15, 0, 300]
    offsethome = [423, -2.5, 185, -180, 0, 0, 300]
    sample1above = [608.5, -67, 185, -180, 0, 0, 300]
    sample1 = [608.5, -67, 80, 180, 0, 0, 200]
    sample2above = [608.5, -35, 185, -180, 0, 0, 300]
    sample2 = [608.5, -35, 80, 180, 0, 0, 200]
    sample3above = [608.5, -4, 185, -180, 0, 0, 300]
    sample3 = [608.5, -4, 80, 180, 0, 0, 200]
    sample4above = [608.5, 27, 185, -180, 0, 0, 300]
    sample4 = [608.5, 27, 80, 180, 0, 0, 200]
    sample5above = [608.5, 58, 185, -180, 0, 0, 300]
    sample5 = [608.5, 58, 80, 180, 0, 0, 200]
    userarea = [-792, -229, 162, 90, 0, -90, 300]
    measurementstation = [540, -397, 59, -90, 0, -90, 200]

    #-------------------

    @staticmethod
    def connect():
        a = XArmAPI(uFactory_xArm.IP, is_radian=False)
        a.clean_warn(); a.clean_error()
        a.motion_enable(True); a.set_mode(0); a.set_state(0)
        uFactory_xArm.arm = a
        return a
    
    @staticmethod
    def _ensure():
        if uFactory_xArm.arm is None:
            raise RuntimeError("Call connect() first.")
        return uFactory_xArm.arm
        
    @staticmethod
    def move_to(pos, speed_override=None):
        arm = uFactory_xArm._ensure()
        x,y,z,r,p,yaw,spd = pos
        s = speed_override if speed_override is not None else spd
        code = arm.set_position(x=x, y=y, z=z, roll=r, pitch=p, yaw=yaw, speed=s, wait=True)
        if code not in (0, None):
            raise RuntimeError(f"set_position failed: {code}")
        
    @staticmethod
    def _grip_move(pos, speed=2000, timeout=2.0):
        arm = uFactory_xArm._ensure()
        arm.set_gripper_enable(True); arm.set_gripper_mode(0); arm.set_gripper_speed(speed)
        arm.set_gripper_position(pos, speed=speed, wait=False)
        t0 = time.time()
        while time.time() - t0 < timeout:
            code, cur = arm.get_gripper_position()
            if code in (0, None) and abs((cur or 0) - pos) < 10:
                break
            time.sleep(0.02)

    @staticmethod
    def gripper_open(pos=130, speed=2000): uFactory_xArm._grip_move(pos, speed)
    @staticmethod
    def gripper_close(pos=0,   speed=2000): uFactory_xArm._grip_move(pos, speed)

    @staticmethod
    def get_pose():
        arm = uFactory_xArm._ensure()
        code, pose = arm.get_position(is_radian=False)
        if code not in (0, None):
            raise RuntimeError(f"get_position error: {code}")
        return pose

    @staticmethod
    def move_forward(dx=50, speed=100):
        x,y,z,r,p,yaw = uFactory_xArm.get_pose()[:6]
        uFactory_xArm.arm.set_position(x=x+dx, y=y, z=z, roll=r, pitch=p, yaw=yaw, speed=speed, wait=True)

    @staticmethod
    def move_backward(dx=50, speed=100):
        x,y,z,r,p,yaw = uFactory_xArm.get_pose()[:6]
        uFactory_xArm.arm.set_position(x=x-dx, y=y, z=z, roll=r, pitch=p, yaw=yaw, speed=speed, wait=True)

    @staticmethod    
    def connect_to_robot():
        if uFactory_xArm.arm is None:
            uFactory_xArm.connect()
        return uFactory_xArm.arm

    # MID LEVEL FUNCTIONS
    
    @staticmethod
    def go_home():
        print("Going home...")
        uFactory_xArm.move_to(uFactory_xArm.home)

    @staticmethod
    def pick_sample_from_bed(i:int):
        print(f"Picking sample {i} from bed...")
        if not (1 <= i <= 5): raise ValueError("i must be 1..5")
        above = getattr(uFactory_xArm, f"sample{i}above")
        pose  = getattr(uFactory_xArm, f"sample{i}")
        uFactory_xArm.move_to(uFactory_xArm.offsethome)
        uFactory_xArm.move_to(above)
        uFactory_xArm.gripper_open()
        uFactory_xArm.move_to(pose)
        uFactory_xArm.gripper_close()
        uFactory_xArm.move_to(above)

    @staticmethod
    def place_sample_to_bed(i:int):
        print(f"Placing sample to bed slot {i}...")
        if not (1 <= i <= 5): raise ValueError("i must be 1..5")
        above = getattr(uFactory_xArm, f"sample{i}above")
        pose  = getattr(uFactory_xArm, f"sample{i}")
        uFactory_xArm.move_to(above)
        uFactory_xArm.move_to(pose)
        uFactory_xArm.gripper_open()
        uFactory_xArm.move_to(above)
        uFactory_xArm.move_to(uFactory_xArm.offsethome)
        uFactory_xArm.gripper_close()

    @staticmethod
    def place_sample_to_userarea():
        print("Placing sample to user area...")
        uFactory_xArm.move_to(uFactory_xArm.offsethome)
        uFactory_xArm.arm.set_position(x=263,y=-270,z=185,roll=180,pitch=0,yaw=0,
                        speed=300, radius=20, wait=False)   # 20 mm blend
        uFactory_xArm.arm.set_position(x=45,y=-270,z=215,roll=180,pitch=0,yaw=-120,
                        speed=300, radius=20, wait=False)   
        uFactory_xArm.arm.set_position(x=-250,y=-85,z=300,roll=180,pitch=0,yaw=-160,
                        speed=300, radius=20, wait=False)  
        uFactory_xArm.arm.set_position(x=-742,y=-229,z=162,roll=90,pitch=0,yaw=-90,
                        speed=300, radius=20, wait=True)   
        uFactory_xArm.move_to(uFactory_xArm.userarea)
        uFactory_xArm.gripper_open()
        uFactory_xArm.arm.set_position(x=-742,y=-229,z=162,roll=90,pitch=0,yaw=-90,
                        speed=300, radius=20, wait=True)   
        uFactory_xArm.arm.set_position(x=-250,y=-85,z=300,roll=180,pitch=0,yaw=-160,
                        speed=300, radius=20, wait=False)  
        uFactory_xArm.arm.set_position(x=45,y=-270,z=215,roll=180,pitch=0,yaw=-120,
                        speed=300, radius=20, wait=False)    
        uFactory_xArm.arm.set_position(x=263,y=0,z=185,roll=180,pitch=0,yaw=0,
                        speed=300, radius=20, wait=False)   # 20 mm blend
        uFactory_xArm.move_to(uFactory_xArm.offsethome)
        uFactory_xArm.gripper_close()

    @staticmethod
    def pick_sample_from_userarea():
        print("Picking sample from user area...")
        uFactory_xArm.move_to(uFactory_xArm.offsethome)
        uFactory_xArm.arm.set_position(x=263,y=0,z=185,roll=180,pitch=0,yaw=0,
                        speed=300, radius=20, wait=False)   # 20 mm blend
        uFactory_xArm.arm.set_position(x=45,y=-270,z=215,roll=180,pitch=0,yaw=-120,
                        speed=300, radius=20, wait=False)    # stop at final
        uFactory_xArm.arm.set_position(x=-250,y=-85,z=300,roll=180,pitch=0,yaw=-160,
                        speed=300, radius=20, wait=False)    # stop at final
        uFactory_xArm.arm.set_position(x=-742,y=-229,z=162,roll=90,pitch=0,yaw=-90,
                        speed=300, radius=20, wait=True)   
        uFactory_xArm.gripper_open()
        uFactory_xArm.move_to(uFactory_xArm.userarea)
        uFactory_xArm.gripper_close()
        uFactory_xArm.arm.set_position(x=-742,y=-229,z=162,roll=90,pitch=0,yaw=-90,
                        speed=300, radius=20, wait=True)   
        uFactory_xArm.arm.set_position(x=-250,y=-85,z=300,roll=180,pitch=0,yaw=-160,
                        speed=300, radius=20, wait=False)    # stop at final
        uFactory_xArm.arm.set_position(x=45,y=-270,z=215,roll=180,pitch=0,yaw=-120,
                        speed=300, radius=20, wait=False)    # stop at final
        uFactory_xArm.arm.set_position(x=263,y=0,z=185,roll=180,pitch=0,yaw=0,
                        speed=300, radius=20, wait=False)   # 20 mm blend
        uFactory_xArm.move_to(uFactory_xArm.offsethome)

    @staticmethod
    def place_sample_to_measurementstation():
        print("Placing sample to measurement station...")
        uFactory_xArm.move_to(uFactory_xArm.offsethome)
        uFactory_xArm.move_to(uFactory_xArm.measurementstation)
        uFactory_xArm.gripper_open()
        uFactory_xArm.arm.set_position(x=500,y=-397,z=59,roll=-90,pitch=0,yaw=-90,
                        speed=300, radius=20, wait=False)
        uFactory_xArm.move_to(uFactory_xArm.offsethome)
        uFactory_xArm.gripper_close()

    @staticmethod
    def pick_sample_from_measurementstation():
        print("Picking sample from measurement station...")
        uFactory_xArm.move_to(uFactory_xArm.offsethome)
        uFactory_xArm.arm.set_position(x=500,y=-397,z=59,roll=-90,pitch=0,yaw=-90,
                        speed=300, radius=20, wait=True)
        uFactory_xArm.gripper_open()
        uFactory_xArm.move_to(uFactory_xArm.measurementstation)
        uFactory_xArm.gripper_close()
        uFactory_xArm.move_to(uFactory_xArm.offsethome)



