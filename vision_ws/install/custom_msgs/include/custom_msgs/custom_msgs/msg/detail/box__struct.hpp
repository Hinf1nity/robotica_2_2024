// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from custom_msgs:msg/Box.idl
// generated code does not contain a copyright notice

#ifndef CUSTOM_MSGS__MSG__DETAIL__BOX__STRUCT_HPP_
#define CUSTOM_MSGS__MSG__DETAIL__BOX__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__struct.hpp"
// Member 'centre'
// Member 'corners'
#include "custom_msgs/msg/detail/corner__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__custom_msgs__msg__Box __attribute__((deprecated))
#else
# define DEPRECATED__custom_msgs__msg__Box __declspec(deprecated)
#endif

namespace custom_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct Box_
{
  using Type = Box_<ContainerAllocator>;

  explicit Box_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_init),
    centre(_init)
  {
    (void)_init;
  }

  explicit Box_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_alloc, _init),
    centre(_alloc, _init)
  {
    (void)_init;
  }

  // field types and members
  using _header_type =
    std_msgs::msg::Header_<ContainerAllocator>;
  _header_type header;
  using _centre_type =
    custom_msgs::msg::Corner_<ContainerAllocator>;
  _centre_type centre;
  using _corners_type =
    std::vector<custom_msgs::msg::Corner_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<custom_msgs::msg::Corner_<ContainerAllocator>>>;
  _corners_type corners;

  // setters for named parameter idiom
  Type & set__header(
    const std_msgs::msg::Header_<ContainerAllocator> & _arg)
  {
    this->header = _arg;
    return *this;
  }
  Type & set__centre(
    const custom_msgs::msg::Corner_<ContainerAllocator> & _arg)
  {
    this->centre = _arg;
    return *this;
  }
  Type & set__corners(
    const std::vector<custom_msgs::msg::Corner_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<custom_msgs::msg::Corner_<ContainerAllocator>>> & _arg)
  {
    this->corners = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    custom_msgs::msg::Box_<ContainerAllocator> *;
  using ConstRawPtr =
    const custom_msgs::msg::Box_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<custom_msgs::msg::Box_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<custom_msgs::msg::Box_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      custom_msgs::msg::Box_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<custom_msgs::msg::Box_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      custom_msgs::msg::Box_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<custom_msgs::msg::Box_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<custom_msgs::msg::Box_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<custom_msgs::msg::Box_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__custom_msgs__msg__Box
    std::shared_ptr<custom_msgs::msg::Box_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__custom_msgs__msg__Box
    std::shared_ptr<custom_msgs::msg::Box_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const Box_ & other) const
  {
    if (this->header != other.header) {
      return false;
    }
    if (this->centre != other.centre) {
      return false;
    }
    if (this->corners != other.corners) {
      return false;
    }
    return true;
  }
  bool operator!=(const Box_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct Box_

// alias to use template instance with default allocator
using Box =
  custom_msgs::msg::Box_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace custom_msgs

#endif  // CUSTOM_MSGS__MSG__DETAIL__BOX__STRUCT_HPP_
