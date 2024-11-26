// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from custom_msgs:msg/Corner.idl
// generated code does not contain a copyright notice

#ifndef CUSTOM_MSGS__MSG__DETAIL__CORNER__BUILDER_HPP_
#define CUSTOM_MSGS__MSG__DETAIL__CORNER__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "custom_msgs/msg/detail/corner__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace custom_msgs
{

namespace msg
{

namespace builder
{

class Init_Corner_y
{
public:
  explicit Init_Corner_y(::custom_msgs::msg::Corner & msg)
  : msg_(msg)
  {}
  ::custom_msgs::msg::Corner y(::custom_msgs::msg::Corner::_y_type arg)
  {
    msg_.y = std::move(arg);
    return std::move(msg_);
  }

private:
  ::custom_msgs::msg::Corner msg_;
};

class Init_Corner_x
{
public:
  Init_Corner_x()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Corner_y x(::custom_msgs::msg::Corner::_x_type arg)
  {
    msg_.x = std::move(arg);
    return Init_Corner_y(msg_);
  }

private:
  ::custom_msgs::msg::Corner msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::custom_msgs::msg::Corner>()
{
  return custom_msgs::msg::builder::Init_Corner_x();
}

}  // namespace custom_msgs

#endif  // CUSTOM_MSGS__MSG__DETAIL__CORNER__BUILDER_HPP_
