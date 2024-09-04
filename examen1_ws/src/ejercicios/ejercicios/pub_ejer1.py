import rclpy
from rclpy.node import Node

from std_msgs.msg import Int8MultiArray


class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('publisher_python')
        self.publisher_ = self.create_publisher(Int8MultiArray, 'topico_ds', 10)
        timer_period = 3
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = Int8MultiArray()
        msg.data = list(map(int, f'{self.i:03b}'))
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%d" "%d "%d"' %(msg.data[0], msg.data[1], msg.data[2]))
        self.i += 1
        if self.i == 8:
            self.i = 0


def main(args=None):
    rclpy.init(args=args)
    minimal_publisher = MinimalPublisher()
    rclpy.spin(minimal_publisher)
    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
