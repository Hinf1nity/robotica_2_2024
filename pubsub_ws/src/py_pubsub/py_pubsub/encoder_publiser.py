
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState


class EncoderPublisher(Node):
    def __init__(self):
        super().__init__('encoder_publisher')
        self.publisher = self.create_publisher(JointState, '/joint_states', 10)
        self.timer = self.create_timer(0.1, self.publish_joint_states)  # 10 Hz
        self.left_position = 0.0
        self.right_position = 0.0

    def publish_joint_states(self):
        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.name = ['left_wheel_joint', 'right_wheel_joint']
        # Actualiza con datos de encoders
        msg.position = [self.left_position, self.right_position]
        msg.velocity = [0.1, 0.1]  # Opcional: velocidad angular en rad/s
        self.publisher.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    encoder_publisher = EncoderPublisher()
    rclpy.spin(encoder_publisher)
    encoder_publisher.destroy_node()
    rclpy.shutdown()
