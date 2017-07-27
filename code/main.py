### global libraries & functions & parameters
from config import *

# -2x^3 + 3x^2
#
# (-1/a^2)(x-a)^2 + 1; b = (-1)/(a^2); c=1
#		-(x^2/a^2) + (2/a)x
a = 0.4 #0.6
para2 = -1.0 / (a * a)
para1 = 2.0 / a
para3 = 0.8
para4 = 0.0
def fcolor(x):
	# [0, 1] -> [0, 1]
	if (x < a):
		# y = para3 * (para1 * x + para2 * x * x) + para4
		y = para1 * x + para2 * x * x
	else:
		y = 1
	return y
def whiten(img):
	if FLAG.white:
		print "whiten the segmented image"
		height, width, colors = img.shape
		for i in range(height):
			for j in range(width):
				img[i, j, 0] = fcolor(img[i, j, 0])
				img[i, j, 1] = fcolor(img[i, j, 1]) 
				img[i, j, 2] = fcolor(img[i, j, 2])
		max_val = np.max(img)
		min_val = np.min(img)
	return img


for data in DAT:
	### meta data
	in_name = data.name + data.suffix
	resized_name = data.name + "_resized" + data.suffix
	segment_name = data.name + "_segment" + data.suffix
	outline_name = data.name + "_outline" + data.suffix
	saliency_name = data.name + "_saliency" + data.suffix
	swimg_name = data.name + "_saliaware" + data.suffix
	blurr_name = data.name + "_blurred" + data.suffix
	sharpen_name = data.name + "_sharpen" + data.suffix
	edge_name = data.name + "_edge" + data.suffix
	sledge_name = data.name + "_saliency_edge" + data.suffix
	diffusion_name = data.name + "_diffusion" + data.suffix
	color_name = data.name + "_color" + data.suffix
	diffused_edge_name = data.name + "_diffedge" + data.suffix
	diffused_line_name = data.name + "_diffline" + data.suffix
	final_name = data.name + "_final" + data.suffix
	texture_name = data.name + "_texture" + data.suffix
	out_folder = data.folder
	### resize the image so that we can speed up...
	if FLAG.resize:
		if check_img(resized_name, out_folder):
			print "image {0} has already been resized as {1}".format(in_name, resized_name)
			img = load_img(resized_name, img_folder = out_folder)
			dshow_img(img, "image already resized, press ESC to eacape")
		else:
			print "resizing image {0}...".format(in_name)
			# resize the image
			img = load_img(in_name)
			dshow_img(img, "input image, press ESC to escape")
			# img_downsize = getDownSize(img, PARA.max_height, PARA.max_width)
			# img = img_downsize.img
			img = getDownSize(img, PARA.max_height, PARA.max_width)
			dshow_img(img, "resized image, press ESC to escape")

			save_img(img, resized_name, out_folder)
	else:
		img = load_img(in_name)

	### get the saliency map
	if FLAG.saliency:
		if check_img(saliency_name, out_folder):
			print "image {0}' has already been calculated, saved as {1}".format(in_name, saliency_name)
			img_sm = load_img(saliency_name, img_folder=out_folder)
			dshow_img(img_sm, "image saliency map already calculated, press ESC to escape")
			# print img_sm
		else:
			### get the saliency map
			print "calculating saliency map of the image {0}".format(in_name)
			img_sm_map = getSaliencyMap(img)
			img_sm = mat2img(img_sm_map)
			dshow_img(img_sm, "saliency map, press ESC to escape")
			save_img(img_sm, saliency_name, out_folder)
			img_sm = load_img(saliency_name, img_folder=out_folder)

	if FLAG.apply_saliency:
		if check_img(swimg_name, out_folder) and check_img(blurr_name, out_folder):
			img_saliency = load_img(swimg_name, img_folder=out_folder)
			img_blur = load_img(blurr_name, img_folder=out_folder)
			dshow_img(img_blur, "blurred image")
			dshow_img(img_saliency, "image saliency applied")
		else:
			img_sm = rescale_intensity(img_sm, in_range=(0, 1), out_range=(0, 1))
			img_blur = Gaussian(img, ksize=15)# Gaussian(img, ksize=21) # ksize should be odd number
			print "applying saliency map to image {0}".format(in_name)
			img_saliency = img_sm * img + (1 - img_sm) * img_blur
			save_img(img_blur, blurr_name, out_folder)
			save_img(img_saliency, swimg_name, out_folder)
			img_saliency = load_img(swimg_name, img_folder=out_folder)
			dshow_img(img_blur, "blurred image")
			dshow_img(img_saliency, "image saliency applied")
		img = img_saliency

	### take in input image & segment & get outline ###
	if FLAG.segment:
		if check_img(segment_name, out_folder):
			print "image {0} has already been segmented as {1}".format(in_name, segment_name)
			img_seg = load_img(segment_name, img_folder = out_folder)
			dshow_img(img_seg, "image already segmented, press ESC to eacape")
		else:
			print "segmentating image {0}...".format(in_name)
			# segmenting the image
			img_seg = segmentation(img)
			dshow_img(img_seg, "segmented image, press ESC to escape")
			img_seg = int2float_img(img_seg)
			img_seg = whiten(img_seg)
			dshow_img(img_seg, "whitened image, press ESC to escape")
			save_img(img_seg, segment_name, out_folder)
			img_seg = load_img(segment_name, img_folder = out_folder)
			img_seg = rescale_intensity(img_seg, in_range=(0, 1), out_range=(0, 1))

	### get the outline of the image
	if FLAG.outline:
		if check_img(sharpen_name, out_folder) and check_img(edge_name, out_folder) and check_img(outline_name, out_folder):
			img_sharp = load_img(sharpen_name, img_folder=out_folder)
			img_edge = load_img(edge_name, img_folder=out_folder)
			img_outline = load_img(outline_name, img_folder=out_folder)
			dshow_img(img_sharp, "sharpened image already existed, press ESC to escape")
			dshow_img(img_edge, "edge of the image already existed, press ESC to escape")
			dshow_img(img_outline, "outline of the image")
		else:
			print "outlining the original picture {0}".format(in_name)
			img_sharp = get_sharp(img)
			dshow_img(img_sharp, "sharpened image, press ESC to escape")
			save_img(img_sharp, sharpen_name, out_folder)
			img_edge = get_edge(img_sharp)
			dshow_img(img_edge, "edge of the image, press ESC to escape")
			save_img(img_edge, edge_name, out_folder)
			img_outline = Laplacian(img, sigma=10, ksize=5)
			img_outline= rescale_intensity(img_outline, in_range=(0, 1), out_range=(0, 1))
			img_outline = get_edge_reverse(img_outline)
			dshow_img(img_outline, "outline of the image, press ESC to escape")
			save_img(img_outline, outline_name, out_folder)
			# load_img(edge_name, img_folder=out_folder)

		# img_ink = 1 - img_edge
		'''	
		img_ink = img_edge - 1
		dshow_img(img_ink + img_seg)
		'''
		# print img_ink[0, 0]

	if FLAG.apply_saliency_edge:
		# dshow_img(img_edge, "edge of the image, press ESC to escape")
		img_edge = img_sm * img_edge + (1 - img_sm) * 1
		img_outline = img_sm * img_outline + (1 - img_sm) * 1
		'''
		img_ink = img_edge - 1
		dshow_img(img_ink + img_seg, "ink applied")
		'''
		

	# random ink points
	if FLAG.ink_diffusion:
		if check_img(diffusion_name, out_folder) and check_img(color_name, out_folder) and check_img(diffused_edge_name, out_folder) and check_img(diffused_line_name, out_folder):
			img_diffusion = load_img(diffusion_name, img_folder=out_folder)
			img_color = load_img(color_name, img_folder=out_folder)
			img_diffedge = load_img(diffused_edge_name, img_folder=out_folder)
			# img_diffline = load_img(diffused_line_name, img_folder=out_folder)
		else:
			print "ink difussion {0}".format(in_name)
			'''
			img_ink = img_edge - 1
			img_whole = img_ink + img_seg
			dshow_img(img_whole, "ink applied")
			'''
			img_diffusion = ink_diffusion(img_seg, R=4)
			dshow_img(img_diffusion, "ink diffusion")
			save_img(img_diffusion, diffusion_name, out_folder)
			# img_color = load_img("test1.jpg", img_folder=out_folder)
			img_color = median_blur(img_diffusion, n=2)
			img_color = Gaussian(img_color, sigma=10, ksize=5)
			dshow_img(img_color, "ink diffusion - blurred")
			save_img(img_color, color_name, out_folder)
			# edge
			
			edge_diffusion = ink_diffusion_saliaware(img_edge, R_ref=img_sm[:,:,0])
			dshow_img(edge_diffusion, "edge diffusion")
			img_diffedge = median_blur_saliaware(edge_diffusion, n_ref=img_sm[:,:,0])
			# img_diffedge = Gaussian(img_diffedge, sigma=1, ksize=3)
			# img_diffedge = Gaussian(dge_diffusion, sigma=1, ksize=3)
			dshow_img(img_diffedge, "ink diffusion - blurred")
			save_img(img_diffedge, diffused_edge_name, out_folder)
			# line
			outline_diffusion = ink_diffusion_saliaware(img_outline, R_ref=img_sm[:,:,0])
			dshow_img(outline_diffusion, "edge diffusion")
			img_diffline = median_blur_saliaware(outline_diffusion, n_ref=img_sm[:,:,0])
			dshow_img(img_diffline, "ink diffusion - blurred")
			save_img(img_diffline, diffused_line_name, out_folder)
			
			
		# img_edge = img_diffedge
	else:
		img_diffedge = 0

	if FLAG.final:
		if check_img(final_name, out_folder):
			img_final = load_img(final_name, img_folder=out_folder)
		else:
			assert FLAG.ink_diffusion, "ink diffusion must be applied first"
			assert FLAG.outline, "outline must be calculated first"
			img_ink = img_edge - 1
			img_ink_extend = img_diffedge - 1
			# img_ink_outline = img_outline - 1
			img_ink_outline = img_diffline - 1
			# img_ink_outline = rescale_intensity(img_ink_outline, in_range=(0, 1), out_range=(0, 1))
			height, width, colors = img_color.shape
			# img_final = img_ink_extend[:height, :width, :] * 0.4 + img_ink[:height, :width, :] * 0.6 + img_ink_outline[:height, :width, :] + img_color
			# img_final = img_ink_extend[:height, :width, :] * 1.2 + img_ink[:height, :width, :] * 0.8 + img_ink_outline[:height, :width, :] * 0.2 + img_color
			img_final = img_ink_extend[:height, :width, :] * 1.1 + img_ink[:height, :width, :] * 0.1 + img_ink_outline[:height, :width, :] * 0.1 + img_color
			# img_final = img_ink_extend * 0.2 + img_ink * 0.6 + img_color #img_ink_extend * 0.1 + img_ink * 0.6 + img_color
			# img_final = img_ink_extend * 0.8 + img_color #img_ink_extend * 0.1 + img_ink * 0.6 + img_color
			## img_final = img_ink_extend * 0.8 + img_color #img_ink_extend * 0.1 + img_ink * 0.6 + img_color
			img_final = rescale_intensity(img_final, in_range=(0, 1), out_range=(0, 1))
			dshow_img(img_final, "final image")
			save_img(img_final, final_name, out_folder)

	if FLAG.background:
		if data.background is not None:
			s, s_colored = img_read(final_name, img_folder=out_folder, img_dir=DIR_O)
			t, t_colored = img_read(data.background, img_dir=DIR_I)
			print 'Mixed gradient starting ...'
			im_texture = poisson_blending(s, t, True)
			img_write(texture_name, im_texture, s_colored and t_colored, img_folder=out_folder)
			print 'Mixed gradient ended successfully.'
			