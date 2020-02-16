#!/usr/bin/env python

import math
import rospy
import tf2_ros
from std_msgs.msg import String
from sensor_msgs.msg import LaserScan, Range
from geometry_msgs.msg import TransformStamped
from tf.transformations import euler_from_quaternion

class DistanceSensorObject(object):
    def __init__(self, world_origin_frame_id, frame_id, tf_buffer_object):
        self.frame_id = frame_id
        self.world_origin_frame_id = world_origin_frame_id
        
        self.tf_buffer_object = tf_buffer_object

        self.position = None
        self.rotation = None
        self.transform_stamped = None
    
    def update(self, measured_distance):
        try:
            self.transform_stamped = self.tf_buffer_object.lookup_transform(self.world_origin_frame_id, self.frame_id, rospy.Time())
        except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException):
            rospy.logerr("[ERROR] could not lookup transform between {0} and {1}".format(self.world_origin_frame_id, self.frame_id))

            return False
            
        if self.transform_stamped is None:
            return False

        self.position = self.transform_stamped.transform.translation.x, self.transform_stamped.transform.translation.y
        self.rotation = euler_from_quaternion((self.transform_stamped.transform.rotation.x, self.transform_stamped.transform.rotation.y, self.transform_stamped.transform.rotation.z, self.transform_stamped.transform.rotation.w))

        return True
    
    def get_measured_point():
        pass


if __name__ == '__main__':
    rospy.init_node('range_tf_monitor')

    tf_buffer = tf2_ros.Buffer()
    listener = tf2_ros.TransformListener(tf_buffer)

    world_origin_frame_id = "base_link"
    front_sensor = DistanceSensorObject(world_origin_frame_id, "ultrasonic_front_emission_point", tf_buffer)
    back_sensor  = DistanceSensorObject(world_origin_frame_id, "ultrasonic_back_emission_point" , tf_buffer)
    left_sensor  = DistanceSensorObject(world_origin_frame_id, "ultrasonic_left_emission_point" , tf_buffer)
    right_sensor = DistanceSensorObject(world_origin_frame_id, "ultrasonic_right_emission_point", tf_buffer)

    rate = rospy.Rate(1)
    while not rospy.is_shutdown():
        
        front_sensor.update(1.0)
        back_sensor.update(1.0)
        left_sensor.update(1.0)
        right_sensor.update(1.0)
        
        rospy.loginfo("[INFO] position: {}, rotation: {}".format(front_sensor.position, front_sensor.rotation))
        rate.sleep()