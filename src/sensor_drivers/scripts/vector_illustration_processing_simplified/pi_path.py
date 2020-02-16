#!/usr/bin/env python
from __future__ import division

import cv2
import sys
import math
import pi_line
import pi_point
import numpy as np
import pi_arithmetic

class Path(object):
	def __init__(self, **kwargs):
		self.__filter_x_function = lambda cur_point : cur_point.x
		self.__filter_y_function = lambda cur_point : cur_point.y
		self.__filter_z_function = lambda cur_point : cur_point.z

		self.ratio = 0

		self.data_points = []
		self.xs = []
		self.ys = []
		self.boundary_lines = []

		self.closed = True
		self.rect_info = pi_arithmetic.RectInfo()

		items_gen = None
		
		if sys.version.startswith("2"):
			items_gen = kwargs.iteritems()
		else:
			items_gen = kwargs.items()

		_raw_point_data = None
		_is_closed = None
		
		_rect = None

		_center = None
		_radius = None
		_angle = 2 * math.pi
		_steps = 32

		_rx = None
		_ry = None

		def __throw_error():
			raise ValueError("Incorrect variables given used ['raw_point_data' or 'rect' or ['center' and 'radius'] or ['center' and 'rx' and 'ry']] and 'is_closed' and or [angle, count]")

		for key, value in items_gen:
			if key.lower() == "raw_point_data":
				_raw_point_data = value
			elif key.lower() == "is_closed":
				_is_closed = value
			elif key.lower() == "rect":
				_rect = value
			elif key.lower() == "center":
				_center = value
			elif key.lower() == "radius":
				_radius = value
			elif key.lower() == "angle":
				_angle = value
			elif key.lower() == "steps":
				_steps = value
			elif key.lower() == "rx":
				_rx = value
			elif key.lower() == "ry":
				_ry = value
		
		if (_raw_point_data is not None) and (_is_closed is not None):
			if (len(_raw_point_data) > 0) and (not isinstance(_raw_point_data[0], pi_point.Point)):
				points = []
				for i in range(len(_raw_point_data)):
					cv_point = _raw_point_data[i]
					points.append(pi_point.Point(x=cv_point.x, y=cv_point.y))

				self.data_points = points
			else:
				self.data_points = _raw_point_data
			
			self.closed = _is_closed
		
		elif (_raw_point_data is not None) and (_is_closed is None):
			raise ValueError("Incorrect variables given - must include is_closed")

		elif _rect is not None:
			point_1 = pi_point.Point(_rect.x, _rect.y)
			point_2 = pi_point.Point(_rect.x + _rect.width, _rect.y)
			point_3 = pi_point.Point(_rect.x + _rect.width, _rect.y + _rect.height)
			point_4 = pi_point.Point(_rect.x, _rect.y + _rect.height)

			points = [point_1, point_2, point_3, point_4]

			self.data_points = points
			self.closed = False
		elif _center is not None:
			points = []

			if _radius is not None:
				rx = ry = _radius
			elif (rx is not None) and (ry is not None):
				pass
			else:
				__throw_error()

			theta = 0.0
			increment = 2.0 * math.pi / _steps
			_rx = abs(_rx)
			_ry = abs(_ry)

			while theta < _angle:
				x = _center.x + _rx * math.cos(theta)
				y = _center.y + _ry * math.sin(theta)

				points.append(pi_point.Point(x, y))
				theta += increment

			self.data_points = points
			self.closed = False


		self.calculate()
	
	def __repr__(self):
		return self.__str__()

	def __str__(self):
		return str(self.get_as_dictionary())

	def get_start_point(self):
		return self.data_points[0]

	def get_end_point(self):
		return self.data_points[-1]

	def get_position(self, position):
		# render into a sequence of points stored in an array
		# and use its length to compute the position returning
		# the start and ends of smaller/section lines
		pass
	
	def compute_high_resolution_path(self, resolution=0.1):
		#TODO: compute hi-res path using the get_position method

		# self.high_res_xs = []
		# self.high_res_ys = []

		# self.high_res_xs.append(self.boundary_lines[0].start.x)
		# self.high_res_ys.append(self.boundary_lines[0].start.y)

		# for line in self.boundary_lines:
		# 	self.high_res_xs.append(line.end.x)
		# 	self.high_res_ys.append(line.end.y)
		
		# self.high_res_xs.append(line.start.x)
		# self.high_res_ys.append(line.start.y)

		pass
	
	def count_edges(self, angle_threshold):
		count = 1

		def _get_angle(a, b, c):
			return math.acos(((b ** 2) + (a ** 2) - (c ** 2)) / (2.0 * b * a))

		for i in range(len(self.boundary_lines) - 1):
			current_line = self.boundary_lines[i]
			next_line = self.boundary_lines[i+1]

			a = current_line.length
			b = next_line.length
			c = pi_line.Line(current_line.start, next_line.end).length

			if min(a, b, c) <= 0: continue

			angle = _get_angle(a, b, c)

			if abs(angle) > angle_threshold:
				count += 1
		
		return count


	def get_rect_info(self):
		return self.rect_info

	def get_boundary_lines(self):
		return self.boundary_lines

	def get_intersecting_points(self, pi_object):
		if isinstance(pi_object, pi_line.Line):
			intersecting_points = []

			for i in range(len(self.boundary_lines)):
				current_line = self.boundary_lines[i]
				intersecting_point = pi_object.get_intersecting_point(current_line)

				if not intersecting_point.isinf():
					intersecting_points.append(intersecting_point)

			return intersecting_points
		elif isinstance(pi_object, Path):
			intersecting_points = []

			for i in range(len(self.boundary_lines)):
				line = self.boundary_lines[i]
				for j in range(len(pi_object.boundary_lines)):
					other_line = pi_object.boundary_lines[j]
					intersecting_point = line.get_intersecting_point(other_line)

					if not intersecting_point.isinf():
						intersecting_points.append(intersecting_point)

			return intersecting_points
		else:
			raise ValueError("Incorrect variables given 'variables must be [pi_line.Line or pi_path.Path]'")

		return False

	def get_shading_lines(self, spacing=10.0, angle=0.0, padding=0.0):
		lines = []

		min_x = self.rect_info.top_left.x - padding;
		min_y = self.rect_info.top_left.y - padding;

		max_x = self.rect_info.bottom_right.x + padding;
		max_y = self.rect_info.bottom_right.y + padding;

		cx = (max_x - min_x)/2.0 + min_x;
		cy = (max_y - min_y)/2.0 + min_y;

		about_point = pi_point.Point(cx, cy)

		for y in range(min_y, max_y, spacing):
			start = pi_point.Point(min_x, y)
			end = pi_point.Point(max_x, y)
			line = pi_line.Line(start, end)

			line.rotate(angle, about_point)
			lines.append(line)

		return lines

	def get_intersecting_lines(self, spacing=10.0, angle=0.0):
		padding = max(rect_info.width, rect_info.height)
		lines = self.get_shading_lines(spacing, angle, padding)

		intersecting_lines = []
		for i in range(len(lines)):
			line = lines[i]
			intersecting_points = self.get_intersecting_points(line)

			sorted(intersecting_points, key=self.__filter_x_function)

			for j in range(0, max(len(intersecting_points)-1, 0), 2):
				start = intersecting_points[i]
				end = intersecting_points[j+1]

				line = pi_line.Line(start, end)
				intersecting_lines.append(line)

		return intersecting_lines

	def is_touching(self, pi_object):
		if isinstance(pi_object, pi_point.Point):
			# uses raying casting algorithm to solve point in polygon
			inf_point = pi_point.Point(pi_object.x + self.rect_info.top_left.x + self.rect_info.width + 10, pi_object.y)
			ray_line = pi_line.Line(pi_object, inf_point)

			intersecting_points = self.get_intersecting_points(ray_line)
			return not (len(intersecting_points) % 2 == 0)
		elif isinstance(pi_object, pi_line.Line):
			points = self.get_intersecting_points(pi_object)
			return self.is_touching(pi_object.start) or self.is_touching(pi_object.end) or (len(points) > 0)
		else:
			return False

		return False

	def is_within(self, pi_object, resolution=0.0001):
		if isinstance(pi_object, pi_point.Point):
			# uses ray casting algorithm to solve point in polygon

			inf_point = pi_point.Point(pi_object.x + self.rect_info.top_left.x + self.rect_info.width + 10, pi_object.y)
			ray_line = pi_line.Line(pi_object, inf_point)

			intersecting_points = self.get_intersecting_points(ray_line)

			if len(intersecting_points) % 2 == 0:
				return False

			elif len(intersecting_points) == 1:
				if intersecting_points[i].equal(pi_object):
					# it's just touching
					return False

			return True
		elif isinstance(pi_object, pi_line.Line):
			points = self.get_intersecting_points(pi_object)

			if (len(points)) == 1:
				if (self.is_touching(pi_object.start) and not (pi_object.start.equal(points[0]))):
					return True

				elif (self.is_touching(pi_object.end) and not (pi_object.end.equal(points[0]))):
					return True
			elif len(points) == 2:
				other_points = [pi_object.start, pi_object.end]

				sorted(other_points, key=self.__filter_x_function)
				sorted(other_points, key=self.__filter_x_function)

				dx_0 = other_points[0].x - points[0].x
				dx_1 = other_points[1].x - points[1].x

				resolution = -1.0 * resolution
				return (dx_0 >= resolution) and (dx_1 >= resolution)

			if self.is_within(pi_object.start) or self.is_within(pi_object.end):
				return True
			elif self.is_touching(pi_object.start) and self.is_touching(pi_object.end):
				return True
			else:
				return False

		return False


	def mask(self, image_in, image_out, override_image_out, empty_color, translation_x, translation_y, translation_z=0):
		pass

	def draw(self, image, color=(255, 255, 255), stroke_width=1, line_type=8, shift=0):
		for i in range(len(self.boundary_lines)):
			image = self.boundary_lines[i].draw(image, color, stroke_width, line_type, shift)

		return image

	def reflect(self, x, y, z, about_point=None):
		if about_point is None: about_point = self.rect_info.center

		self.data_points = []
		self.closed = False

		return self.calculate()

	def shear(self, x=0, y=0, z=0, about_point=None):
		if about_point is None: about_point = self.rect_info.center

		self.data_points = []
		self.closed = False

		for i in range(len(self.boundary_lines)):
			line = boundary_lines[i]
			line.shear(x, y, z)
			data_points.append(line)

		return self.calculate()

	def scale(self, x=0, y=0, z=0, about_point=None):
		tx = 0
		ty = 0
		tz = 0

		if about_point is not None:
			tx = about_point.x / 2.0
			ty = about_point.y / 2.0
			tz = about_point.z / 2.0

		self.data_points = []
		self.closed = False

		for i in range(len(self.boundary_lines)):
			line = self.boundary_lines[i]
			line.scale(x, y, z)
			line.translate(tx, ty, tz)
			data_points.append(line)

		return self.calculate()

	def rotate(self, angle, about_point=None):
		if about_point is None: about_point = self.rect_info.center

		self.data_points = []
		self.closed = False

		for i in range(len(self.boundary_lines)):
			line = self.boundary_lines[i]
			line.rotate(angle, about_point)
			self.data_points.append(line.start)

		return self.calculate()

	def translate(self, x=0, y=0, z=0):
		self.data_points = []
		self.closed = False

		for i in range(len(self.boundary_lines)):
			line = self.boundary_lines[i]
			line.translate(x, y, z)
			data_points.append(line)

		return self.calculate()

	def fuzzy_compare(self, other):
		# based on the difference in the number of sizes
		sides_diff = abs(len(boundary_lines) - len(other.boundary_lines))

		# based on the distance between the centroid and geometric center of the path
		controid_diff = abs( pi_arithmetic.measure(self.rect_info.center, self.calculate_centroid()) - pi_arithmetic.measure(other.rect_info.center, other.calculate_centroid()) )

		return 0.0

	def calculate_centroid(self):
		# for a non-self-intersecting path

		cx = cy = 0
		scale = 1.0 / (6.0 * self.calculate_signed_area())

		for i in range(len(self.data_points)):
			next_index = (i + 1)  % len(self.data_points)
			cx += (self.xs[i] + self.xs[next_index]) * ((self.xs[i] * self.ys[next_index]) - (self.xs[next_index] * self.ys[i]))
			cy += (self.ys[i] + self.ys[next_index]) * ((self.xs[i] * self.ys[next_index]) - (self.xs[next_index] * self.ys[i]))

		return pi_point.Point(cx * scale, cy * scale)

	def calculate_signed_area(self):
		var = 0;
		for i in range(len(self.data_points)):
			next_index = (i + 1)  % len(self.data_points)
			var += (self.xs[i] * self.ys[next_index]) - (self.xs[next_index] * self.ys[i])
		return 0.5 * var;

	def calculate(self):
		if not self.closed: self.data_points.append( self.data_points[0] )

		for i in range(len(self.data_points)):
			point = self.data_points[i]
			self.xs.append(point.x)
			self.ys.append(point.y)

		self.boundary_lines = []
		perimeter = 0

		for i in range(len(self.data_points)-1):
			start = self.data_points[i]
			end = self.data_points[i+1]

			self.line = pi_line.Line(start, end)
			self.boundary_lines.append(self.line)

			perimeter += abs(self.line.get_length())

			self.rect_info.top_left     = pi_point.Point(min(self.xs), min(self.ys))
			self.rect_info.width        = max(self.xs) - self.rect_info.top_left.x
			self.rect_info.height       = max(self.ys) - self.rect_info.top_left.y
			self.rect_info.bottom_right = pi_point.Point(self.rect_info.top_left.x + self.rect_info.width, self.rect_info.top_left.y + self.rect_info.height)
			self.rect_info.area         = self.rect_info.width * self.rect_info.height
			self.rect_info.radius       = math.sqrt(pow(self.rect_info.width/2.0, 2) + pow(self.rect_info.height/2.0, 2)) / 2.0
			self.rect_info.center       = pi_point.Point(self.rect_info.top_left.x + (self.rect_info.width/2.0), self.rect_info.top_left.y + (self.rect_info.height/2.0))
			self.rect_info.perimeter    = perimeter

			mn = min(self.rect_info.width, self.rect_info.height)
			mx = max(self.rect_info.width, self.rect_info.height)

			self.ratio = 0 if ((mn <= 0) or (mx <= 0)) else mn / mx
			
		return True
	
	def as_np_index(self):
		return ( np.array(self.ys, dtype=np.int64), np.array(self.xs, dtype=np.int64) )
	
	def get_as_contour(self):
		xys = np.array(zip(self.xs, self.ys), dtype=np.int32)
		xys.reshape((len(self.ys), 1, 2))

		return xys

	def get_as_dictionary(self):
		params = {
			"xs": self.xs,
			"ys": self.ys,
			"data_points": self.data_points,
			"boundary_lines": self.boundary_lines,
			"closed": self.closed,
			"rect_info": self.rect_info
		}

		return params

	def get_as_deep_dictionary(self):
		params = {
			"xs": self.xs,
			"ys": self.ys,
			"data_points": [i.get_as_deep_dictionary() for i in self.data_points],
			"boundary_lines": [i.get_as_deep_dictionary() for i in self.boundary_lines],
			"closed": self.closed,
			"rect_info": self.rect_info.get_as_deep_dictionary()
		}

		return params


def test_path():
	path = Path()
	print ("path = ", path.get_as_dictionary())

if __name__ == '__main__':
	def test():
		test_path()

	test()