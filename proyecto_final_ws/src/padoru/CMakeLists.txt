cmake_minimum_required(VERSION 3.8)
project(padoru)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(hardware_interface REQUIRED)
find_package(pluginlib REQUIRED)
find_package(ros2_control REQUIRED)
find_package(controller_manager REQUIRED)
# uncomment the following section in order to fill in further dependencies
# manually. find_package(<dependency> REQUIRED)

include_directories(${rclcpp_INCLUDE_DIRS} ${hardware_interface_INCLUDE_DIRS}
                    ${ros2_control_INCLUDE_DIRS})

add_library(diff_drive_hardware SHARED src/DiffDriver.cpp)
ament_target_dependencies(diff_drive_hardware rclcpp hardware_interface
                          pluginlib ros2_control controller_manager)
pluginlib_export_plugin_description_file(hardware_interface
                                         plugin_description.xml)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # the following line skips the linter which checks for copyrights comment the
  # line when a copyright and license is added to all source files
  set(ament_cmake_copyright_FOUND TRUE)
  # the following line skips cpplint (only works in a git repo) comment the line
  # when this package is in a git repo and when a copyright and license is added
  # to all source files
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

install(DIRECTORY config description launch worlds
        DESTINATION share/${PROJECT_NAME}/)

install(TARGETS diff_drive_hardware DESTINATION lib)

install(FILES plugin_description.xml DESTINATION share/${PROJECT_NAME})

ament_package()
