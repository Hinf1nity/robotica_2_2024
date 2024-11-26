// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from custom_msgs:msg/Box.idl
// generated code does not contain a copyright notice

#ifndef CUSTOM_MSGS__MSG__DETAIL__BOX__TRAITS_HPP_
#define CUSTOM_MSGS__MSG__DETAIL__BOX__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "custom_msgs/msg/detail/box__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__traits.hpp"
// Member 'centre'
// Member 'corners'
#include "custom_msgs/msg/detail/corner__traits.hpp"

namespace custom_msgs
{

namespace msg
{

inline void to_flow_style_yaml(
  const Box & msg,
  std::ostream & out)
{
  out << "{";
  // member: header
  {
    out << "header: ";
    to_flow_style_yaml(msg.header, out);
    out << ", ";
  }

  // member: centre
  {
    out << "centre: ";
    to_flow_style_yaml(msg.centre, out);
    out << ", ";
  }

  // member: corners
  {
    if (msg.corners.size() == 0) {
      out << "corners: []";
    } else {
      out << "corners: [";
      size_t pending_items = msg.corners.size();
      for (auto item : msg.corners) {
        to_flow_style_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const Box & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: header
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "header:\n";
    to_block_style_yaml(msg.header, out, indentation + 2);
  }

  // member: centre
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "centre:\n";
    to_block_style_yaml(msg.centre, out, indentation + 2);
  }

  // member: corners
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.corners.size() == 0) {
      out << "corners: []\n";
    } else {
      out << "corners:\n";
      for (auto item : msg.corners) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "-\n";
        to_block_style_yaml(item, out, indentation + 2);
      }
    }
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const Box & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace msg

}  // namespace custom_msgs

namespace rosidl_generator_traits
{

[[deprecated("use custom_msgs::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const custom_msgs::msg::Box & msg,
  std::ostream & out, size_t indentation = 0)
{
  custom_msgs::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use custom_msgs::msg::to_yaml() instead")]]
inline std::string to_yaml(const custom_msgs::msg::Box & msg)
{
  return custom_msgs::msg::to_yaml(msg);
}

template<>
inline const char * data_type<custom_msgs::msg::Box>()
{
  return "custom_msgs::msg::Box";
}

template<>
inline const char * name<custom_msgs::msg::Box>()
{
  return "custom_msgs/msg/Box";
}

template<>
struct has_fixed_size<custom_msgs::msg::Box>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<custom_msgs::msg::Box>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<custom_msgs::msg::Box>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // CUSTOM_MSGS__MSG__DETAIL__BOX__TRAITS_HPP_
