from custom_interface.srv import StringService
import requests
import sys
import rclpy
from rclpy.node import Node

class MinimalService(Node):

    def __init__(self, ip):
        super().__init__('minimal_service')
        self.srv =  self.create_service(StringService, 'change_led', self.change_state_callback)
        self.ip = ip

    def change_state_callback(self, req, res):
        if req.a == 0:
            res.response = 'off'
            self.send_request(self.ip, 'off')
        elif req.a == 1:
            res.response = 'on'
            self.send_request(self.ip, 'on')
        else:
            res.response = 'error'

        self.get_logger().info('Incoming request: %d' % (req.a))

        return res
    
    def send_request(self, url, data):
        try:
            response = requests.get(f'http://{url}/{data}')
            print(response.text)
        except requests.exceptions.RequestException as e:
            print("Error: {}".format(e))


def main():
    rclpy.init()
    min_svc = MinimalService(str(sys.argv[1]))
    rclpy.spin(min_svc)
    rclpy.shutdown()


if __name__ == '__main__':
    main()