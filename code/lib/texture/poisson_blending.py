# poisson blending
import numpy as np

# from img_rw import img_read, img_write, img_check
# from least_squares import least_squares_calc

from align_img import align_images
from least_squares import construct_A_poisson, lsqr_poisson_blend

# global variables
# from global_variables import *

# the process to do poisson blending
def poisson_blending(s, t, maximum):
	# read the images in: source and target
	# s, s_colored = img_read(DIR_IN + s_fname)
	# t, t_colored = img_read(DIR_IN + t_fname)

	# select & align source and target images and also get the mask
	s, s_mask, tinyt, tinyt_topleft = align_images(s, t)
	# recovery of mask
	s_mask = np.mean(s_mask, 2).astype(bool)
	# source image's channels
	sr = s[:, :, 0]
	sg = s[:, :, 1]
	sb = s[:, :, 2]	
	# tiny target's channels
	tr = tinyt[:, :, 0]
	tg = tinyt[:, :, 1]
	tb = tinyt[:, :, 2]
	# target image's channels, for final
	fr = t[:, :, 0]
	fg = t[:, :, 1]
	fb = t[:, :, 2]

	# blend each channel separately
	channels = []
	for i, (sc, tc, fc) in enumerate(zip([sr, sg, sb], [tr, tg, tb], [fr, fg, fb])):
		print 'blending No.{0} channel ... '.format(i)
		channels.append(lsqr_poisson_blend(sc, s_mask, tc, fc, tinyt_topleft, maximum = maximum))
	im_out = np.dstack(channels)
	return im_out