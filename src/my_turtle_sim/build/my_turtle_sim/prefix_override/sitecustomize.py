import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/agro/ROS2/src/my_turtle_sim/install/my_turtle_sim'
