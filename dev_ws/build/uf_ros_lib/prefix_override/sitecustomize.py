import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/ch/Workspace/llm-driven-robotics/dev_ws/install/uf_ros_lib'
