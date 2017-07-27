import numpy as np
import matplotlib.pyplot as plt
from skimage.draw import polygon
from scipy.sparse import diags
from scipy.sparse import vstack
from scipy.sparse.linalg import lsqr

# pad a direction of the mask
def shift(m, direction):
	padded = np.pad(m, [(d, 0) if d>0 else (0, -d) for d in direction], mode='constant')
	return padded[[np.s_[:sh] if d>0 else np.s_[-sh:] for sh, d in zip(m.shape, direction)]]

# pad the mask
def inside(mask):
	return shift(mask, (-1, 0)) & shift(mask, (0, -1)) & shift(mask, (1, 0)) & shift(mask, (0, 1))

# used to select points to align the image
def get_outline(im, cmd):
	# draw picture and command
	fig = plt.figure()
	plt.imshow(im, cmap='gray', vmin=0, vmax=1)
	plt.title(cmd)
	ax = plt.axis()
	plt.xlim(ax[0], ax[1])
	plt.ylim(ax[2], ax[3])
	# selected points
	pts = []
	# start input
	while True:
		# get inouts, store and draw them
		x, y = plt.ginput(n=1, timeout=0)[0]
		x = int(x)
		y = int(y)
		if pts and (x, y) == pts[-1]:
			break
		pts.append((x, y))
		xs, ys = zip(*pts)
		plt.plot(xs, ys, 'ko-')
		plt.draw()
	# close the window
	plt.close('all')
	# return the array of input points
	return np.array(xs), np.array(ys)

# form a real mask according to the points given
def get_mask(im, ys, xs, alt=""):
	rr, cc = polygon(ys, xs)
	mask = np.zeros(im.shape)
	mask[rr, cc] = 1.0
	# img_write(DIR_OUT + "mask" + alt + ".jpg", mask, False)
	return mask