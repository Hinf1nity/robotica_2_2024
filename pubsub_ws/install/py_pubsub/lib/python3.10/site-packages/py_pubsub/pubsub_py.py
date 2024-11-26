import rclpy
from rclpy.node import Node

from std_msgs.msg import String


class MinimalPublisherSubscriber(Node):

    def __init__(self):
        super().__init__('pubsub_python')
        self.subscription = self.create_subscription(
            String,
            'topico_pubsub_python',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning
        self.publisher_ = self.create_publisher(String, 'topico_python', 10)
        self.i = 0

    def listener_callback(self, msg):
        self.get_logger().info('I heard in python: "%s"' % msg.data)
        self.publisher_.publish(msg)
        self.i += 1


def main(args=None):
    rclpy.init(args=args)

    minimal_publisher_subscriber = MinimalPublisherSubscriber()

    rclpy.spin(minimal_publisher_subscriber)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_publisher_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
