"""
Applies contrast stretching on an image. Takes image an levels as parameters.
Returns the new image
"""

import numpy as np
import imutil


def cont_stretch(im, levels):
#create output image
    im_out = np.zeros((im.shape[0],im.shape[1],3), dtype=np.uint8)
#compute upper and lower bounds according to formula
    a, b = 0, levels-1
    c, d = im.min(), im.max()
#get image shape height, width and num. of channels and apply formula
    if imutil.is_gray(im):
        im_out = np.zeros((im.shape[0],im.shape[1]), dtype=np.uint8)
        im = imutil.correct_gray(im)
        h, w = im.shape
        im_out[0:h, 0:w] = (im[0:h, 0:w] - c)*((b - a)/(d-c)) + a
#apply formula for rgb , to prevent color distortion, use the same c and d values
    else:
        h, w, ch = im.shape
        img = imutil.rgb2ycbcr(im)
        dMat = img[:,:,0]
        dMat[0:h, 0:w] = (dMat[0:h, 0:w] - c)*((b - a)/(d-c)) + a
        img[:,:,0] = dMat
        im_out = imutil.ycbcr2rgb(img)

    return im_out
