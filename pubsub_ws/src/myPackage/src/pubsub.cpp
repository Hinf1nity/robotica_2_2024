#include <functional>
#include <memory>
#include <string>

#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"

using std::placeholders::_1;

/* This example creates a subclass of Node and uses std::bind() to register a
  member function as a callback from the timer. */

class MinimalPublisherSubscriber : public rclcpp::Node
{
public:
    MinimalPublisherSubscriber()
        : Node("pub_sub")
    {
        subscription_ = this->create_subscription<std_msgs::msg::String>(
            "mensajito_pubsub", 10, std::bind(&MinimalPublisherSubscriber::topic_callback, this, _1));
        publisher_ = this->create_publisher<std_msgs::msg::String>("mensajito_topico", 10);
    }

private:
    void topic_callback(const std_msgs::msg::String &msg) const
    {
        RCLCPP_INFO(this->get_logger(), "I heard: '%s'", msg.data.c_str());
        publisher_->publish(msg);
    }
    rclcpp::Subscription<std_msgs::msg::String>::SharedPtr subscription_;
    rclcpp::Publisher<std_msgs::msg::String>::SharedPtr publisher_;
};

int main(int argc, char *argv[])
{
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<MinimalPublisherSubscriber>());
    rclcpp::shutdown();
    return 0;
}