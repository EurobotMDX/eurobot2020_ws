#!/usr/bin/env python

from __future__ import division
from vector_illustration_processing_simplified import pi_point, pi_line, pi_arithmetic

import math
import rospy
import tf2_ros
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import TransformStamped
from tf.transformations import euler_from_quaternion

class Transform(object):
    def __init__(self, position = None, rotation = None):
        self.position = position
        self.rotation = rotation

        if self.position is None:
            self.position = pi_point.Point()
        
        if self.rotation is None:
            self.rotation = 0.0
    
    def __repr__(self):
        return self.__str__()
    
    def __str__(self):
        return str(self.get_as_dictionary())
    
    def get_as_dictionary(self):
        params = {
            "position": self.position,
            "rotation": self.rotation
        }

        return params
    
    def get_as_deep_dictionary(self):
        params = {
            "position": self.position.get_as_deep_dictionary(),
            "rotation": self.rotation
        }

        return params
    
    def set_from_ros_transform(self, ros_stamped_transform):
        x = ros_stamped_transform.transform.translation.x
        y = ros_stamped_transform.transform.translation.y

        self.rotation = euler_from_quaternion((
            ros_stamped_transform.transform.rotation.x,
            ros_stamped_transform.transform.rotation.y,
            ros_stamped_transform.transform.rotation.z,
            ros_stamped_transform.transform.rotation.w
            ))[-1]
        
        self.position = pi_point.Point(x, y)
    
    def set_position(self, position):
        self.position = position
    
    def set_rotation(self, rotation):
        self.rotation = rotation

class RangeSensor(object):
    def __init__(self, parent_frame_id, relative_frame_id, tf_buffer_object):
        self.relative_frame_id = relative_frame_id
        self.parent_frame_id = parent_frame_id
        
        self.tf_buffer_object = tf_buffer_object
        self.transform_stamped = None

        self.relative_transform = Transform()

        self.distance_measured = 0
    
    def __log(self, msg):
        rospy.loginfo("[INFO] {}".format(msg))

    def update(self, distance_measured):
        self.distance_measured = distance_measured
    
    def get_relative_measured_point(self):
        x = self.relative_transform.position.x + self.distance_measured * math.sin(self.relative_transform.rotation)
        y = self.relative_transform.position.y + self.distance_measured * math.cos(self.relative_transform.rotation)

        return pi_point.Point(x, y)
    
    def update_transform(self):
        try:
            self.transform_stamped = self.tf_buffer_object.lookup_transform(self.parent_frame_id, self.relative_frame_id, rospy.Time())
        except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException):
            rospy.logerr("[ERROR] could not lookup transform between {0} and {1}".format(self.parent_frame_id, self.relative_frame_id))

            return False
        
        if self.transform_stamped is None:
            return False
        
        self.relative_transform.set_from_ros_transform(self.transform_stamped)
        return True

class LaserScannerUsingRangeSensors(object):
    def __init__(self, parent_frame_id, relative_frame_id, tf_buffer_object):
        self.relative_frame_id = relative_frame_id
        self.parent_frame_id = parent_frame_id
        
        self.tf_buffer_object = tf_buffer_object
        self.transform_stamped = None

        self.relative_transform = Transform()
        self.set_number_of_active_sensors(1)
    
    def __log(self, msg):
        rospy.loginfo("[INFO] {}".format(msg))

    def set_number_of_active_sensors(self, howmany):
        self.number_of_active_sensors = howmany
        self.number_of_data_points = self.number_of_active_sensors * 1

        self.compute()
    
    def compute(self):
        self.ranges = [0] * self.number_of_active_sensors
        self.point_cloud = [pi_point.Point()] * self.number_of_active_sensors
        self.simulated_origins = [pi_point.Point()] * self.number_of_active_sensors

        self.populate_simulated_origins()

        # pre-populate the LaserScan message
        self.scan_msg = LaserScan()
        self.scan_msg.header.frame_id = self.relative_frame_id
        self.scan_msg.angle_min = -math.pi
        self.scan_msg.angle_max =  math.pi
        self.scan_msg.angle_increment = (2.0 * math.pi) / self.number_of_data_points
        self.scan_msg.time_increment = 0
        self.scan_msg.scan_time = 0
        self.scan_msg.range_min = 0.01
        self.scan_msg.range_max = 0.50
    
    def publish_message(self, publisher):
        self.scan_msg.header.stamp = rospy.Time.now()
        self.scan_msg.ranges = self.ranges

        publisher.publish(self.scan_msg)
    
    def populate_simulated_origins(self):
        sim_radius = 0.3
        angle_increment = 2.0 * math.pi / self.number_of_data_points

        for i in range(self.number_of_data_points):
            angle = i * angle_increment

            x_position = self.relative_transform.position.x + sim_radius * math.sin(self.relative_transform.rotation + angle)
            y_position = self.relative_transform.position.y + sim_radius * math.cos(self.relative_transform.rotation + angle)

            self.simulated_origins[i] = pi_point.Point(x_position, y_position)
    
    def update(self, range_sensors):
        '''note the order of the sensors determines the order of the data cloud generated'''

        for i in range(self.number_of_active_sensors):
            point = range_sensors[i].get_relative_measured_point()
            self.point_cloud[i] = point

            measured_distance_line = pi_line.Line(self.relative_transform.position, point)
            simulated_origin_line  = pi_line.Line(self.relative_transform.position, self.simulated_origins[i])

            r = measured_distance_line.get_length()
            angle = measured_distance_line.get_angle_from_line(simulated_origin_line)

            self.ranges[i] = r * math.cos(angle)
        
        # self.__log("simulated_origins : {}".format(self.simulated_origins))
        # self.__log("point_cloud : {}".format(self.point_cloud))
    
    def update_transform(self):
        try:
            self.transform_stamped = self.tf_buffer_object.lookup_transform(self.parent_frame_id, self.relative_frame_id, rospy.Time())
        except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException):
            rospy.logerr("[ERROR] could not lookup transform between {0} and {1}".format(self.parent_frame_id, self.relative_frame_id))

            return False
        
        if self.transform_stamped is None:
            return False
        
        self.relative_transform.set_from_ros_transform(self.transform_stamped)
        self.compute()
        return True