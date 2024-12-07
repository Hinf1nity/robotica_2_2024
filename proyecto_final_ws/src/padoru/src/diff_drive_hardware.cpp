#include "hardware_interface/types/hardware_interface_type_values.hpp"
#include <hardware_interface/system_interface.hpp>
#include <pluginlib/class_list_macros.hpp>
#include <rclcpp/rclcpp.hpp>
#include <std_msgs/msg/float32_multi_array.hpp>
#include <std_msgs/msg/int8_multi_array.hpp>

class DiffDriveHardware : public hardware_interface::SystemInterface,
                          public rclcpp::Node {
public:
  DiffDriveHardware() : Node("diff_drive_hardware") {}

  hardware_interface::CallbackReturn
  on_init(const hardware_interface::HardwareInfo &info) override {
    // Inicializa ROS 2: suscriptores y publicadores
    encoder_sub_ = this->create_subscription<std_msgs::msg::Int8MultiArray>(
        "encoders", 10,
        std::bind(&DiffDriveHardware::encoder_callback, this,
                  std::placeholders::_1));

    velocity_pub_ = this->create_publisher<std_msgs::msg::Float32MultiArray>(
        "vel_arduino", 10);

    // Inicializa variables de hardware
    left_position_ = right_position_ = 0.0;
    left_velocity_ = right_velocity_ = 0.0;
    left_velocity_command_ = right_velocity_command_ = 0.0;
    time_ = std::chrono::system_clock::now();

    return hardware_interface::CallbackReturn::SUCCESS;
  }

  std::vector<hardware_interface::StateInterface>
  export_state_interfaces() override {
    std::vector<hardware_interface::StateInterface> state_interfaces;

    // Usando constantes de hardware_interface_type_values.hpp
    state_interfaces.emplace_back(hardware_interface::StateInterface(
        "left_wheel_joint", hardware_interface::HW_IF_POSITION,
        &left_position_));
    state_interfaces.emplace_back(hardware_interface::StateInterface(
        "left_wheel_joint", hardware_interface::HW_IF_VELOCITY,
        &left_velocity_));
    state_interfaces.emplace_back(hardware_interface::StateInterface(
        "right_wheel_joint", hardware_interface::HW_IF_POSITION,
        &right_position_));
    state_interfaces.emplace_back(hardware_interface::StateInterface(
        "right_wheel_joint", hardware_interface::HW_IF_VELOCITY,
        &right_velocity_));

    return state_interfaces;
  }

  std::vector<hardware_interface::CommandInterface>
  export_command_interfaces() override {
    std::vector<hardware_interface::CommandInterface> command_interfaces;

    // Usando constantes de hardware_interface_type_values.hpp
    command_interfaces.emplace_back(hardware_interface::CommandInterface(
        "left_wheel_joint", hardware_interface::HW_IF_VELOCITY,
        &left_velocity_command_));
    command_interfaces.emplace_back(hardware_interface::CommandInterface(
        "right_wheel_joint", hardware_interface::HW_IF_VELOCITY,
        &right_velocity_command_));

    return command_interfaces;
  }

  hardware_interface::return_type
  read(const rclcpp::Time &time, const rclcpp::Duration &period) override {
    // Lee datos de los encoders y actualiza posiciones/velocidades

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
  write(const rclcpp::Time &time, const rclcpp::Duration &period) override {
    // Publica velocidades calculadas en el tópico "vel_arduino"
    // Limita las velocidades a los valores máximos y mínimos definidos
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

private:
  // Callback para los encoders
  void encoder_callback(const std_msgs::msg::Int8MultiArray::SharedPtr msg) {
    std::lock_guard<std::mutex> lock(encoder_mutex_);
    encoder_data_ = msg->data; // Asume que msg->data[0] es izquierda,
                               // msg->data[1] es derecha
  }

  rclcpp::Subscription<std_msgs::msg::Int8MultiArray>::SharedPtr encoder_sub_;
  rclcpp::Publisher<std_msgs::msg::Float32MultiArray>::SharedPtr velocity_pub_;
  std::mutex encoder_mutex_;
  std::vector<int8_t> encoder_data_{0, 0};

  double left_position_ = 0.0, right_position_ = 0.0;
  double left_velocity_ = 0.0, right_velocity_ = 0.0;
  double left_velocity_command_ = 0.0, right_velocity_command_ = 0.0;
  double left_wheel_velocity_min_ = -18.0, left_wheel_velocity_max_ = 18.0;
  double right_wheel_velocity_min_ = -18.0, right_wheel_velocity_max_ = 18.0;
  std::chrono::time_point<std::chrono::system_clock> time_;

  static constexpr double ENCODER_RESOLUTION =
      0.14271; // Ajusta según la resolución de tus encoders
};

#include "pluginlib/class_list_macros.hpp"
PLUGINLIB_EXPORT_CLASS(DiffDriveHardware, hardware_interface::SystemInterface)
