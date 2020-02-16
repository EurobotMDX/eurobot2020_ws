#!/usr/bin/env python
from __future__ import division

import cv2
import sys
import math
import warnings
import pi_point
import numpy as np
import pi_arithmetic


class Line(object):
	def __init__(self, start=pi_point.Point(), end=pi_point.Point()):
		self.end = None
		self.start = None
		self.ref_point = None
		
		self.line = []

		self.m = 0.0
		self.angle = 0.0
		self.length = 0.0

		self.start = start
		self.end = end

		self.compute()
	
	def __repr__(self):
		return self.__str__()

	def __str__(self):
		return str(self.get_as_dictionary())

	def compute(self):
		self.line = [self.start, self.end]

		self.m = self.get_gradient()
		self.ref_point = self.start
		self.length = self.get_length()
		self.angle = self.get_angle()

		return True
	
	def get_in_between_points(self, resolution=0.1):

		points = []

		range_val = 1.0 / resolution
		for i in range(int(range_val)):
			points.append( self.get_point(i / range_val) )
		
		return points

	def __rotate_coord(self, coord, angle, about_point):
		c1 = about_point.x
		c2 = about_point.y
		c3 = about_point.z

		x_old = coord.x
		y_old = coord.y
		z_old = coord.z

		x = np.matrix([
			[c1, c2]
			])

		y = np.matrix([
			[math.cos(angle), -1.0 * math.sin(angle)],
			[math.sin(angle),        math.cos(angle)]
			])

		z = np.matrix([
			[x_old - c1, y_old - c2]
			])

		a = x + (y * z)

		return pi_point.Point(x=a[0,0], y=a[1,0])

	def get_length(self):
		return pi_arithmetic.measure(self.start, self.end)

	def get_gradient(self):
		return math.tan(self.get_angle())

	def get_angle(self):
		dx = self.end.x - self.start.x
		dy = self.end.y - self.start.y
		return math.atan2(dy, dx)
	
	def get_angle_from_line(self, other_line):
		a = (self.get_gradient() - other_line.get_gradient())
		b = 1 + (self.get_gradient() * other_line.get_gradient())
		
		try:
			return math.atan(a/b)
		except ZeroDivisionError:
			return pi_arithmetic.sign_of(a) * math.pi / 2.0

	def get_midpoint(self):
		x = self.start.x + ((self.end.x - self.start.x) * 0.5)
		y = self.start.y + ((self.end.y - self.start.y) * 0.5)
		return pi_point.Point(x, y)

	def get_point(self, position):
		x = self.start.x + ((self.end.x - self.start.x) * position)
		y = self.start.y + ((self.end.y - self.start.y) * position)
		return pi_point.Point(x, y)
	
	def plot(self, title="line_01"):
		return True

	def is_on_line(self, point, resolution=0.001):
		# This works based on the principle
		# A--C-----B; where AC,CB,AB are a lines
		# and AC + CB == AB

		ac = pi_arithmetic.measure(self.start, point)
		cb = pi_arithmetic.measure(point, self.end)
		ab = pi_arithmetic.measure(self.start, self.end)

		return abs((ac + cb) - ab) <= resolution

	def get_intersecting_point(self, other):
		x1 = self.start.x;  x2 = self.end.x
		y1 = self.start.y;  y2 = self.end.y

		x3 = other.start.x; x4 = other.end.x
		y3 = other.start.y; y4 = other.end.y

		a = np.matrix([
				[x1, y1],
				[x2, y2]
			])

		b = np.matrix([
				[x1, 1],
				[x2, 1]
			])

		c = np.matrix([
				[x3, y3],
				[x4, y4]
			])

		d = np.matrix([
				[x3, 1],
				[x4, 1]
			])

		e = np.matrix([
				[y1, 1],
				[y2, 1]
			])

		f = np.matrix([
				[y3, 1],
				[y4, 1]
			])

		A = np.matrix([
				[np.linalg.det(a), np.linalg.det(b)],
				[np.linalg.det(c), np.linalg.det(d)]
			])

		B = np.matrix([
				[np.linalg.det(b), np.linalg.det(e)],
				[np.linalg.det(d), np.linalg.det(f)]
			])

		C = np.matrix([
				[np.linalg.det(a), np.linalg.det(e)],
				[np.linalg.det(c), np.linalg.det(f)]
			])

		x = y = 0
		with warnings.catch_warnings(record=True) as w:
			x = np.linalg.det(A) / np.linalg.det(B)
			y = np.linalg.det(C) / np.linalg.det(B)
			
		point = pi_point.Point(x, y)
		if not (self.is_on_line(point) and other.is_on_line(point)):
			new_point = pi_point.Point()
			new_point.set_inf()

			return new_point

		return point

	def draw(self, img, color=(255, 255, 255), stroke_width=5, line_type=8, shift=0):
		cv2.line(
				img,
				(int(self.line[0].x), int(self.line[0].y)),
				(int(self.line[1].x), int(self.line[1].y)),
				tuple(color),
				int(stroke_width)
			)

		return img

	def translate(self, x, y, z=0):
		translation_vector = pi_point.Point(x=x, y=y, z=z)

		self.start = self.start + translation_vector
		self.end = self.start + translation_vector

		return self.compute()

	def shear(self, x, y):
		return True

	def scale(self, **kwargs):
		mag = None
		mag_x = None
		mag_y = None
		mag_z = None
		about_point = None

		items_gen = None
		
		if sys.version.startswith("2"):
			items_gen = kwargs.iteritems()
		else:
			items_gen = kwargs.items()

		for key, value in items_gen:
			if key.lower() == "mag":
				mag = value
			elif key.lower() == "mag_x":
				mag_x = value
			elif key.lower() == "mag_y":
				mag_y = value
			elif key.lower() == "mag_z":
				mag_z = value
			elif key.lower() == "about_point":
				about_point = about_point

		if (mag_x is not None) and (mag_y is not None) and (about_point is None):
			scale_vector = None
			if mag_z is not None:
				scale_vector = pi_point.Point(x=mag_x, y=mag_y, z=mag_z)
			else:
				scale_vector = pi_point.Point(x=mag_x, y=mag_y)

			self.start *= scale_vector
			self.end   *= scale_vector
		elif (mag_x is not None) and (mag_y is not None) and (about_point is not None):
			dx = mag_x * self.length * 0.5 * math.cos(angle)
			dy = mag_y * self.length * 0.5 * math.sin(angle)

			self.start = pi_point.Point(about_point.x - dx, about_point.y - dy)
			self.end   = pi_point.Point(about_point.x + dx, about_point.y + dy)
		elif mag is not None:
			if about_point is None:
				about_point = get_midpoint()

			new_length = mag * length * 0.5
			dx = new_length * math.cos(angle)
			dy = new_length * math.sin(angle)

			self.start = pi_point.Point(about_point.x - dx, about_point.y - dy)
			self.end   = pi_point.Point(about_point.x + dx, about_point.y + dy)
		else:
			raise ValueError("Incorrect variables received use 'mag' or ('mag_x', 'mag_y', ['mag_z']) and or 'about_point'")

		return self.compute()

	def rotate(self, angle, about_point=None):
		if about_point is None:
			about_point = self.get_midpoint()

		self.start = self.__rotate_coord(self.start, angle, about_point)
		self.end = self.__rotate_coord(self.end, angle, about_point)

		return self.compute()

	def get_as_dictionary(self):
		params = {
			"start": self.start,
			"end": self.end,
			"ref_point": self.ref_point,
			"line": self.line,
			"m": self.m,
			"angle": self.angle,
			"length": self.length
		}

		return params

	def get_as_deep_dictionary(self):
		params = {
			"start": self.start.get_as_deep_dictionary(),
			"end": self.end.get_as_deep_dictionary(),
			"ref_point": self.ref_point.get_as_deep_dictionary(),
			"line": [i.get_as_deep_dictionary() for i in self.line],
			"m": self.m,
			"angle": self.angle,
			"length": self.length
		}

		return params

def test_line():
	line = Line()
	print ("line = ", line.get_as_dictionary())

if __name__ == '__main__':
	def test():
		test_line()

	test()