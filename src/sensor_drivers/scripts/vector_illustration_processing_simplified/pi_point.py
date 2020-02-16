#!/usr/bin/env python
from __future__ import division

import cv2
import sys
import math

class Point(object):
	def __init__(self, x=0, y=0, z=0):
		self.x = 0.00
		self.y = 0.00
		self.z = 0.00
		self.r = 0.00
		self.theta = 0.00
		self.point = []
		self.point_polar = []

		self.x = x
		self.y = y
		self.z = z

		self.calculate()
	
	def __repr__(self):
		return self.__str__()

	def __str__(self):
		return str(self.get_as_dictionary())

	def __add__(self, other):
		return self.add(other)

	def __sub__(self, other):
		return self.sub(other)

	def __mul__(self, other):
		return self.mul(other)

	def __div__(self, other):
		return self.div(other)

	def __pow__(self, other):
		return self.pow(other)

	def __eq__(self, other):
		return self.eq(other)

	def __lt__(self, other):
		return self.lt(other)

	def __gt__(self, other):
		return self.gt(other)

	def isinf(self):
		if sys.version.startswith("2"):
			# for python 2
			return (self.x == float("inf")) and (self.y == float("inf")) and (self.z == float("inf"))
		else:
			return (self.x == math.inf) and (self.y == math.inf) and (self.z == math.inf)

	def isnan(self):
		if sys.version.startswith("2"):
			# for python 2
			return (self.x == float("nan")) and (self.y == float("nan")) and (self.z == float("nan"))
		else:
			return (self.x == math.nan) and (self.y == math.nan) and (self.z == math.nan)

	def add(self, other):
		if isinstance(other, Point):
			return Point(self.x + other.x, self.y + other.y, self.z + other.z)
		else:
			return Point(self.x + other, self.y + other, self.z + other)

	def sub(self, other):
		if isinstance(other, Point):
			return Point(self.x - other.x, self.y - other.y, self.z - other.z)
		else:
			return Point(self.x - other, self.y - other, self.z - other)

	def mul(self, other):
		if isinstance(other, Point):
			return Point(self.x * other.x, self.y * other.y, self.z * other.z)
		else:
			return Point(self.x * other, self.y * other, self.z * other)

	def div(self, other):
		if isinstance(other, Point):
			return Point(self.x / other.x, self.y / other.y, self.z / other.z)
		else:
			return Point(self.x / other, self.y / other, self.z / other)

	def pow(self, other):
		if isinstance(other, Point):
			return Point(self.x ** other.x, self.y ** other.y, self.z ** other.z)
		else:
			return Point(self.x ** other, self.y ** other, self.z ** other)

	def log(self, other):
		if isinstance(other, Point):
			return Point(math.log(self.x, other.x), math.log(self.y + other.y), math.log(self.z + other.z))
		else:
			return Point(math.log(self.x + other), math.log(self.y + other), math.log(self.z + other))

	def eq(self, other):
		if isinstance(other, Point):
			return (self.x == other.x) and (self.y == other.y) and (self.z == other.z) 
		else:
			return (self.x == other) and (self.y == other) and (self.z == other)

	def n_eq(self, other):
		if isinstance(other, Point):
			return (self.x != other.x) and (self.y != other.y) and (self.z != other.z) 
		else:
			return (self.x != other)   and (self.y != other)   and (self.z != other)

	def lt(self, other):
		if isinstance(other, Point):
			return (self.x < other.x) and (self.y < other.y) and (self.z < other.z) 
		else:
			return (self.x < other)   and (self.y < other)   and (self.z < other)

	def lt_eq(self, other):
		if isinstance(other, Point):
			return (self.x <= other.x) and (self.y <= other.y) and (self.z <= other.z) 
		else:
			return (self.x <= other)   and (self.y <= other)   and (self.z <= other)

	def gt(self, other):
		if isinstance(other, Point):
			return (self.x > other.x) and (self.y > other.y) and (self.z > other.z) 
		else:
			return (self.x > other)   and (self.y > other)   and (self.z > other)

	def gt_eq(self, other):
		if isinstance(other, Point):
			return (self.x >= other.x) and (self.y >= other.y) and (self.z >= other.z) 
		else:
			return (self.x >= other)   and (self.y >= other)   and (self.z >= other)

	def get_as_dictionary(self):
		params = {
			"x":self.x,
			"y":self.y,
			"z":self.z,
			"r":self.r,
			"theta":self.theta,
			"point":self.point,
			"point_polar":self.point_polar
		}

		return params

	def get_as_deep_dictionary(self):
		params = {
			"x":self.x,
			"y":self.y,
			"z":self.z,
			"r":self.r,
			"theta":self.theta,
			"point":self.point,
			"point_polar":self.point_polar
		}

		return params

	def get_absolute(self):
		return Point(x=abs(self.x), y=abs(self.y), z=abs(self.z))

	def get_as_polar(self):
		pass

	def calculate(self):
		self.r = math.sqrt(pow(self.x, 2) + pow(self.y, 2))
		self.theta = math.atan2(self.y, self.x)

		self.point = [
			self.x, 
			self.y
		]

		self.point_polar = [
			self.r,
			self.theta
		]

		return True

	def set_zero(self):
		self.x = 0
		self.y = 0
		self.z = 0

		return True

	def set_inf(self):
		if sys.version.startswith("2"):
			# for python 2
			self.x = float("inf")
			self.y = float("inf")
			self.z = float("inf")
		else:
			self.x = math.inf
			self.y = math.inf
			self.z = math.inf

		return self.calculate()

	def set_nan(self):
		if sys.version.startswith("2"):
			# for python 2
			self.x = float("nan")
			self.y = float("nan")
			self.z = float("nan")
		else:
			self.x = math.nan
			self.y = math.nan
			self.z = math.nan

		return self.calculate()

	def draw(self, image, color=(255, 255, 255), dot_width=1):
		cv2.circle(image, (int(self.x), int(self.y)), dot_width, color, -1)
		return image



def test_point():
	point = Point(x=0)
	print ("point = ", point.get_as_dictionary())

if __name__ == '__main__':
	def test():
		test_point()

	test()