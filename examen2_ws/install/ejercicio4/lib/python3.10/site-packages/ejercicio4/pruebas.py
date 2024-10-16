import numpy as np
from nav_msgs.msg import Odometry, OccupancyGrid
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
import math


class Explorador(Node):
    def __init__(self):
        super().__init__('explorador')
        self.subscription = self.create_subscription(
            LaserScan,
            '/base_scan',
            self.listener_callback,
            10)
        self.subscription_odom = self.create_subscription(
            Odometry,
            '/odom',
            self.listener_callback_odom,
            10)
        self.publisher = self.create_publisher(Twist, '/cmd_vel', 10)
        self.timer = self.create_timer(3, self.timer_callback)
        self.giro = 0
        self.position = 0
        self.position_next = 0

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
            if front_avg < 0.7:
                cmd_vel.linear.x = 0.0
                cmd_vel.angular.z = -0.5  # Gira a la derecha cuando hay un obstáculo al frente
            else:
                cmd_vel.linear.x = 0.5
                # Ajusta el giro de acuerdo con la proximidad a las paredes
                if left_avg < 0.5:
                    # Gira hacia la derecha si está muy cerca de la pared izquierda
                    cmd_vel.angular.z = 0.5
                elif right_avg < 0.5:
                    # Gira hacia la izquierda si está muy cerca de la pared derecha
                    cmd_vel.angular.z = -0.5
                else:
                    cmd_vel.angular.z = 0.0  # Avanza recto si no hay obstáculos cercanos

        else:
            cmd_vel.linear.x = 0.0
            cmd_vel.angular.z = -0.5
            print('Girando')

        if left_avg > 2.5 and self.giro == 0:
            self.giro = 1
            self.position_next = self.position - math.pi/2
            print('Giro: ', self.position_next)

        angle1 = self.pi_2_2pi(self.position)
        print('Posición: ', angle1)
        angle2 = self.pi_2_2pi(self.position_next)

        if angle1 <= angle2 and self.giro == 1:
            self.giro = 2
            self.timer.reset()

        self.publisher.publish(cmd_vel)
        self.get_logger().info('Front: %f, Left: %f, Right: %f' %
                               (front_avg, left_avg, right_avg))

    def pi_2_2pi(self, angle):
        normalized_angle = (angle + math.pi) % (2 * math.pi)
        if normalized_angle < 0:
            normalized_angle += 2 * math.pi
        return normalized_angle

    def listener_callback_odom(self, msg):
        x = msg.pose.pose.position.x
        y = msg.pose.pose.position.y
        orientation_q = msg.pose.pose.orientation
        _, _, yaw = self.euler_from_quaternion(
            orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w)
        self.position = yaw
        self.get_logger().info('Posición: x=%f, y=%f, yaw=%f' % (x, y, yaw))

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
        if self.giro == 2:
            self.giro = 0


def main(args=None):
    rclpy.init(args=args)
    explorador = Explorador()
    rclpy.spin(explorador)
    explorador.destroy_node()
    rclpy.shutdown()


# 3

# 333


class ExploradorFloodFillMap(Node):
    def __init__(self):
        super().__init__('explorador_flood_fill_map')

        # Subscripción al mapa y odometría
        self.map_subscription = self.create_subscription(
            OccupancyGrid,
            '/map',
            self.map_callback,
            10)

        self.odom_subscription = self.create_subscription(
            Odometry,
            '/odom',
            self.odom_callback,
            10)

        self.publisher = self.create_publisher(Twist, '/cmd_vel', 10)

        # Variables de estado
        self.map_data = None
        self.resolution = 0.0
        self.origin = (0.0, 0.0)
        self.visited = set()  # Celdas visitadas
        self.stack = []  # Pila para flood fill
        self.position = (0, 0)  # Posición inicial del robot

    def map_callback(self, msg):
        """Callback para obtener el mapa del entorno."""
        self.map_data = np.array(msg.data).reshape(
            (msg.info.height, msg.info.width))
        self.resolution = msg.info.resolution
        self.origin = (msg.info.origin.position.x, msg.info.origin.position.y)

        # Convertir posición actual a coordenadas de la grilla
        current_cell = self.to_grid_coords(self.position[0], self.position[1])

        # Iniciar flood fill si no hay celdas en la pila
        if not self.stack:
            self.stack.append(current_cell)

        # Ejecutar Flood Fill para explorar el mapa
        self.flood_fill()

    def odom_callback(self, msg):
        """Callback de odometría para actualizar la posición del robot."""
        x = msg.pose.pose.position.x
        y = msg.pose.pose.position.y
        orientation_q = msg.pose.pose.orientation
        _, _, yaw = self.euler_from_quaternion(
            orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w)
        self.position = (x, y, yaw)

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

    def flood_fill(self):
        """Ejecuta el algoritmo Flood Fill usando el mapa y la odometría."""
        if self.stack and self.map_data is not None:
            # Obtener la celda actual
            cell = self.stack.pop()

            # Convertir la celda a posición en el mapa
            if cell not in self.visited:
                self.visited.add(cell)

                # Buscar las celdas vecinas
                neighbors = [
                    (cell[0] + 1, cell[1]),   # derecha
                    (cell[0] - 1, cell[1]),   # izquierda
                    (cell[0], cell[1] + 1),   # abajo
                    (cell[0], cell[1] - 1)    # arriba
                ]

                for neighbor in neighbors:
                    if self.is_cell_unexplored(neighbor) and neighbor not in self.visited:
                        self.stack.append(neighbor)

                # Mover el robot hacia la siguiente celda
            self.move_to_next_cell(cell)

    def is_cell_unexplored(self, cell):
        """Verifica si una celda no ha sido explorada."""
        # Obtener el valor de la celda en el mapa
        x, y = cell
        if 0 <= x < self.map_data.shape[0] and 0 <= y < self.map_data.shape[1]:
            # Celdas no exploradas en el mapa ocupacional suelen tener valor -1
            return self.map_data[x, y] == -1
        return False

    def move_to_next_cell(self, cell):
        """Controla el movimiento del robot hacia una nueva celda."""
        target_position = self.to_world_coords(cell[0], cell[1])
        current_position = self.position  # La posición actual del robot

        # Calcular el ángulo hacia la celda objetivo
        angle_to_target = math.atan2(target_position[1] - current_position[1],
                                     target_position[0] - current_position[0])

        # Obtener la orientación actual del robot (asumimos que tienes orientación en el callback de odometría)
        current_orientation = self.position[2]

        # Calcula la diferencia angular
        angular_error = self.normalize_angle(
            angle_to_target - current_orientation)

        # Si el ángulo de error es significativo, girar el robot
        if abs(angular_error) > 0.1:  # Si la diferencia angular es mayor a 0.1 radianes
            cmd_vel = Twist()
            cmd_vel.angular.z = 0.5 if angular_error > 0 else - \
                0.5  # Girar en la dirección correcta
            self.publisher.publish(cmd_vel)
        else:
            # Una vez alineado, avanzar hacia la celda objetivo
            cmd_vel = Twist()
            cmd_vel.linear.x = 0.5  # Avanza hacia adelante
            self.publisher.publish(cmd_vel)

    def normalize_angle(self, angle):
        """Normaliza un ángulo para que esté entre -pi y pi."""
        while angle > math.pi:
            angle -= 2 * math.pi
        while angle < -math.pi:
            angle += 2 * math.pi
        return angle

    def to_grid_coords(self, x, y):
        """Convierte coordenadas del mundo real a coordenadas de la grilla (mapa)."""
        grid_x = int((x - self.origin[0]) / self.resolution)
        grid_y = int((y - self.origin[1]) / self.resolution)
        return (grid_x, grid_y)

    def to_world_coords(self, grid_x, grid_y):
        """Convierte coordenadas de la grilla a coordenadas del mundo real."""
        x = grid_x * self.resolution + self.origin[0]
        y = grid_y * self.resolution + self.origin[1]
        return (x, y)


def main(args=None):
    rclpy.init(args=args)
    explorador = ExploradorFloodFillMap()
    rclpy.spin(explorador)
    explorador.destroy_node()
    rclpy.shutdown()
