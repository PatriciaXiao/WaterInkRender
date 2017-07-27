from __future__ import division
import cv2
from scipy.misc import imresize
import numpy as np
from skimage.exposure import rescale_intensity
import math

from bilateralfilter import bilateralFilter

BRIGHT = 2.0

def normalize_lab(image_lab):
	return image_lab[:,:,0]*(100/255)

def segmentation(img, kernel_size=5, kernel_sigma=[3,2], q_level=10, sigmaE=0.5, phiE=1.0, T=0.99):
	image = imresize(img, 0.5)
	shape = image.shape   
	#print "dimension: %dx%dx%d"%(shape[0], shape[1], shape[2])
	image_lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
	image_l = normalize_lab(image_lab)
	counter = 0
	# Applying bilateral filter  
	
	while counter<2:	
		image_l = bilateralFilter(image_l, kernel_size, kernel_sigma)
		counter += 1
	counter = 0
	I = quantize(image_l, q_level)

	while counter<2: 
		image_l = bilateralFilter(image_l, kernel_size, kernel_sigma)
		counter += 1

	out = BRIGHT * I
	out_final = np.empty(shape, dtype=np.uint8)
	out_final[:,:,0] = out
	out_final[:,:,1] = image_lab[:,:,1]
	out_final[:,:,2] = image_lab[:,:,2]
	out_final = imresize(out_final, 2.0)

	img_seg = cv2.cvtColor(out_final, cv2.COLOR_LAB2BGR) 
	return img_seg

def quantize(image, q_level):
	im_shape = image.shape
	for j in range(im_shape[1]):
		for i in range(im_shape[0]):
			image[i, j] = math.ceil(image[i, j]/10.0) * q_level
	return image