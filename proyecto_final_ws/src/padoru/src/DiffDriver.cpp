
#include "include/DiffDriver.h"

DiffDriveHardware::DiffDriveHardware()
    : Node("diff_drive_hardware"), left_position_(0.0), right_position_(0.0),
      left_velocity_(0.0), right_velocity_(0.0), left_velocity_command_(0.0),
      right_velocity_command_(0.0), left_wheel_velocity_min_(-18.0),
      left_wheel_velocity_max_(18.0), right_wheel_velocity_min_(-18.0),
      right_wheel_velocity_max_(18.0), time_(std::chrono::system_clock::now()) {
}

hardware_interface::CallbackReturn
DiffDriveHardware::on_init(const hardware_interface::HardwareInfo &info) {
  encoder_sub_ = this->create_subscription<std_msgs::msg::Int8MultiArray>(
      "encoders", 10,
      std::bind(&DiffDriveHardware::encoder_callback, this,
                std::placeholders::_1));

  velocity_pub_ = this->create_publisher<std_msgs::msg::Float32MultiArray>(
      "vel_arduino", 10);

  return hardware_interface::CallbackReturn::SUCCESS;
}

std::vector<hardware_interface::StateInterface>
DiffDriveHardware::export_state_interfaces() {
  std::vector<hardware_interface::StateInterface> state_interfaces;

  state_interfaces.emplace_back(hardware_interface::StateInterface(
      "left_wheel_joint", hardware_interface::HW_IF_POSITION, &left_position_));
  state_interfaces.emplace_back(hardware_interface::StateInterface(
      "left_wheel_joint", hardware_interface::HW_IF_VELOCITY, &left_velocity_));
  state_interfaces.emplace_back(hardware_interface::StateInterface(
      "right_wheel_joint", hardware_interface::HW_IF_POSITION,
      &right_position_));
  state_interfaces.emplace_back(hardware_interface::StateInterface(
      "right_wheel_joint", hardware_interface::HW_IF_VELOCITY,
      &right_velocity_));

  return state_interfaces;
}

std::vector<hardware_interface::CommandInterface>
DiffDriveHardware::export_command_interfaces() {
  std::vector<hardware_interface::CommandInterface> command_interfaces;

  command_interfaces.emplace_back(hardware_interface::CommandInterface(
      "left_wheel_joint", hardware_interface::HW_IF_VELOCITY,
      &left_velocity_command_));
  command_interfaces.emplace_back(hardware_interface::CommandInterface(
      "right_wheel_joint", hardware_interface::HW_IF_VELOCITY,
      &right_velocity_command_));

  return command_interfaces;
}

hardware_interface::return_type
DiffDriveHardware::read(const rclcpp::Time &time,
                        const rclcpp::Duration &period) {
  auto new_time = std::chrono::system_clock::now();
  std::chrono::duration<double> diff = new_time - time_;
  double dt = diff.count();
  time_ = new_time;

  std::lock_guard<std::mutex> lock(encoder_mutex_);
  double pos_prev = left_position_;
  left_position_ = encoder_data_[0] * ENCODER_RESOLUTION;
  right_velocity_ = (left_position_ - pos_prev) / dt;

  pos_prev = right_position_;
  right_position_ = encoder_data_[1] * ENCODER_RESOLUTION;
  right_velocity_ = (right_position_ - pos_prev) / dt;

  return hardware_interface::return_type::OK;
}

hardware_interface::return_type
DiffDriveHardware::write(const rclcpp::Time &time,
                         const rclcpp::Duration &period) {
  left_velocity_command_ =
      std::clamp(left_velocity_command_, left_wheel_velocity_min_,
                 left_wheel_velocity_max_);
  right_velocity_command_ =
      std::clamp(right_velocity_command_, right_wheel_velocity_min_,
                 right_wheel_velocity_max_);

  auto msg = std_msgs::msg::Float32MultiArray();
  msg.data = {static_cast<float>(left_velocity_command_),
              static_cast<float>(right_velocity_command_)};
  velocity_pub_->publish(msg);

  return hardware_interface::return_type::OK;
}

void DiffDriveHardware::encoder_callback(
    const std_msgs::msg::Int8MultiArray::SharedPtr msg) {
  std::lock_guard<std::mutex> lock(encoder_mutex_);
  encoder_data_ = msg->data;
}

#include "pluginlib/class_list_macros.hpp"
PLUGINLIB_EXPORT_CLASS(DiffDriveHardware, hardware_interface::SystemInterface)
