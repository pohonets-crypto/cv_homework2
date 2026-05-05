"""
Applies histogram sliding on an image. Takes image, levels, value and direction(ctrl) as parameters.
Returns the new image
"""

import numpy as np
import  imutil

def hist_slide(im, val, ctrl):
#create the output image
    im_out = np.zeros((im.shape[0],im.shape[1],3), dtype=np.uint8)
#slide the histogram while maintaining the boundaries

    if imutil.is_gray(im):
        im = imutil.correct_gray(im)
        im_out = im.copy()
        if(ctrl == 'inc'):
            lim = 255 - val
            im_out[im_out > lim] = 255
            im_out[im_out <= lim] += val
        else:
            lim = 0 + val
            im_out[im_out < lim] = 0
            im_out[im_out >= lim] -= val
# if rgb:
    else:
        img = imutil.rgb2ycbcr(im)
        im_out = img.copy()
        dMat = img[:,:,0]
        if(ctrl == 'dec'):
            lim = 255 + val
            dMat[dMat > lim] = 255
            dMat[dMat <= lim] += val
        else:
            lim = 0 + val
            dMat[dMat < lim] = 0
            dMat[dMat >= lim] -= val
        im_out[:,:,0] = dMat
        im_out = imutil.ycbcr2rgb(im_out)

    return np.uint8(im_out)