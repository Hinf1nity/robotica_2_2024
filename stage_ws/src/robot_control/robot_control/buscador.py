import math
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import OccupancyGrid, Odometry
from geometry_msgs.msg import Twist, Pose


class AutoMapper(Node):

    def __init__(self):
        super().__init__('auto_mapper')

        # Suscribirse a los tópicos necesarios
        self.subscription_map = self.create_subscription(
            OccupancyGrid,
            '/map',
            self.map_callback,
            10)

        self.subscription_odom = self.create_subscription(
            Odometry,
            '/odom',
            self.odom_callback,
            10)

        self.subscription_scan = self.create_subscription(
            LaserScan,
            '/base_scan',
            self.scan_callback,
            10)

        self.publisher_cmd_vel = self.create_publisher(Twist, '/cmd_vel', 10)

        # Almacenar la información del mapa y del escaneo
        self.map_data = None
        self.map_info = None
        self.robot_pose = None
        self.scan_data = None

        self.frontier_threshold = 10  # Define cuándo una celda es una frontera no explorada
        self.safe_distance = 1.0  # Distancia mínima segura de obstáculos

    def map_callback(self, msg):
        self.map_data = msg.data
        self.map_info = msg.info
        self.get_logger().info('Mapa recibido.')

    def odom_callback(self, msg):
        # Obtener la posición del robot desde /odom
        self.robot_pose = msg.pose.pose
        self.get_logger().info(
            f'Posición actual: x={self.robot_pose.position.x}, y={self.robot_pose.position.y}')

    def scan_callback(self, msg):
        # Guardar los datos del escáner láser
        self.scan_data = msg.ranges

    def get_map_index(self, x, y):
        """
        Convierte coordenadas de mundo (x, y) en un índice unidimensional en el array del mapa OccupancyGrid.
        """
        map_x = int((x - self.map_info.origin.position.x) /
                    self.map_info.resolution)
        map_y = int((y - self.map_info.origin.position.y) /
                    self.map_info.resolution)
        index = map_y * self.map_info.width + map_x
        return index

    def is_frontier(self, index):
        """
        Determina si una celda en el mapa es una frontera no explorada.
        """
        print("Index: ", index)
        if self.map_data[index] == -1:
            # Comprobar si tiene al menos una celda adyacente libre (valor 0)
            width = self.map_info.width
            neighbors = [
                index + 1, index - 1,  # izquierda y derecha
                index + width, index - width  # arriba y abajo
            ]
            for neighbor in neighbors:
                if 0 <= neighbor < len(self.map_data) and self.map_data[neighbor] == 0:
                    return True
        return False

    def explore(self):
        """
        Explora el entorno buscando nuevas fronteras.
        """
        if self.robot_pose is None or self.map_data is None:
            self.get_logger().info("Esperando información de odometría y mapa...")
            return

        # Variables para controlar el movimiento
        cmd_msg = Twist()

        # Buscar fronteras no exploradas en el mapa
        for y in range(self.map_info.height):
            for x in range(self.map_info.width):
                index = y * self.map_info.width + x
                if self.is_frontier(index):
                    # Determinar la dirección para moverse hacia la frontera
                    frontier_x = x * self.map_info.resolution + self.map_info.origin.position.x
                    frontier_y = y * self.map_info.resolution + self.map_info.origin.position.y

                    # Controlar el movimiento del robot hacia esa frontera
                    cmd_msg.linear.x = 0.2  # Avanzar hacia la frontera
                    cmd_msg.angular.z = self.calculate_turn(
                        frontier_x, frontier_y)
                    self.publisher_cmd_vel.publish(cmd_msg)
                    self.get_logger().info(
                        f'Moviéndose hacia la frontera en x={frontier_x}, y={frontier_y}')
                    return

    def calculate_turn(self, target_x, target_y):
        """
        Calcula el giro necesario para que el robot se oriente hacia una meta.
        """
        if self.robot_pose is None:
            return 0.0

        # Convertir la orientación del robot de cuaternión a ángulos de Euler (roll, pitch, yaw)
        q = self.robot_pose.orientation
        siny_cosp = 2 * (q.w * q.z + q.x * q.y)
        cosy_cosp = 1 - 2 * (q.y * q.y + q.z * q.z)
        x = math.atan2(siny_cosp, cosy_cosp)
        y = math.asin(2 * (q.w * q.y - q.z * q.x))

        # Calcular el ángulo hacia la meta
        dx = target_x - x
        dy = target_y - y
        target_angle = math.atan2(dy, dx)

        # Obtener el ángulo actual del robot
        robot_orientation = self.robot_pose.orientation
        robot_angle = 2 * math.atan2(robot_orientation.z, robot_orientation.w)

        # Calcular la diferencia angular
        angle_diff = target_angle - robot_angle

        # Ajustar el giro del robot para que apunte hacia la meta
        return 0.5 * angle_diff

    def avoid_obstacles(self):
        """
        Control básico de evasión de obstáculos basado en datos de escaneo láser.
        """
        if self.scan_data is None:
            return False  # No hay datos de escaneo

        # Si el robot está demasiado cerca de un obstáculo, evadir
        front_range = self.scan_data[108:162]
        left_range = self.scan_data[162:216]
        back_range = self.scan_data[109:162]
        right_range = self.scan_data[54:108]
        front_left_range = self.scan_data[217:270]

        min_distance = min(front_range)

        if min_distance < self.safe_distance:
            cmd_msg = Twist()
            cmd_msg.linear.x = 0.0  # Detener avance
            cmd_msg.angular.z = 0.5  # Girar para evitar el obstáculo
            self.publisher_cmd_vel.publish(cmd_msg)
            self.get_logger().info(
                f'Evadiendo obstáculo a {min_distance} metros.')
            return True

        return False


def main(args=None):
    rclpy.init(args=args)

    auto_mapper = AutoMapper()

    try:
        while rclpy.ok():
            rclpy.spin_once(auto_mapper)
            if not auto_mapper.avoid_obstacles():  # Evitar obstáculos si es necesario
                auto_mapper.explore()  # Si no hay obstáculos, continuar explorando
    except KeyboardInterrupt:
        pass
    finally:
        auto_mapper.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()


# # Dividimos el LIDAR en 5 secciones
#         front_range = msg.ranges[108:162]
#         left_range = msg.ranges[162:216]
#         back_range = msg.ranges[109:162]
#         right_range = msg.ranges[54:108]
#         front_left_range = msg.ranges[217:270]
