import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/hinfinity/Documents/robotica_2_2024/vision_ws/install/camera_vision'
