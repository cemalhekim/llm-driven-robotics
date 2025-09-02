# tools.py
from robotmotion import uFactory_xArm
import random
from results_store import log_measurement, current_run


def connect_to_robot():
    if uFactory_xArm.arm is None:
        uFactory_xArm.connect()
    return uFactory_xArm.arm

# MID LEVEL FUNCTIONS
def go_home():
    print("Going home...")
    uFactory_xArm.move_to(uFactory_xArm.home)

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

def place_sample_to_measurementstation():
    print("Placing sample to measurement station...")
    uFactory_xArm.move_to(uFactory_xArm.offsethome)
    uFactory_xArm.move_to(uFactory_xArm.measurementstation)
    uFactory_xArm.gripper_open()
    uFactory_xArm.arm.set_position(x=500,y=-397,z=59,roll=-90,pitch=0,yaw=-90,
                    speed=300, radius=20, wait=False)
    uFactory_xArm.move_to(uFactory_xArm.offsethome)
    uFactory_xArm.gripper_close()

def pick_sample_from_measurementstation():
    print("Picking sample from measurement station...")
    uFactory_xArm.move_to(uFactory_xArm.offsethome)
    uFactory_xArm.arm.set_position(x=500,y=-397,z=59,roll=-90,pitch=0,yaw=-90,
                    speed=300, radius=20, wait=True)
    uFactory_xArm.gripper_open()
    uFactory_xArm.move_to(uFactory_xArm.measurementstation)
    uFactory_xArm.gripper_close()
    uFactory_xArm.move_to(uFactory_xArm.offsethome)

def ocp_measurement_step():
    v = random.uniform(0, 1)
    print("Open Circuit Potential measurement started...")
    print(f"OCP measurement done. Result: {v:.3f} V")
    return v

def ca_measurement_step():
    v = random.uniform(0, 1)
    print("Chronoamperometry measurement started...")
    print(f"CA measurement done. Result: {v:.3f} A")
    return v

def cv_measurement_step():
    import random
    v = random.uniform(0, 1)
    print("Cyclic Voltammetry measurement started...")
    print(f"CV measurement done. Result: {v:.3f} V")
    return v
#----------------------------------

# HIGH LEVEL FUNCTIONS
def ocp_measurement(i:int):
    pick_sample_from_bed(i)
    place_sample_to_measurementstation()
    v = ocp_measurement_step()
    log_measurement("ocp", i, v, meta={"pose":"measurementstation"})
    pick_sample_from_measurementstation()
    place_sample_to_bed(i)

def ca_measurement(i:int):
    pick_sample_from_bed(i)
    place_sample_to_measurementstation()
    v = ca_measurement_step()
    log_measurement("ca", i, v, meta={"pose":"measurementstation"})
    pick_sample_from_measurementstation()
    place_sample_to_bed(i)

def cv_measurement(i:int):
    pick_sample_from_bed(i)
    place_sample_to_measurementstation()
    v = cv_measurement_step()
    log_measurement("cv", i, v, meta={"pose":"measurementstation"})
    pick_sample_from_measurementstation()
    place_sample_to_bed(i)

def bring_sample_to_user(i:int):
    pick_sample_from_bed(i)
    place_sample_to_userarea()

def collect_sample_from_user(i:int):
    pick_sample_from_userarea()
    place_sample_to_bed(i)