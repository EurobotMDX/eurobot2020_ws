# generated from catkin/cmake/template/pkg.context.pc.in
CATKIN_PACKAGE_PREFIX = ""
PROJECT_PKG_CONFIG_INCLUDE_DIRS = "${prefix}/include;/usr/include/eigen3;/opt/ros/kinetic/share/orocos_kdl/../../include".split(';') if "${prefix}/include;/usr/include/eigen3;/opt/ros/kinetic/share/orocos_kdl/../../include" != "" else []
PROJECT_CATKIN_DEPENDS = "geometry_msgs;kdl_conversions;tf".replace(';', ' ')
PKG_CONFIG_LIBRARIES_WITH_PREFIX = "-ltf_conversions;/opt/ros/kinetic/lib/liborocos-kdl.so.1.3.2".split(';') if "-ltf_conversions;/opt/ros/kinetic/lib/liborocos-kdl.so.1.3.2" != "" else []
PROJECT_NAME = "tf_conversions"
PROJECT_SPACE_DIR = "/home/ros/lidar_ws/install"
PROJECT_VERSION = "1.11.9"
