from custom_interface.srv import GetPosition

import rclpy
import sympy as sp
from rclpy.node import Node


class MinimalService(Node):

    def __init__(self):
        super().__init__('minimal_service')
        self.srv = self.create_service(
            GetPosition, 'add_thee_ints', self.add_numbers_callback)
        self.th1, self.th2, self.th3, self.L1, self.L2 = sp.symbols(
            'th1 th2 th3 L1 L2')
        self.matrices()

    def add_numbers_callback(self, req, res):
        Tf = self.M_simplified.subs(
            {self.th1: req.th1, self.th2: req.th2, self.th3: req.th3, self.L1: req.l1, self.L2: req.l2})
        res.x = float(Tf[0])
        res.y = float(Tf[1])
        res.z = float(Tf[2])

        self.get_logger().info('Incoming request\nth1: %f th2: %f th3: %f l1: %f l2: %f' %
                               (req.th1, req.th2, req.th3, req.l1, req.l2))

        return res

    def matrices(self):
        Ry1 = sp.Matrix([
            [sp.cos(-self.th2), 0, sp.sin(-self.th2), 0],
            [0, 1, 0, 0],
            [-sp.sin(-self.th2), 0, sp.cos(-self.th2), 0],
            [0, 0, 0, 1]
        ])

        Rx1 = sp.Matrix([
            [1, 0, 0, 0],
            [0, sp.cos(self.th1), -sp.sin(self.th1), 0],
            [0, sp.sin(self.th1), sp.cos(self.th1), 0],
            [0, 0, 0, 1]
        ])

        Tz1 = sp.Matrix([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, -self.L1],
            [0, 0, 0, 1]

        ])

        Ry2 = sp.Matrix([
            [sp.cos(-self.th3), 0, sp.sin(-self.th3), 0],
            [0, 1, 0, 0],
            [-sp.sin(-self.th3), 0, sp.cos(-self.th3), 0],
            [0, 0, 0, 1]
        ])

        Tz2 = sp.Matrix([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, -self.L2],
            [0, 0, 0, 1]
        ])
        M = Rx1 * Ry1 * Tz1 * Ry2 * Tz2
        self.M_simplified = sp.simplify(M * sp.Matrix([0, 0, 0, 1]))


def main():
    rclpy.init()
    min_svc = MinimalService()
    rclpy.spin(min_svc)
    rclpy.shutdown()


if __name__ == '__main__':
    main()
