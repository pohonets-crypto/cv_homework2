'''
Equalizes histogram of an image with k levels. Takes image and number of levels as parameters.
Returns the new image.
'''

import numpy as np
import imutil


def hist_eq(im, levels):
    h, w = im.shape
    tot_pixs = h * w
    im_hist = np.zeros((levels))
#count number of pixels for each level
    for i in range(0,levels):
        im_hist[i] = np.count_nonzero(im == i)
#find pdf
    pdf = np.zeros((levels))
    for i in range(0,levels):
        pdf[i] = im_hist[i]/tot_pixs
#find cdf
    cdf = np.zeros((levels))
    cdf[0] = pdf[0]
    for i in range(1, levels):
        cdf[i] = pdf[i] + cdf[i-1]
    im2 = np.zeros((h,w))
#transform
    for j in range(0,h):
        for k in range(0,w):
            im2[j, k] = int(round((levels-1) * cdf[im[j, k]]))
    return np.uint8(im2)
"""
Utility for hist_eq, handles the cases for gray and RGB images
Returns the new image
"""
def hist_eq_util(im, levels):
#detect if image is gray or rgb, do appropriate operations
    im_out = im.copy()
    if imutil.is_gray(im):
        im = imutil.correct_gray(im)
        im_out = hist_eq(im, levels)
    else:
        im_out = imutil.rgb2ycbcr(im)
        im_out[:,:,0] = hist_eq(im_out[:,:,0], levels)
        im_out = imutil.ycbcr2rgb(im_out)
    return im_out