
#ifndef DIFF_DRIVE_HARDWARE_HPP
#define DIFF_DRIVE_HARDWARE_HPP

#include "hardware_interface/types/hardware_interface_type_values.hpp"
#include <algorithm>
#include <chrono>
#include <hardware_interface/system_interface.hpp>
#include <mutex>
#include <pluginlib/class_list_macros.hpp>
#include <rclcpp/rclcpp.hpp>
#include <std_msgs/msg/float32_multi_array.hpp>
#include <std_msgs/msg/int8_multi_array.hpp>
#include <vector>

class DiffDriveHardware : public hardware_interface::SystemInterface,
                          public rclcpp::Node {
public:
  DiffDriveHardware();
  hardware_interface::CallbackReturn
  on_init(const hardware_interface::HardwareInfo &info) override;
  std::vector<hardware_interface::StateInterface>
  export_state_interfaces() override;
  std::vector<hardware_interface::CommandInterface>
  export_command_interfaces() override;
  hardware_interface::return_type read(const rclcpp::Time &time,
                                       const rclcpp::Duration &period) override;
  hardware_interface::return_type
  write(const rclcpp::Time &time, const rclcpp::Duration &period) override;

private:
  void encoder_callback(const std_msgs::msg::Int8MultiArray::SharedPtr msg);

  rclcpp::Subscription<std_msgs::msg::Int8MultiArray>::SharedPtr encoder_sub_;
  rclcpp::Publisher<std_msgs::msg::Float32MultiArray>::SharedPtr velocity_pub_;
  std::mutex encoder_mutex_;
  std::vector<int8_t> encoder_data_{0, 0};

  double left_position_;
  double right_position_;
  double left_velocity_;
  double right_velocity_;
  double left_velocity_command_;
  double right_velocity_command_;
  double left_wheel_velocity_min_;
  double left_wheel_velocity_max_;
  double right_wheel_velocity_min_;
  double right_wheel_velocity_max_;
  std::chrono::time_point<std::chrono::system_clock> time_;

  static constexpr double ENCODER_RESOLUTION = 0.14271;
};

#endif // DIFF_DRIVE_HARDWARE_HPP
