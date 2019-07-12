cmake_minimum_required(VERSION 2.8.3)
project(observer)


find_package(catkin REQUIRED COMPONENTS
	ensenso_camera_msgs)

catkin_package()

include_directories(
  ${rospy_INCLUDE_DIRS}
  ${sensor_msgs_INCLUDE_DIRS}
  ${std_msgs_INCLUDE_DIRS}
)

catkin_python_setup()

#catkin_install_python(PROGRAMS 
#  scripts/observer
#  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
#)

#add_dependencies(observer ${catkin_EXPORTED_TARGETS})
