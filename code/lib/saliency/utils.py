# utilities

import sys
import os
import math
import itertools
import cv2 as cv
import numpy as np


class Util:
	def normalize_range(self, src, begin=0, end=255):
		dst = np.zeros((len(src), len(src[0])))
		amin, amax = np.amin(src), np.amax(src)
		for y, x in itertools.product(xrange(len(src)), xrange(len(src[0]))):
			if amin != amax:
				dst[y][x] = (src[y][x] - amin) * (end - begin) / (amax - amin) + begin
			else:
				dst[y][x] = (end + begin) / 2.
		return dst

	def normalize(self, src):
		src = self.normalize_range(src, 0., 1.)
		amax = np.amax(src)
		maxs = []

		for y in xrange(1, len(src) - 1):
			for x in xrange(1, len(src[0]) - 1):
				val = src[y][x]
				if val == amax:
					continue
				if val > src[y - 1][x] and val > src[y + 1][x] and val > src[y][x - 1] and val > src[y][x + 1]:
					maxs.append(val)

		if len(maxs) != 0:
			src *= math.pow(amax - (np.sum(maxs) / np.float64(len(maxs))), 2.)

		return src
