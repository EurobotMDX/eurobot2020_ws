#!/usr/bin/env python

import math
import json
import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Range, PointCloud
from geometry_msgs.msg import Point32

range_sensors_frame_ids = ["ultrasonic_left_emission_point", "ultrasonic_back_emission_point", "ultrasonic_right_emission_point", "ultrasonic_front_emission_point"]

def publish_ultrasonic_messages(data_publishers, measured_distances):
    range_msg = Range()
    range_msg.radiation_type = 0 # ULTRASOUND
    range_msg.field_of_view = math.pi / 6.0 # 30 degrees
    range_msg.min_range = 0.01
    range_msg.max_range = 2.5

    for index, measured_distance in enumerate(measured_distances):
        range_msg.range = measured_distance
        range_msg.header.frame_id = range_sensors_frame_ids[index]
        range_msg.header.stamp = rospy.Time.now()

        data_publishers[index].publish(range_msg)

def publish_point_cloud_messages(data_publishers, measured_distances):
    point_32_msg = Point32()
    point_cloud_msg = PointCloud()

    for index, measured_distance in enumerate(measured_distances):
        point_32_msg.x = measured_distance
        point_cloud_msg.points = [point_32_msg]

        point_cloud_msg.header.frame_id = range_sensors_frame_ids[index]
        point_cloud_msg.header.stamp = rospy.Time.now()

        data_publishers[index].publish(point_cloud_msg)

def main():
    rospy.init_node("range_sensors_ros_handler_node", anonymous=False)

    front_range_publisher = rospy.Publisher("/front_ultrasonic_data", Range, queue_size=5)
    back_range_publisher  = rospy.Publisher("/back_ultrasonic_data",  Range, queue_size=5)
    left_range_publisher  = rospy.Publisher("/left_ultrasonic_data",  Range, queue_size=5)
    right_range_publisher = rospy.Publisher("/right_ultrasonic_data", Range, queue_size=5)

    front_point_cloud_publisher = rospy.Publisher("/front_point_cloud_data", PointCloud, queue_size=5)
    back_point_cloud_publisher  = rospy.Publisher("/back_point_cloud_data",  PointCloud, queue_size=5)
    left_point_cloud_publisher  = rospy.Publisher("/left_point_cloud_data",  PointCloud, queue_size=5)
    right_point_cloud_publisher = rospy.Publisher("/right_point_cloud_data", PointCloud, queue_size=5)

    front_sensor_msg = PointCloud()
    front_sensor_msg.header.frame_id = "ultrasonic_front_emission_point"

    def callback(data):
        measured_distances = json.loads(data.data)
        publish_ultrasonic_messages([left_range_publisher, back_range_publisher, right_range_publisher, front_range_publisher], measured_distances)
        publish_point_cloud_messages([left_point_cloud_publisher, back_point_cloud_publisher, right_point_cloud_publisher, front_point_cloud_publisher], measured_distances)

    rospy.Subscriber("raw_range_data", String, callback)
    rospy.spin()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException as e:
        # raise e
        pass