# motiontests.py
from tools import connect_to_robot, go_home, go_offsethome, pick_sample_from_bed, place_sample_to_bed
from robotmotion import uFactory_xArm

connect_to_robot()
uFactory_xArm.move_to(uFactory_xArm.sample2)


'''
if __name__ == "__main__":
    arm = uFactory_xArm.connect()
    
    uFactory_xArm.go_home(arm)
    uFactory_xArm.move_forward(arm, dx=50)   # +50 mm X
    time.sleep(1)
    uFactory_xArm.move_backward(arm, dx=50)  # -50 mm X
'''

'''
if __name__ == "__main__":
    arm = uFactory_xArm.connect()
    uFactory_xArm.move_to(uFactory_xArm.leavehome)
    uFactory_xArm.move_to(uFactory_xArm.sample2above)
    uFactory_xArm.gripper_open(arm)
    uFactory_xArm.move_to(uFactory_xArm.sample2)
    uFactory_xArm.gripper_close(arm)
    uFactory_xArm.move_to(uFactory_xArm.sample2above)
    uFactory_xArm.move_to(uFactory_xArm.sample2)
    uFactory_xArm.gripper_open(arm)
    uFactory_xArm.move_to(uFactory_xArm.sample2above)
    uFactory_xArm.move_to(uFactory_xArm.leavehome)
    uFactory_xArm.gripper_close(arm)
    uFactory_xArm.go_home(arm)
'''

'''
if __name__ == "__main__":
    arm = uFactory_xArm.connect()
    uFactory_xArm.move_to(uFactory_xArm.leavehome)
    uFactory_xArm.move_to(uFactory_xArm.sample1above)
'''

'''
if __name__ == "__main__":
    arm = uFactory_xArm.connect()
    uFactory_xArm.move_to(uFactory_xArm.leavehome)
    uFactory_xArm.pick_sample_from_bed(2, arm)
    uFactory_xArm.place_sample_to_bed(2, arm)
    uFactory_xArm.pick_sample_from_bed(3, arm)
    uFactory_xArm.place_sample_to_bed(4, arm)
    uFactory_xArm.move_to(uFactory_xArm.leavehome)
    uFactory_xArm.go_home(arm)
'''

'''
if __name__ == "__main__":
    arm = uFactory_xArm.connect()
    uFactory_xArm.move_to(uFactory_xArm.leavehome)
    uFactory_xArm.move_to(uFactory_xArm.sample5above)
    uFactory_xArm.move_to(uFactory_xArm.leavehome)
    uFactory_xArm.go_home(arm)
'''
'''
if __name__ == "__main__":
    arm = uFactory_xArm.connect()
    uFactory_xArm.move_to(uFactory_xArm.leavehome)
    uFactory_xArm.move_to(uFactory_xArm.sample3above)
    uFactory_xArm.gripper_open(arm)
    uFactory_xArm.move_to(uFactory_xArm.sample3)

User: grab sample four
Assistant: {"name":"pick_sample_from_bed","arguments":{"i":4}}
User: put it back
Assistant: {"name":"place_sample_to_bed","arguments":{"i":4}}
'''


