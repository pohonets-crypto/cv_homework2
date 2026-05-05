"""
Applies logarithmic transformation on an image. Takes image, levels and c as parameters.
Returns the new image
"""

import numpy as np
import imutil


def log_transform(im, levels, c):
#create output image
    im_out = np.zeros((im.shape[0],im.shape[1],3), dtype=np.uint8)
#if image is gray
    if imutil.is_gray(im):
        im_out = np.zeros((im.shape[0],im.shape[1]), dtype=np.uint8)
#since opencv handles gray images like 3-channel image, reduce the channel size
        im = imutil.correct_gray(im)
#get height and width
#normalize the image to perform logarithmic transform
        im_out = im/(levels-1)
#apply the formula
        im_out = c*np.log(1+im_out)
#normalize in range 0...255
        im_out = (im_out / im_out.max()) * (levels-1)
    else:
#convert to YCbCr
        im_out = imutil.rgb2ycbcr(im)
        dMat = im_out[:, :, 0].astype(float)
        dMat = dMat/(levels-1)
        dMat = c*np.log(1 + (dMat))
        im_out[:, :, 0] = (dMat / dMat.max()) * (levels-1)
#convert back to RGB
        im_out = imutil.ycbcr2rgb(im_out)
    return np.uint8(im_out)