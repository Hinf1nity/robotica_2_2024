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

    def send_request(self, a, b, c, d, e):
        self.req.th1 = a
        self.req.th2 = b
        self.req.th3 = c
        self.req.l1 = d
        self.req.l2 = e
        return self.cli.call_async(self.req)


def main():
    rclpy.init()

    minimal_client = MinimalClientAsync()
    future = minimal_client.send_request(float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5]))
    rclpy.spin_until_future_complete(minimal_client, future)
    response = future.result()
    minimal_client.get_logger().info(
        'From: th1=%d, th2=%d, th3=%d, l1=%f, l2=%f\nResult: x=%f, y=%f, z=%f' %
        (float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5]), response.x, response.y, response.z))

    minimal_client.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()