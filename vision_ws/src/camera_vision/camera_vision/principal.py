import lgpio
import rclpy
import serial
from rclpy.node import Node
from std_msgs.msg import Int32


class Principal(Node):
    def __init__(self):
        super().__init__('principal')
        self.subscription = self.create_subscription(
            Int32,
            'action',
            self.listener_callback,
            10)
        self.subscription
        self.h = lgpio.gpiochip_open(0)
        self.motor_1 = 17
        self.motor_2 = 18
        lgpio.gpio_claim_output(self.h, self.motor_1)
        lgpio.gpio_claim_output(self.h, self.motor_2)
        self.ser = serial.Serial('/dev/ttyACM0', 9600)
        self.action = 1
        self.pos_angular = 0

    def listener_callback(self, msg):
        self.get_logger().info('Receiving action')
        if msg.data > 1 and self.action < 2:
            self.action = msg.data
            self.ser.reset_input_buffer()
            if self.ser.in_waiting > 0:
                self.pos_angular = float(self.ser.readline().decode('utf-8'))

        if self.action == 1:
            self.mover_robot(self.action)
        else:
            self.control_giro()

    def mover_robot(self, action):
        if action == 1:
            lgpio.gpio_write(self.h, self.motor_1, 1)
            lgpio.gpio_write(self.h, self.motor_2, 1)
        elif action == 2:
            lgpio.gpio_write(self.h, self.motor_1, 0)
            lgpio.gpio_write(self.h, self.motor_2, 1)
        elif action == 3 or action == 4:
            lgpio.gpio_write(self.h, self.motor_1, 1)
            lgpio.gpio_write(self.h, self.motor_2, 0)
        else:
            lgpio.gpio_write(self.h, self.motor_1, 0)
            lgpio.gpio_write(self.h, self.motor_2, 0)

    def control_giro(self):
        self.ser.reset_input_buffer()
        if self.ser.in_waiting > 0:
            angulo = float(self.ser.readline().decode('utf-8'))
            if self.action == 4:
                if abs(angulo - self.pos_angular) >= 180:
                    self.enviar_datos("5")
                    self.action = 0
            elif abs(angulo - self.pos_angular) >= 90:
                self.enviar_datos("5")
                self.action = 0
        self.mover_robot(self.action)

    def enviar_datos(self, action):
        self.ser.write(action)


def main(args=None):
    rclpy.init(args=args)
    principal = Principal()
    rclpy.spin(principal)
    rclpy.shutdown()
