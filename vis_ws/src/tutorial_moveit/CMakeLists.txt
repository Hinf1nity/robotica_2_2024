cmake_minimum_required(VERSION 3.8)
project(tutorial_moveit)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(moveit_ros_planning_interface REQUIRED)
find_package(rclcpp REQUIRED)
find_package(geometric_shapes REQUIRED)
find_package(shape_msgs REQUIRED)

add_executable(obstacle_moveit src/obstacle_moveit.cpp)
add_executable(moveit_movimiento src/moveit_movimiento.cpp)
add_executable(moveit_sequence src/moveit_sequence.cpp)

target_include_directories(obstacle_moveit PUBLIC
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
  $<INSTALL_INTERFACE:include>)
target_compile_features(obstacle_moveit PUBLIC c_std_99 cxx_std_17)  # Require C99 and C++17
ament_target_dependencies(
  obstacle_moveit
  "moveit_ros_planning_interface"
  "rclcpp"
  geometric_shapes
  shape_msgs
)

target_include_directories(moveit_movimiento PUBLIC
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
  $<INSTALL_INTERFACE:include>)

target_compile_features(moveit_movimiento PUBLIC c_std_99 cxx_std_17)  # Require C99 and C++17
ament_target_dependencies(
  moveit_movimiento
  "moveit_ros_planning_interface"
  "rclcpp"
  geometric_shapes
  shape_msgs
)

target_include_directories(moveit_sequence PUBLIC
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
  $<INSTALL_INTERFACE:include>)

target_compile_features(moveit_sequence PUBLIC c_std_99 cxx_std_17)  # Require C99 and C++17

ament_target_dependencies(
  moveit_sequence
  "moveit_ros_planning_interface"
  "rclcpp"
  geometric_shapes
  shape_msgs
)

install(TARGETS obstacle_moveit moveit_movimiento moveit_sequence
  DESTINATION lib/${PROJECT_NAME})

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # the following line skips the linter which checks for copyrights
  # comment the line when a copyright and license is added to all source files
  set(ament_cmake_copyright_FOUND TRUE)
  # the following line skips cpplint (only works in a git repo)
  # comment the line when this package is in a git repo and when
  # a copyright and license is added to all source files
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
