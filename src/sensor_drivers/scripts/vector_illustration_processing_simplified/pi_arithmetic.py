#!/usr/bin/env python
from __future__ import division

import sys
import math

def measure(point_1, point_2):
	return math.sqrt(pow(point_2.x - point_1.x, 2) + pow(point_2.y - point_1.y, 2) + pow(point_2.z - point_1.z, 2))

def sign_of(val):
	return abs(val) / float(val)

class RectInfo(object):
	bottom_right = None
	center       = None
	top_left     = None
	
	height    = 0
	width     = 0
	radius    = 0
	area      = 0
	perimeter = 0

	def __init__(self, **kwargs):
		items_gen = None
		
		if sys.version.startswith("2"):
			items_gen = kwargs.iteritems()
		else:
			items_gen = kwargs.items()

		for key, value in items_gen:
			if key.lower() == "bottom_right":
				self.bottom_right = value
			elif key.lower() == "center":
				self.center = value
			elif key.lower() == "top_left":
				self.top_left = value
			elif key.lower() == "height":
				self.height = value
			elif key.lower() == "width":
				self.width = value
			elif key.lower() == "radius":
				self.radius = value
			elif key.lower() == "area":
				self.area = value
			elif key.lower() == "perimeter":
				self.perimeter = value

	def get_as_dictionary(self):
		params = {
			"bottom_right":self.bottom_right,
			"center":self.center,
			"top_left":self.top_left,
			"height":self.height,
			"width":self.width,
			"radius":self.radius,
			"area":self.area,
			"perimeter":self.perimeter
		}

		return params

	def get_as_deep_dictionary(self):
		params = {
			"bottom_right":self.bottom_right.get_as_deep_dictionary(),
			"center":self.center.get_as_deep_dictionary(),
			"top_left":self.top_left.get_as_deep_dictionary(),
			"height":self.height,
			"width":self.width,
			"radius":self.radius,
			"area":self.area,
			"perimeter":self.perimeter
		}

		return params
