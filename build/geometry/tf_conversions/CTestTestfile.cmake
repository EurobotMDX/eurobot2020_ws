# CMake generated Testfile for 
# Source directory: /home/ros/lidar_ws/src/geometry/tf_conversions
# Build directory: /home/ros/lidar_ws/build/geometry/tf_conversions
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test(_ctest_tf_conversions_gtest_test_eigen_tf "/home/ros/lidar_ws/build/catkin_generated/env_cached.sh" "/usr/bin/python" "/opt/ros/kinetic/share/catkin/cmake/test/run_tests.py" "/home/ros/lidar_ws/build/test_results/tf_conversions/gtest-test_eigen_tf.xml" "--return-code" "/home/ros/lidar_ws/devel/lib/tf_conversions/test_eigen_tf --gtest_output=xml:/home/ros/lidar_ws/build/test_results/tf_conversions/gtest-test_eigen_tf.xml")
add_test(_ctest_tf_conversions_gtest_test_kdl_tf "/home/ros/lidar_ws/build/catkin_generated/env_cached.sh" "/usr/bin/python" "/opt/ros/kinetic/share/catkin/cmake/test/run_tests.py" "/home/ros/lidar_ws/build/test_results/tf_conversions/gtest-test_kdl_tf.xml" "--return-code" "/home/ros/lidar_ws/devel/lib/tf_conversions/test_kdl_tf --gtest_output=xml:/home/ros/lidar_ws/build/test_results/tf_conversions/gtest-test_kdl_tf.xml")
add_test(_ctest_tf_conversions_nosetests_test.posemath.py "/home/ros/lidar_ws/build/catkin_generated/env_cached.sh" "/usr/bin/python" "/opt/ros/kinetic/share/catkin/cmake/test/run_tests.py" "/home/ros/lidar_ws/build/test_results/tf_conversions/nosetests-test.posemath.py.xml" "--return-code" "\"/usr/bin/cmake\" -E make_directory /home/ros/lidar_ws/build/test_results/tf_conversions" "/usr/bin/nosetests-2.7 -P --process-timeout=60 /home/ros/lidar_ws/src/geometry/tf_conversions/test/posemath.py --with-xunit --xunit-file=/home/ros/lidar_ws/build/test_results/tf_conversions/nosetests-test.posemath.py.xml")
