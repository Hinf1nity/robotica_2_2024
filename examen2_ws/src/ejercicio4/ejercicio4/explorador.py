import numpy as np
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist


class Explorador(Node):
    def __init__(self):
        super().__init__('explorador')
        self.subscription = self.create_subscription(
            LaserScan,
            '/base_scan',
            self.listener_callback,
            10)
        self.publisher = self.create_publisher(Twist, '/cmd_vel', 10)
        self.timer = self.create_timer(0.5, self.timer_callback)
        self.giro = 0
        self.count = 0

    def listener_callback(self, msg):
        cmd_vel = Twist()
        self.ranges = msg.ranges
        front_range = msg.ranges[108:162]
        front_avg = min(front_range)
        left_range = msg.ranges[0:54]
        left_avg = sum(left_range) / len(left_range)
        right_range = msg.ranges[162:216]
        right_avg = sum(right_range) / len(right_range)

        if self.giro != 1:
            if front_avg < 0.7 and right_avg > left_avg:
                cmd_vel.linear.x = 0.025
                cmd_vel.angular.z = 0.5  # Gira a la derecha cuando hay un obstáculo al frente

            elif front_avg < 0.7 and right_avg < left_avg:
                cmd_vel.linear.x = 0.01
                cmd_vel.angular.z = -0.5

            else:
                cmd_vel.linear.x = 0.5
                # Ajusta el giro de acuerdo con la proximidad a las paredes
                if left_avg < 0.705:
                    # Gira hacia la derecha si está muy cerca de la pared izquierda
                    cmd_vel.angular.z = 0.275
                elif right_avg < 0.7:
                    # Gira hacia la izquierda si está muy cerca de la pared derecha
                    cmd_vel.angular.z = -0.25
                else:
                    cmd_vel.angular.z = 0.0  # Avanza recto si no hay obstáculos cercanos

        else:
            cmd_vel.linear.x = 0.0
            cmd_vel.angular.z = -0.5
            print('Girando')

        if left_avg > 2.5 and self.giro == 0:
            self.giro = 1
            self.count = 0
            cmd_vel.linear.x = 0.0
            cmd_vel.angular.z = 0.
            self.timer.reset()

        self.publisher.publish(cmd_vel)
        self.get_logger().info('Front: %f, Left: %f, Right: %f' %
                               (front_avg, left_avg, right_avg))

    def timer_callback(self):
        if self.giro != 0:
            self.count += 1
            if self.count == 6:
                self.giro = 2
                print('Giro completado')
            if self.count == 16:
                self.giro = 0
                self.count = 0
                print('giro = 0')


def main(args=None):
    rclpy.init(args=args)
    explorador = Explorador()
    rclpy.spin(explorador)
    explorador.destroy_node()
    rclpy.shutdown()
