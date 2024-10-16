import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan


class LidarSubscriber(Node):

    def __init__(self):
        super().__init__('lidar_subscriber')
        self.subscription = self.create_subscription(
            LaserScan,
            'base_scan',
            self.listener_callback,
            10)
        self.subscription

    def listener_callback(self, msg):
        self.get_logger().info('Received LIDAR scan data: %d points' % len(msg.ranges))
        right_distance = min(msg.ranges[0:89])
        front_distance = min(msg.ranges[90:179])
        left_distance = min(msg.ranges[180:269])
        print('Right distance: %s' % right_distance)
        print('Front distance: %s' % front_distance)
        print('Left distance: %s' % left_distance)
        self.get_logger().info('First range: %s' % msg.ranges[0])


def main(args=None):
    rclpy.init(args=args)

    lidar_subscriber = LidarSubscriber()

    rclpy.spin(lidar_subscriber)

    lidar_subscriber.destroy_node()
    rclpy.shutdown()
