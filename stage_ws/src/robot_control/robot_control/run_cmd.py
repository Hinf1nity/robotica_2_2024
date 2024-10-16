import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


class CmdVelPublisher(Node):
    def __init__(self):
        super().__init__('cmd_vel_publisher_node')
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)

    def timer_callback(self):
        msg = Twist()

        # Set linear and angular velocity (example values)
        msg.linear.x = 0.5  # Move forward with 0.5 m/s
        msg.angular.z = 0.2  # Rotate with 0.2 rad/s

        # Publish the velocity command
        self.publisher_.publish(msg)

        # Log the message for debugging
        self.get_logger().info(
            f'Publishing cmd_vel: linear.x={msg.linear.x}, angular.z={msg.angular.z}')


def main(args=None):
    rclpy.init(args=args)

    # Create the CmdVelPublisher node and spin it
    node = CmdVelPublisher()
    rclpy.spin(node)

    # Clean up on shutdown
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
