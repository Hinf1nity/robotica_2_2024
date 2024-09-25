#include <memory>

#include <rclcpp/rclcpp.hpp>
#include <moveit/move_group_interface/move_group_interface.h>
#include <tf2/LinearMath/Quaternion.h>
int main(int argc, char *argv[])
{
    // Initialize ROS and create the Node
    rclcpp::init(argc, argv);
    auto const node = std::make_shared<rclcpp::Node>(
        "hello_moveit",
        rclcpp::NodeOptions().automatically_declare_parameters_from_overrides(true));

    // Create a ROS logger
    auto const logger = rclcpp::get_logger("hello_moveit");

    // Next step goes here
    // Create the MoveIt MoveGroup Interface
    using moveit::planning_interface::MoveGroupInterface;
    auto move_group_interface = MoveGroupInterface(node, "panda_arm");

    // Set a target Pose
    auto const target_pose = []
    {
        geometry_msgs::msg::Pose msg;
        tf2::Quaternion q;
        q.setRPY(3.142, 0, 0);
        msg.orientation.w = q.w();
        msg.orientation.x = q.x();
        msg.orientation.y = q.y();
        msg.orientation.z = q.z();
        msg.position.x = 0.295;
        msg.position.y = 0.284;
        msg.position.z = 0.138;
        return msg;
    }();
    move_group_interface.setPoseTarget(target_pose);

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

    // Add a new target pose
    auto const target_pose2 = []
    {
        geometry_msgs::msg::Pose msg;
        tf2::Quaternion q;
        q.setRPY(3.142, 0, 0);
        msg.orientation.w = q.w();
        msg.orientation.x = q.x();
        msg.orientation.y = q.y();
        msg.orientation.z = q.z();
        msg.orientation.w = 1.0;
        msg.position.x = 0.295;
        msg.position.y = -0.284;
        msg.position.z = 0.138;
        return msg;
    }();
    move_group_interface.setPoseTarget(target_pose2);

    // Create a plan to that target pose
    auto const [success2, plan2] = [&move_group_interface]
    {
        moveit::planning_interface::MoveGroupInterface::Plan msg;
        auto const ok = static_cast<bool>(move_group_interface.plan(msg));
        return std::make_pair(ok, msg);
    }();

    // Execute the plan
    if (success2)
    {
        move_group_interface.execute(plan2);
    }
    else
    {
        RCLCPP_ERROR(logger, "Planing 2 failed!");
    }

    // Shutdown ROS
    rclcpp::shutdown();
    return 0;
}
