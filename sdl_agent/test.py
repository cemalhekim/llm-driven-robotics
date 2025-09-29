from tools import *
from robotmotion import *

uFactory_xArm.connect()

ocp_measurement(2)
ca_measurement(1)
bring_sample_to_user(1)
collect_sample_from_user(1)