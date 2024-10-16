#include <iostream>
#include <memory>
#include <rclcpp/rclcpp.hpp>
#include <moveit/move_group_interface/move_group_interface.h>
#include <moveit/planning_scene_interface/planning_scene_interface.h>
#include <geometric_shapes/shape_operations.h>
#include <shape_msgs/msg/solid_primitive.hpp>
#include <moveit_msgs/msg/collision_object.hpp>

int main(int argc, char * argv[]) {
  // Inicializar ROS y crear el nodo
  rclcpp::init(argc, argv);
  auto const node = std::make_shared<rclcpp::Node>(
    "ejercicio2",
    rclcpp::NodeOptions().automatically_declare_parameters_from_overrides(true)
  );

  // Crear un logger de ROS
  auto const logger = rclcpp::get_logger("ejercicio2");

  // Crear la interfaz MoveGroup
  static const std::string PLANNING_GROUP = "panda_arm";
  moveit::planning_interface::MoveGroupInterface move_group(node, PLANNING_GROUP);

  int opcion = 0;
  do {
    // Mostrar el menú
    std::cout << "Seleccione una opción:\n";
    std::cout << "1. Ejecutar primer movimiento\n";
    std::cout << "2. Ejecutar segundo movimiento\n";
    std::cout << "3. Salir\n";
    std::cout << "Opción: ";
    std::cin >> opcion;

    if (opcion == 1) {
      // Primer Movimiento
      geometry_msgs::msg::Pose target_pose;
      target_pose.orientation.w = 1.0;
      target_pose.position.x = -0.58;
      target_pose.position.y = 0.2;
      target_pose.position.z = 0.5;
      move_group.setPoseTarget(target_pose);

      moveit::planning_interface::MoveGroupInterface::Plan my_plan;
      bool success = (move_group.plan(my_plan) == moveit::planning_interface::MoveItErrorCode::SUCCESS);

      if (success) {
        RCLCPP_INFO(logger, "Plan successful for first move, executing...");
        move_group.execute(my_plan);
      } else {
        RCLCPP_ERROR(logger, "Planning failed for first move!");
      }
    } 
    else if (opcion == 2) {
      // Segundo Movimiento
      geometry_msgs::msg::Pose second_pose;
      second_pose.orientation.w = 0.0;
      second_pose.position.x = 0.1;
      second_pose.position.y = 0.1;
      second_pose.position.z = 0.7;
      move_group.setPoseTarget(second_pose);

      moveit::planning_interface::MoveGroupInterface::Plan second_plan;
      bool success = (move_group.plan(second_plan) == moveit::planning_interface::MoveItErrorCode::SUCCESS);

      if (success) {
        RCLCPP_INFO(logger, "Plan successful for second move, executing...");
        move_group.execute(second_plan);
      } else {
        RCLCPP_ERROR(logger, "Planning failed for second move!");
      }
    } 
    else if (opcion == 3) {
      std::cout << "Saliendo del programa...\n";
    } 
    else {
      std::cout << "Opción no válida, por favor intente nuevamente.\n";
    }
  } while (opcion != 3);

  // Finalizar ROS
  rclcpp::shutdown();
  return 0;
}
