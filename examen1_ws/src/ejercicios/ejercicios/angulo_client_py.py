import sys

from custom_interface.srv import GetPosition
import rclpy
from rclpy.node import Node


class MinimalClientAsync(Node):

    def __init__(self):
        super().__init__('minimal_client_async')
        self.cli = self.create_client(GetPosition, 'add_thee_ints')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        self.req = GetPosition.Request()

    def send_request(self, d=69.5, e=71.5):
        self.angulos = [0., 0., 0.]
        self.req.angulos = self.angulos
        self.req.l1 = d
        self.req.l2 = e
        return self.cli.call_async(self.req)


def main():
    rclpy.init()

    minimal_client = MinimalClientAsync()
    future = minimal_client.send_request()
    rclpy.spin_until_future_complete(minimal_client, future)
    response = future.result()
    minimal_client.get_logger().info(
        'From: th1=%d, th2=%d, th3=%d\nResult: x=%f, y=%f, z=%f' %
        (minimal_client.angulos[0], minimal_client.angulos[1], minimal_client.angulos[2], response.x, response.y, response.z))

    minimal_client.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()