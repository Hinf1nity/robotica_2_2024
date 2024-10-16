import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
import math


class Giro90(Node):
    def __init__(self):
        super().__init__('giro_90')
        self.subscription_odom = self.create_subscription(
            Odometry,
            '/odom',
            self.listener_callback_odom,
            10)
        self.publisher = self.create_publisher(Twist, '/cmd_vel', 10)
        self.timer = self.create_timer(0.1, self.timer_callback)
        self.giro = 0
        self.position = 0.
        self.position_next = 0.

    def listener_callback_odom(self, msg):
        x = msg.pose.pose.position.x
        y = msg.pose.pose.position.y
        orientation_q = msg.pose.pose.orientation
        _, _, yaw = self.euler_from_quaternion(
            orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w)
        self.position = yaw

    def euler_from_quaternion(self, x, y, z, w):
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

    def timer_callback(self):
        cmd_vel = Twist()
        print('Posición: ', self.position)
        print('Posición siguiente: ', self.position_next)
        if self.giro == 0:
            self.position_next = self.position - math.pi/2
            cmd_vel.linear.x = 0.0
            cmd_vel.angular.z = -0.5
            self.publisher.publish(cmd_vel)
            self.giro = 1
            print('Giro: ', self.position_next)

        elif self.position <= self.position_next:
            cmd_vel.linear.x = 0.0
            cmd_vel.angular.z = 0.0
            self.publisher.publish(cmd_vel)
            print('Giro completado 1')

        elif self.giro == 1:
            cmd_vel.linear.x = 0.0
            cmd_vel.angular.z = -0.5
            self.publisher.publish(cmd_vel)

        else:
            cmd_vel.linear.x = 0.0
            cmd_vel.angular.z = 0.0
            self.publisher.publish(cmd_vel)
            print('Giro completado')


def main(args=None):
    rclpy.init(args=args)
    giro_90 = Giro90()
    rclpy.spin(giro_90)
    giro_90.destroy_node()
    rclpy.shutdown()
