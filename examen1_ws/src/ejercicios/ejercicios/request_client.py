import sys

from custom_interface.srv import StringService
import rclpy
from rclpy.node import Node


class MinimalClientAsync(Node):

    def __init__(self):
        super().__init__('minimal_client_async')
        self.cli = self.create_client(StringService, 'change_led')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        self.req = StringService.Request()

    def send_request(self, a):
        self.req.a = a
        return self.cli.call_async(self.req)


def main():
    rclpy.init()

    minimal_client = MinimalClientAsync()
    future = minimal_client.send_request(int(sys.argv[1]))
    rclpy.spin_until_future_complete(minimal_client, future)
    response = future.result()
    minimal_client.get_logger().info(
        'Number: %d\nState change to %s' %
        (int(sys.argv[1]), response.response))

    minimal_client.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()