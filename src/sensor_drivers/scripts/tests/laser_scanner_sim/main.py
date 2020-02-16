#!/usr/bin/env python

from __future__ import division
from vector_illustration_processing_simplified import pi_point, pi_line, pi_arithmetic

import math
import numpy

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
    
    def set_position(self, position):
        self.position = position
    
    def set_rotation(self, rotation):
        self.rotation = rotation

class RangeSensor(object):
    def _init__(self, parent_transform, relative_transform):
        self.parent_transform = parent_transform
        self.relative_transform = relative_transform

        self.distance_measured = 0

    def update(self, distance_measured):
        self.distance_measured = distance_measured
    
    def get_relative_measured_point(self):
        x = self.relative_transform.position.x + self.distance_measured * math.sin(self.relative_transform.rotation)
        y = self.relative_transform.position.y + self.distance_measured * math.sin(self.relative_transform.rotation)

        return pi_point.Point(x, y)

class LaserScannerUsingRangeSensors(object):
    def __init__(self, parent_transform, relative_transform):
        self.parent_transform = parent_transform
        self.relative_transform = relative_transform

        self.set_number_of_active_sensors(1)

    def set_number_of_active_sensors(self, howmany):
        self.number_of_active_sensors = howmany
        self.number_of_data_points = self.number_of_active_sensors * 1

        self.ranges = [0] * self.number_of_active_sensors
        self.point_cloud = [pi_point.Point()] * self.number_of_active_sensors
        self.simulated_origins = [pi_point.Point()] * self.number_of_active_sensors

        self.populate_simulated_origins()
    
    def populate_simulated_origins(self):
        sim_radius = 100
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
            simulated_origin_line = pi_line.Line(self.relative_transform.position, self.simulated_origins[i])

            r = measured_distance_line.get_length()
            angle = measured_distance_line.get_angle_from_line(simulated_origin_line)

            self.ranges[i] = r * math.cos(angle)