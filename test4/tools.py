# tools.py
from robotmotion import uFactory_xArm

#--- FUNCTIONS OF THE ROBOT TO CALL ---
    
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

#----------------------------------

