from scipy.misc import imresize

'''
# it also works but looks less formal, and I suspect that it is not the best way of implementing it
def downsize(img, max_height, max_width):
	# print img.shape # height, width, color_channels
	height, width, colors = img.shape
	# while (height > max_height or width > max_width):
	while (height > max_height or width > max_width):
		img = imresize(img, 0.5)
		height, width, colors = img.shape
	return img
'''

MAX_H = 1000
MAX_W = 1000

def getDownSize(img, max_height = MAX_H, max_width = MAX_W):
	dst = DownSize(img, max_height, max_width)
	return dst.img

class DownSize:
	def __init__(self, img, max_height = MAX_H, max_width = MAX_W):
		self.height_limit = max_height
		self.width_limit = max_width
		self.img = self.__downsize_img(img)
	def __downsize_img(self, img):
		height, width, colors = img.shape
		max_height=self.height_limit
		max_width=self.width_limit
		while (height > max_height or width > max_width):
			img = imresize(img, 0.5)
			height, width, colors = img.shape
		return img