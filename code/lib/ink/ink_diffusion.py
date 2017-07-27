
import random
import cv2
import numpy as np

def ink_diffusion(img, R=10): # empiracally R = 2k (here k = 2n + 1)
	# print "hello ink diffusion"
	diffusion_img = ink_particles(img, R=R)
	return diffusion_img

# random spread
def ink_particles(img, R):
	# img = img * 2
	particles_img = img
	height, width, colors = particles_img.shape
	# print height, width, colors
	for i in range(height): # [0, height - 1]
		for j in range(width):
			min_i = max(0, i - R)
			max_i = min(height - 1, i + R)
			min_j = max(0, j - R)
			max_j = min(width - 1, j + R)
			goal_i = get_random(min_i, max_i)
			goal_j = get_random(min_j, max_j)
			# print goal_i, goal_j
			# raw_input("pause")
			particles_img[i, j] = img[goal_i, goal_j]
	return particles_img

def median_blur(img, n=5):
	# blur_img = cv2.medianBlur(img, n)
	blur_img = img
	height, width, colors = blur_img.shape
	array = []
	for i in range(height): # [0, height - 1]
		for j in range(width):
			array = [[],[],[]]
			min_i = max(0, i - n)
			max_i = min(height - 1, i + n)
			min_j = max(0, j - n)
			max_j = min(width - 1, j + n)
			for idx_i in range(min_i, max_i + 1):
				for idx_j in range(min_j, max_j + 1):
					array[0].append(img[idx_i, idx_j, 0])
					array[1].append(img[idx_i, idx_j, 1])
					array[2].append(img[idx_i, idx_j, 2])
			# raw_input("")
			blur_img[i, j] = [get_mid(array[0]), get_mid(array[1]), get_mid(array[2])]
			del array[2]
			del array[1]
			del array[0]
			# particles_img[i, j] = img[idx_i, idx_j]
	return blur_img


def get_mid(array):
	# return np.median(array)
	return np.nanmedian(array)

# https://docs.python.org/2/library/random.html#random.SystemRandom
def get_random(min_val, max_val, mode="int"):
	# get a random number
	if mode=="int":
		return int_random(min_val, max_val)
	# elif mode=="float":
		#
	# print "get a random number"

def int_random(min_val, max_val):
	return random.randint(min_val, max_val)

def unit_random(): # 0.0 ~ 1.0
	return random.random()

def char_random(string):
	return random.choice(string)

def float_random(min_val, max_val):
	return random.uniform(min_val, max_val)

###### _saliaware
def ink_diffusion_saliaware(img, R_ref): # empiracally R = 2n
	# print "hello ink diffusion"
	diffusion_img = ink_particles_saliaware(img, R_ref=R_ref)
	# particles_img = ink_particles(img, R=R)
	# diffusion_img = median_blur(particles_img, n=n)
	# diffusion_img = cv2.medianBlur(particles_img, 5)
	return diffusion_img

def getR(ref_val):
	if ref_val < 0.3: #0.3:
		return 2
	if ref_val > 0.6: #0.8:
		return 0
	return 1
# random spread
def ink_particles_saliaware(img, R_ref):
	# img = img * 2
	particles_img = img
	height, width, colors = particles_img.shape
	# print height, width, colors
	for i in range(height): # [0, height - 1]
		for j in range(width):
			R = getR(R_ref[i, j])
			min_i = max(0, i - R)
			max_i = min(height - 1, i + R)
			min_j = max(0, j - R)
			max_j = min(width - 1, j + R)
			goal_i = get_random(min_i, max_i)
			goal_j = get_random(min_j, max_j)
			# print goal_i, goal_j
			# raw_input("pause")
			particles_img[i, j] = img[goal_i, goal_j]
	return particles_img

def getN(ref_val):
	if ref_val > 0.4: # 0.6
		return 0
	return 1

def median_blur_saliaware(img, n_ref):
	# blur_img = cv2.medianBlur(img, n)
	blur_img = img
	height, width, colors = blur_img.shape
	array = []
	for i in range(height): # [0, height - 1]
		for j in range(width):
			n = getN(n_ref[i, j])
			array = [[],[],[]]
			min_i = max(0, i - n)
			max_i = min(height - 1, i + n)
			min_j = max(0, j - n)
			max_j = min(width - 1, j + n)
			for idx_i in range(min_i, max_i + 1):
				for idx_j in range(min_j, max_j + 1):
					array[0].append(img[idx_i, idx_j, 0])
					array[1].append(img[idx_i, idx_j, 1])
					array[2].append(img[idx_i, idx_j, 2])
			# raw_input("")
			blur_img[i, j] = [get_mid(array[0]), get_mid(array[1]), get_mid(array[2])]
			del array[2]
			del array[1]
			del array[0]
			# particles_img[i, j] = img[idx_i, idx_j]
	return blur_img