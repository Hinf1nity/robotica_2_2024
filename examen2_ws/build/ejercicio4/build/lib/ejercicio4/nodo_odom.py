import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry


class NodoOdom(Node):
    def __init__(self):
        super().__init__('nodo_odom')
        self.subscription = self.create_subscription(
            Odometry,
            '/odom',
            self.listener_callback,
            10)

    def listener_callback(self, msg):
        x = msg.pose.pose.position.x
        y = msg.pose.pose.position.y
        orientation_q = msg.pose.pose.orientation
        _, _, yaw = self.euler_from_quaternion(
            orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w)
        self.get_logger().info('Posición: x=%f, y=%f, yaw=%f' % (x, y, yaw))

    def euler_from_quaternion(self, x, y, z, w):
        import math
        t0 = +2.0 * (w * x + y * z)
        t1 = +1.0 - 2.0 * (x * x + y * y)
        roll_x = math.atan2(t0, t1)

        t2 = +2.0 * (w * y - z * x)
        t2 = +1.0 if t2 > +1.0 else t2
        t2 = -1.0 if t2 < -1.0 else t2
        pitch_y = math.asin(t2)

        t3 = +2.0 * (w * z + x * y)
        t4 = +1.0 - 2.0 * (y * y + z * z)
        yaw_z = math.atan2(t3, t4)

        return roll_x, pitch_y, yaw_z


def main(args=None):
    rclpy.init(args=args)
    nodo_odom = NodoOdom()
    rclpy.spin(nodo_odom)
    nodo_odom.destroy_node()
    rclpy.shutdown()
