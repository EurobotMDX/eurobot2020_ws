#!/usr/bin/env python

import pi_point
import pi_line
import pi_path


def test_rect_info():
	rect_info = RectInfo()
	print ("rect_info = ", rect_info.get_as_dictionary())

if __name__ == '__main__':
	def test():
		test_rect_info()

	test()
