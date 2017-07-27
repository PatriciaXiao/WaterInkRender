### libraries ###
from __future__ import division
import os
import cv2
import numpy as np
from skimage.exposure import rescale_intensity
import matplotlib.pyplot as plt
import math

# from lib.abstract.cartoon import cartoonize
# from lib.abstract import cartoon

from lib.resize.img_resize import getDownSize
from lib.abstract.segment import segmentation
from lib.saliency.saliency_map import getSaliencyMap
from lib.saliency.utils import Util
from lib.outline.edge import get_sharp, get_edge, Gaussian, Laplacian, get_edge_reverse
from lib.ink.ink_diffusion import ink_diffusion, median_blur, ink_diffusion_saliaware, median_blur_saliaware
from lib.texture.poisson_blending import poisson_blending

DIR_DAT = "img"
FOLD_I = "input"
FOLD_O = "output"
DIR_I = os.path.join(DIR_DAT, FOLD_I)
DIR_O = os.path.join(DIR_DAT, FOLD_O)

EPS = 1.e-4

COLOR_CHANNELS = ['red', 'green', 'blue']

class GuiLin_1:
	name = "guilin_1"
	suffix = ".jpg"
	folder = "GuiLin_1"
	background = None

class GuiLin_2:
	name = "guilin_2"
	suffix = ".jpeg"
	folder = "GuiLin_2"
	background = None

class GuiLin_3:
	name = "guilin_3"
	suffix = ".jpg"
	folder = "GuiLin_3"
	background = None

class GuiLin_4:
	name = "guilin_4"
	suffix = ".jpg"
	folder = "GuiLin_4"
	background = None

class Mountain_1:
	name = "mountain_1"
	suffix = ".jpg"
	folder = "Mountain_1"
	background = None

class Mountain_3:
	name = "mountain_3"
	suffix = ".jpg"
	folder = "Mountain_3"
	background = None

class Mountain_5:
	name = "mountain_5"
	suffix = ".jpg"
	folder = "Mountain_5"
	background = None

class HongLouMeng_1:
	name = "hongloumeng_1"
	suffix = ".jpg"
	folder = "HongLouMeng_1"
	background = None

class Snow_1:
	name = "snow"
	suffix = ".jpg"
	folder = "Snow_1"
	background = None

class Water_1:
	name = "water"
	suffix = ".jpg"
	folder = "Water_1"
	background = "background_water_1.jpg"

class FLAG:
	debug = True
	resize = True
	segment = True
	white = True
	outline = True
	saliency = True
	apply_saliency = True
	apply_saliency_edge = False#True
	ink_diffusion = True
	final = True
	background = True

class PARA:
	max_height = 1000#600
	max_width = 1000#600

# data
#DAT = [GuiLin_1, Mountain_1, HongLouMeng_1, Snow_1, GuiLin_2, Mountain_3, Water_1, Mountain_5, GuiLin_3, GuiLin_4]
DAT = [Mountain_1,Mountain_3]


### i/o ###
UTIL = Util()
def load_img(img_name, img_folder = None):
	if img_folder == None:
		img_path = os.path.join(DIR_I, img_name)
	else:
		img_path = os.path.join(DIR_O, img_folder, img_name)
	# return cv2.imread(fname, cv2.IMREAD_COLOR)
	img = cv2.imread(img_path)
	'''
	if img.mean() >= 1:
		img = img/255.0
	'''
	img = int2float_img(img)
	return img

def int2float_img(img):
	if img.mean() >= 1:
		img = img/255.0
	return img

def float2int_img(img):
	if img.mean() <= 1:
		img = np.floor(img * 255)
	return img

def save_img(img_raw, img_name, img_folder):
	img = float2int_img(img_raw)
	# img_path = os.path.join(DIR_O, img_folder, img_name)
	img_dir = os.path.join(DIR_O, img_folder)
	img_path = os.path.join(img_dir, img_name)
	create_dir(img_dir)
	cv2.imwrite(img_path, img)

def create_dir(new_dir):
	if not os.path.exists(new_dir):
		# os.mkdir(d)
		os.makedirs(new_dir) #multi-layer

def check_img(img_name, img_folder):
	img_path = os.path.join(DIR_O, img_folder, img_name)
	# print img_path
	return os.path.isfile(img_path)

# another pair
def img_read(fname, img_folder="", img_dir=DIR_O):
	# read in image
	fpath = os.path.join(img_dir, img_folder, fname)
	im = plt.imread(fpath)
	if np.max(im) > 1:
		im = im/255.
	# judge if it is a colored image
	if len(im.shape) == 2:
		img_color = False
	else:
		img_color = True
	# if not, create a fake rgb image
	if img_color == False:
		r = im
		g = im
		b = im
		im = cv2.merge([b, g, r])
	# return the results
	return im, img_color

def img_write(fname, im, color, img_folder):
	img_dir = os.path.join(DIR_O, img_folder)
	img_path = os.path.join(img_dir, fname)
	create_dir(img_dir)
	if color:
		im = rescale_intensity(im, in_range=(0, 1), out_range=(0, 1))
		plt.imsave(img_path, im, vmin=0, vmax=1)
	else:
		plt.imsave(img_path, im, cmap='gray', vmin=0, vmax=1)

def img_compare(im1, im2):
	# assert np.allclose(im1, im2, atol=1.e-4)
	if (np.allclose(im1, im2, atol=EPS)):
		print "the two images are approximately the same"
	else:
		print "the two images are different"

### show ### 
def show_img(img, title="press ESC to escape"):
	cv2.imshow(title, img)
	cv2.waitKey()
	cv2.destroyAllWindows()  

def dshow_img(img, title="press ESC to escape"):
	if FLAG.debug:
		return show_img(img, title)

## convert ###
def mat2img(mat):
	# turn to image
	return np.uint8(UTIL.normalize_range(mat))
