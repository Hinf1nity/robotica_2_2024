import rclpy
from rclpy.node import Node
from nav_msgs.msg import OccupancyGrid


class NodoMap(Node):
    def __init__(self):
        super().__init__('nodo_map')
        self.subscription = self.create_subscription(
            OccupancyGrid,
            '/map',
            self.listener_callback,
            10)

    def listener_callback(self, msg):
        self.get_logger().info('Mapa recibido: %d x %d celdas' %
                               (msg.info.width, msg.info.height))
        self.get_logger().info('Resolución: %f' % msg.info.resolution)
        self.get_logger().info('Origen: %f, %f' %
                               (msg.info.origin.position.x, msg.info.origin.position.y))


def main(args=None):
    rclpy.init(args=args)
    nodo_map = NodoMap()
    rclpy.spin(nodo_map)
    nodo_map.destroy_node()
    rclpy.shutdown()
