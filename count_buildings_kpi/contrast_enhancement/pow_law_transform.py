"""
Applies power law(gamma) transformation on an image. Takes image, levels and c as parameters.
Returns the new image
"""

import numpy as np
import imutil


def pow_law_transform(im, levels, c, a):
#create output image
    im_out = np.zeros((im.shape[0],im.shape[1],3), dtype=np.uint8)
#if image is gray
    if imutil.is_gray(im):
        im_out = np.zeros((im.shape[0],im.shape[1]), dtype=np.uint8)
        im = imutil.correct_gray(im)
        im_out = im/(levels-1)
        im_out = c*(im_out**a)
        im_out = (im_out / im_out.max()) * (levels-1)
#if image is color
    else:
        im_out = imutil.rgb2ycbcr(im)
        dMat = im_out[:, :, 0]
        dMat = dMat/(levels-1)
        dMat = c*(dMat**a)
        im_out[:, :, 0] = dMat / dMat.max() * (levels-1)
        im_out = imutil.ycbcr2rgb(im_out)
    return np.uint8(im_out)
