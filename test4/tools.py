# tools.py
from robotmotion import uFactory_xArm
import time

#--- FUNCTIONS OF THE ROBOT TO CALL ---
def connect_to_robot():
    if uFactory_xArm.arm is None:
        uFactory_xArm.connect()
    return uFactory_xArm.arm

def go_home():
    uFactory_xArm.move_to(uFactory_xArm.home)

def pick_sample_from_bed(i:int):
    if not (1 <= i <= 5): raise ValueError("i must be 1..5")
    above = getattr(uFactory_xArm, f"sample{i}above")
    pose  = getattr(uFactory_xArm, f"sample{i}")
    uFactory_xArm.move_to(uFactory_xArm.offsethome)
    uFactory_xArm.move_to(above)
    uFactory_xArm.gripper_open()
    uFactory_xArm.move_to(pose)
    uFactory_xArm.gripper_close()
    uFactory_xArm.move_to(above)

def place_sample_to_bed(i:int):
    if not (1 <= i <= 5): raise ValueError("i must be 1..5")
    above = getattr(uFactory_xArm, f"sample{i}above")
    pose  = getattr(uFactory_xArm, f"sample{i}")
    uFactory_xArm.move_to(above)
    uFactory_xArm.move_to(pose)
    uFactory_xArm.gripper_open()
    uFactory_xArm.move_to(above)
    uFactory_xArm.move_to(uFactory_xArm.offsethome)
    uFactory_xArm.gripper_close()

def place_sample_to_userarea():
    uFactory_xArm.move_to(uFactory_xArm.offsethome)
    uFactory_xArm.arm.set_position(x=263,y=0,z=185,roll=180,pitch=0,yaw=0,
                    speed=300, radius=20, wait=False)   # 20 mm blend
    uFactory_xArm.arm.set_position(x=45,y=-270,z=215,roll=180,pitch=0,yaw=-120,
                    speed=300, radius=20, wait=False)    # stop at final
    uFactory_xArm.arm.set_position(x=-250,y=-85,z=300,roll=180,pitch=0,yaw=-160,
                    speed=300, radius=20, wait=False)    # stop at final
    uFactory_xArm.move_to(uFactory_xArm.userarea)
    uFactory_xArm.gripper_open()
    uFactory_xArm.arm.set_position(x=-250,y=-85,z=300,roll=180,pitch=0,yaw=-160,
                    speed=300, radius=20, wait=False)    # stop at final
    uFactory_xArm.arm.set_position(x=45,y=-270,z=215,roll=180,pitch=0,yaw=-120,
                    speed=300, radius=20, wait=False)    # stop at final
    uFactory_xArm.arm.set_position(x=263,y=0,z=185,roll=180,pitch=0,yaw=0,
                    speed=300, radius=20, wait=False)   # 20 mm blend
    uFactory_xArm.move_to(uFactory_xArm.offsethome)
    uFactory_xArm.gripper_close()

def pick_sample_from_userarea():
    uFactory_xArm.move_to(uFactory_xArm.offsethome)
    uFactory_xArm.arm.set_position(x=263,y=0,z=185,roll=180,pitch=0,yaw=0,
                    speed=300, radius=20, wait=False)   # 20 mm blend
    uFactory_xArm.arm.set_position(x=45,y=-270,z=215,roll=180,pitch=0,yaw=-120,
                    speed=300, radius=20, wait=False)    # stop at final
    uFactory_xArm.arm.set_position(x=-250,y=-85,z=300,roll=180,pitch=0,yaw=-160,
                    speed=300, radius=20, wait=False)    # stop at final
    uFactory_xArm.gripper_open()
    uFactory_xArm.move_to(uFactory_xArm.userarea)
    uFactory_xArm.gripper_close()
    uFactory_xArm.arm.set_position(x=-250,y=-85,z=300,roll=180,pitch=0,yaw=-160,
                    speed=300, radius=20, wait=False)    # stop at final
    uFactory_xArm.arm.set_position(x=45,y=-270,z=215,roll=180,pitch=0,yaw=-120,
                    speed=300, radius=20, wait=False)    # stop at final
    uFactory_xArm.arm.set_position(x=263,y=0,z=185,roll=180,pitch=0,yaw=0,
                    speed=300, radius=20, wait=False)   # 20 mm blend
    uFactory_xArm.move_to(uFactory_xArm.offsethome)
#----------------------------------

