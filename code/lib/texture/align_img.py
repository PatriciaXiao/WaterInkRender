# from img_rw import img_read, img_write, img_check
from least_squares import least_squares_calc
from get_mask import get_mask, get_outline

from skimage.transform import rescale

# global variables
# from global_variables import *

# return the range of the mask
def mask_range(ys, xs):
	x_range = max(xs) - min(xs)
	y_range = max(ys) - min(ys)
	max_size = (y_range, x_range)
	top_left = (min(ys), min(xs))
	return max_size, top_left

# input: image and mask (indicated by x and y)
def crop_to_mask(im, ys, xs):
	# crop the source image to mask
	im_mask = get_mask(im, ys, xs)
	im_max, im_topleft = mask_range(ys, xs)
	im = im[min(ys):max(ys), min(xs):max(xs), :]
	im_mask = im_mask[min(ys):max(ys), min(xs):max(xs), :]
	return im, im_mask

# match the source image to selected area in target image
def match_box(s, s_mask, s_max, t_max):
	# Resize foreground and mask so area fits in box
	y_ratio = float(t_max[0])/s_max[0]
	x_ratio = float(t_max[1])/s_max[1]
	if y_ratio > x_ratio:
		s = rescale(s, x_ratio)
		s_mask = rescale(s_mask, x_ratio)
	else:
		s = rescale(s, y_ratio)
		s_mask = rescale(s_mask, y_ratio)
	return s, s_mask

# do everything needed to align images
def align_images(s, t):
	# get mask boarders from source image (now it is points)
	cmd = 'Outline the selected area by clicking points of its boundary.\nDouble-click on the last point to exit.'
	s_xs, s_ys = get_outline(s, cmd)
	# get area boarders from target image (now it is points)
	cmd = 'Draw a polygon by clicking points.\nDouble-click on the last point to exit.'
	t_xs, t_ys = get_outline(t, cmd)
	# get the mask range information (max size and top left)
	t_max, t_topleft = mask_range(t_ys, t_xs)
	s_max, s_topleft = mask_range(s_ys, s_xs)
	# crop the source image to mask image
	s, s_mask = crop_to_mask(s, s_ys, s_xs)
	# match the source image to selected area
	s, s_mask = match_box(s, s_mask, s_max, t_max)
	if s.shape != s_mask.shape:
		print "Error: mask size not match the source image size."
	assert s.shape == s_mask.shape

	# align the cropped, matched, source image to the target area
	ty, tx = t_topleft
	sy, sx, sc = s_mask.shape
	offset_y, offset_x = (t_max[0] - sy, t_max[1] - sx)	
	# the goal area's top left and area
	area_t_topleft = (ty + offset_y, tx + offset_x)
	area_t = t[ty + offset_y : ty + offset_y + sy,
			  tx + offset_x : tx + offset_x + sx, :].copy()

	return s, s_mask.astype(bool), area_t, area_t_topleft

