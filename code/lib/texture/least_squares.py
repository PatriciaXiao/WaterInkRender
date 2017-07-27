import numpy as np
import matplotlib.pyplot as plt
from scipy.sparse import diags
from scipy.sparse import vstack
from scipy.sparse.linalg import lsqr

# for poisson blending
from get_mask import inside

# The first step is to write the objective function as a set of least squares 
#   constraints in the standard matrix form: (AV-b)^2. 
# Here, "A" is a sparse matrix, 
# "v" are the variables to be solved, intensity values "v" within the source region "S"
# and "b" is a known vector.

# [imh, imw, nb] = size(im); 
# im2var = zeros(imh, imw); 
# im2var(1:imh*imw) = 1:imh*imw;
# Objective 1: 
#    minimize ( v(x+1,y)-v(x,y) - (s(x+1,y)-s(x,y)) )^2   
#    the x-gradients of v should closely match the x-gradients of s
# e=e+1; 
# A(e, im2var(y,x+1))=1; 
# A(e, im2var(y,x))=-1;
# Objective 2: (similar with Obj 1)
#    minimize ( v(x,y+1)-v(x,y) - (s(x,y+1)-s(x,y)) )^2    
#    the y-gradients of v should closely match the y-gradients of s
#
# Objective 3: 
#    minimize (v(1,1)-s(1,1))^2  
#    The top left corners of the two images should be the same color
# e=e+1; 
# A(e, im2var(1,1))=1; 
# b(e)=s(1,1);
# To solve for v, use v = A\b; or v = lscov(A, b); 
# Then, copy each solved value to the appropriate pixel in the output image. 
def construct_A(S):
	height, width = S.shape
	n = height * width
	A = diags(
		diagonals=[1, -1, 1, -1, 1],
		offsets=[0, -1, -n, -n-width, -2*n], 
		shape=[2*n + 1, n],
		format='csr', 
		dtype=float)
	A[n, -1] = 0
	A[-1, -width] = 0
	return A

def least_squares_calc(S):
	height, width = S.shape
	A = construct_A(S)
	b = A.dot(S.ravel())
	v = lsqr(A, b)[0]
	return v.reshape((height, width))

##########################################################
# functions used in poisson blending and mixed gradients #
##########################################################

# calculate b value
def calc_b(b, mask, values):
	bigmask = np.concatenate([mask, mask, mask, mask])
	b[bigmask] = values[bigmask]
	return b

def construct_A_poisson(s, s_border=[[]]):
	imh, imw = s.shape
	sy, sx = np.where(s_border)
	npx = imh * imw
	# offsets are [x,x+1], [x,x-1], [y,y+1], [y,y-1]
	# these are what is used to calculate the gradient
	offsets_list = [[0, -1], [0, 1], [0, -imw], [0, imw]]
	As = []
	for offset in offsets_list:
		A = diags(
			diagonals=[1, -1],
			offsets=offset,
			shape=[npx, npx],
			format='csr',
			dtype=float)
		r, c = (A[imw*sy + sx, :] < 0).nonzero()
		A[(imw*sy + sx)[r], c] = 0
		r, c = A[imw*sy + sx, :].nonzero()
		As.append(A)
	return vstack(As)

def lsqr_poisson_blend(s, s_mask, area_t, t, area_t_topleft, maximum=False):
	# get the source image's mask's inside, boarder and outside
	s_inside = inside(s_mask)
	s_border = s_mask & ~s_inside
	s_outside = ~s_inside
	# get the top left point and the length of x / y of the tiny area in target image
	topleft_y, topleft_x = area_t_topleft
	len_y, len_x = area_t.shape

	# construct A using pixels from 4 directions
	A = construct_A_poisson(s)
	t_prime = A.dot(area_t.ravel())
	s_prime = A.dot(s.ravel())

	b = t_prime.copy() # calculating the known vector b value so that we can calculate v
	if maximum == True:
		max_prime = np.maximum(s_prime, t_prime)
		b = calc_b(b, s_inside.ravel(), max_prime)
	else:
		b = calc_b(b, s_inside.ravel(), s_prime)
	area_t_values = np.concatenate([area_t.ravel(), area_t.ravel(), area_t.ravel(), area_t.ravel()])
	b = calc_b(b, s_border.ravel(), area_t_values)

	A = construct_A_poisson(s, s_border=s_border)
	imh, imw = s.shape
	v = lsqr(A, b)[0]
	v_out = v.reshape((imh, imw)) # reshape it to the source image's size
	t[topleft_y:topleft_y + len_y, topleft_x:topleft_x + len_x] = v_out
	return t