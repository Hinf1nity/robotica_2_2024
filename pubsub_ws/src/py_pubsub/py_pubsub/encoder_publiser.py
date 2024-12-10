
import rclpy
import serial
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray, Int8MultiArray


class EncoderPublisher(Node):
    def __init__(self):
        super().__init__('encoder_publisher')
        self.publisher = self.create_publisher(Int8MultiArray, 'encoders', 10)
        self.subscription = self.create_subscription(
            Float32MultiArray, 'vel_arduino', self.velocity, 10)

        self.timer = self.create_timer(
            0.1, self.publish_encoder_states)  # 10 Hz
        self.ser = serial.Serial('/dev/ttyUSB0', 115200)
        self.left_position = 0.0
        self.right_position = 0.0
        self.left_speed = 0
        self.right_speed = 0

    def velocity(self, msg):
        # Actualiza la velocidad de los motores
        self.left_speed = float(msg.data[0])
        self.right_speed = float(msg.data[1])

    def publish_encoder_states(self):
        msg = Float32MultiArray()
        msg_arduino = str(self.left_speed)+" "+str(self.right_speed)+"\n"
        self.ser.write(msg_arduino.encode())
        data = self.ser.readline().decode().split()
        self.left_position = float(data[0])
        self.right_position = float(data[1])
        msg.data = [self.left_position, self.right_position]
        self.publisher.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    encoder_publisher = EncoderPublisher()
    rclpy.spin(encoder_publisher)
    encoder_publisher.destroy_node()
    rclpy.shutdown()
