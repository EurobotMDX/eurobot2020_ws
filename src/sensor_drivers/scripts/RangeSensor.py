#!/usr/bin/env python

import math
import rospy
from sensor_msgs.msg import LaserScan

class RangeSensor(object):
	def __init__(self, frame_id="", min_range=0.01, max_range=2.0, angle_range=math.radians(30.0)):
		self.frame_id = frame_id

		self.min_range = min_range
		self.max_range = max_range

		angle_range = abs(angle_range)
		self.min_angle = -1.0 * (angle_range / 2.0)
		self.max_angle = +1.0 * (angle_range / 2.0)
		
		self.num_readings = 10
		self.angle_increment = angle_range / self.num_readings

		self.laser_frequency = 1000.0

		self.ranges = []
		self.intensities = []
		self.measured_range = max_range

		# pre-populate the LaserScan message
		self.scan = LaserScan()
		self.scan.header.frame_id = self.frame_id
		self.scan.angle_min = self.min_angle
		self.scan.angle_max = self.max_angle
		self.scan.angle_increment = self.angle_increment
		self.scan.time_increment = 0
		self.scan.scan_time = 0
		self.scan.range_min = self.min_range
		self.scan.range_max = self.max_range

	def update_range(self, measured_range=0.4):
		self.measured_range = self._constrain(measured_range, self.min_range, self.max_range)

	def get_as_laserscan(self):
		self.ranges = []
		self.intensities = []

		for i in range(self.num_readings):
			angle = (i * self.angle_increment) + self.min_angle
			d = self.measured_range / math.cos(angle)
			self.ranges.append(d)

		# populate the LaserScan message
		self.scan.header.stamp = rospy.Time.now()
		self.scan.ranges = self.ranges
		self.scan.intensities = self.intensities

		return self.scan

	def _constrain(self, val, min_val, max_val):
		return min(max_val, max(val, min_val))