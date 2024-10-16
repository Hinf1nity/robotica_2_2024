import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/integralmilk03/robotica_2_2024/examen2_ws/install/ejercicio4'
