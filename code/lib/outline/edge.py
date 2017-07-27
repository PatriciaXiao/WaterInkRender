from __future__ import division
import cv2
import numpy as np
from skimage.filters import gaussian as gaussian_filter
from skimage.exposure import rescale_intensity
from skimage import color

# Gaussian(img, 0, 5)
# Gaussian(img, 10, 5)
def Gaussian(img, sigma=10, ksize=5):
	gs_img = cv2.GaussianBlur(img, (ksize, ksize), sigma) #gaussian_filter(img, sigma, mode='reflect') # single channel
	return gs_img

def Laplacian(img, sigma, ksize):
	lap_img = img - Gaussian(img, sigma, ksize)
	return lap_img

def get_sharp(img, sigma=10, ksize=5):
	if img.mean() >= 1:
		img_reg = img/255.0
	else:
		img_reg = img
	img_lap = Laplacian(img_reg, 10, 5)
	img_sharp = img_reg + img_lap
	img_sharp = rescale_intensity(img_sharp, in_range=(0, 1), out_range=(0, 1))
	return img_sharp

def get_edge(img):
	# print np.max(img), np.min(img)
	height, width, colors = img.shape
	threshold = 0.6 #0.24 # 0.2 #0.36 # 0.5 # 0.3 # the larger the darker
	phiE = 1.0 #1.0 # 6.0 # 10.0 # the larger the darker
	edge = img
	gray = color.rgb2gray(img)

	for i in range(height):
		for j in range(width):
			if gray[i, j] >= threshold:
				edge[i, j, 0] = 1
				edge[i, j, 1] = 1
				edge[i, j, 2] = 1
			elif gray[i, j] < threshold:
				# val = 1 - np.tanh(phiE * edge[i,j, 0])
				# val = 1 + np.tanh(phiE * (edge[i, j, 0] - threshold))
				val = 1 + np.tanh(phiE * (gray[i, j] - threshold))
				# val = 1 - np.tanh(phiE * gray[i, j])
				edge[i, j, 0] = val
				edge[i, j, 1] = val
				edge[i, j, 2] = val
	edge = rescale_intensity(edge, in_range=(0, 1), out_range=(0, 1))
	return edge

###
def get_edge_reverse(img):
	# print np.max(img), np.min(img)
	height, width, colors = img.shape
	# threshold = 0.1 #0.24 # 0.2 #0.36 # 0.5 # 0.3 # the larger the darker
	phiE = 3.0 #1.0 # 6.0 # 10.0 # the larger the darker
	edge = img
	gray = color.rgb2gray(img)

	for i in range(height):
		for j in range(width):
			val = 1 - np.tanh(phiE * gray[i, j])
			# val = 1 - np.tanh(phiE * gray[i, j])
			edge[i, j, 0] = val
			edge[i, j, 1] = val
			edge[i, j, 2] = val
	edge = rescale_intensity(edge, in_range=(0, 1), out_range=(0, 1))
	return edge