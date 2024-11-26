// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from custom_msgs:msg/Box.idl
// generated code does not contain a copyright notice

#ifndef CUSTOM_MSGS__MSG__DETAIL__BOX__BUILDER_HPP_
#define CUSTOM_MSGS__MSG__DETAIL__BOX__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "custom_msgs/msg/detail/box__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace custom_msgs
{

namespace msg
{

namespace builder
{

class Init_Box_corners
{
public:
  explicit Init_Box_corners(::custom_msgs::msg::Box & msg)
  : msg_(msg)
  {}
  ::custom_msgs::msg::Box corners(::custom_msgs::msg::Box::_corners_type arg)
  {
    msg_.corners = std::move(arg);
    return std::move(msg_);
  }

private:
  ::custom_msgs::msg::Box msg_;
};

class Init_Box_centre
{
public:
  explicit Init_Box_centre(::custom_msgs::msg::Box & msg)
  : msg_(msg)
  {}
  Init_Box_corners centre(::custom_msgs::msg::Box::_centre_type arg)
  {
    msg_.centre = std::move(arg);
    return Init_Box_corners(msg_);
  }

private:
  ::custom_msgs::msg::Box msg_;
};

class Init_Box_header
{
public:
  Init_Box_header()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Box_centre header(::custom_msgs::msg::Box::_header_type arg)
  {
    msg_.header = std::move(arg);
    return Init_Box_centre(msg_);
  }

private:
  ::custom_msgs::msg::Box msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::custom_msgs::msg::Box>()
{
  return custom_msgs::msg::builder::Init_Box_header();
}

}  // namespace custom_msgs

#endif  // CUSTOM_MSGS__MSG__DETAIL__BOX__BUILDER_HPP_
