#include <iostream>
#include <memory>

#include <rclcpp/rclcpp.hpp>
#include <moveit/move_group_interface/move_group_interface.h>

int main(int argc, char *argv[])
{
    // Initialize ROS and create the Node
    rclcpp::init(argc, argv);
    auto const node = std::make_shared<rclcpp::Node>(
        "joints_sequence",
        rclcpp::NodeOptions().automatically_declare_parameters_from_overrides(true));

    // Create a ROS logger
    auto const logger = rclcpp::get_logger("joints_sequence");

    // Create a MoveGroupInterface for the arm
    moveit::planning_interface::MoveGroupInterface move_group_interface(node, "panda_arm");
    std::vector<double> const target_joint_values_1 = {0.0, 0.0, 0.0, 0.0, 0.0, 3.14, 0.78};
    std::vector<double> const target_joint_values_2 = {0.0, 1.57, 0.0, 0.0, 0.0, 3.14, 0.78};
    int option;
    int option_past;

    while (true)
    {
        std::cout << "" << std::endl;
        std::cout << "Posición 1: {0.0, 0.0, 0.0, 0.0, 0.0, 3.14, 0.78}" << std::endl;
        std::cout << "Posición 2: {0.0, 1.57, 0.0, 0.0, 0.0, 3.14, 0.78}" << std::endl;
        std::cout << "Enter 1 or 2 to select a position for the panda arm and 3 to exit the program: ";
        std::cin >> option;
        if (option == option_past)
        {
            std::cout << "The arm is already in that position" << std::endl;
            continue;
        }
        if (option == 1)
        {
            // Set the target joint values
            move_group_interface.setJointValueTarget(target_joint_values_1);
        }
        else if (option == 2)
        {
            // Set the target joint values
            move_group_interface.setJointValueTarget(target_joint_values_2);
        }
        else if (option == 3)
        {
            break;
        }
        else
        {
            std::cout << "Invalid option" << std::endl;
            continue;
        }
        option_past = option;

        // Create a plan to that target pose
        auto const [success, plan] = [&move_group_interface]
        {
            moveit::planning_interface::MoveGroupInterface::Plan msg;
            auto const ok = static_cast<bool>(move_group_interface.plan(msg));
            return std::make_pair(ok, msg);
        }();

        // Execute the plan
        if (success)
        {
            move_group_interface.execute(plan);
        }
        else
        {
            RCLCPP_ERROR(logger, "Planing failed!");
        }
    }
    // Shutdown ROS
    rclcpp::shutdown();
    return 0;
}