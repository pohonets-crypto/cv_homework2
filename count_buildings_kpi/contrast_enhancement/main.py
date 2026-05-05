'''
Модуль головних викликів методів корекції яскравості та контрасту
https://emrecankuran.medium.com/a-guide-to-contrast-enhancement-transformation-functions-histogram-sliding-contrast-stretching-34149e5cdeed

'''

import cv2
from log_transform import *
from exp_transform import *
from pow_law_transform import *
from hist_slide import *
from hist_eq import hist_eq_util
from bbheq import bbheq_util
from dsiheq import dsiheq_util



def main():
#read images , get levels and results image
    im = cv2.imread('campus.png')
    levels = imutil.get_depth(im)
    # out = log_transform(im, levels, 2)
    # out = exp_transform(im, levels, 4, 0.5)
    # out = pow_law_transform(im, levels, 2, 0.5)
    # out = hist_slide(im, 50, 'dec')
    # out = hist_slide(im, 50, 'inc') # no
    # out = hist_eq_util(im, levels) #
    # out = bbheq_util(im, levels) # Nice
    out = dsiheq_util(im, levels)  # Nice
    cv2.imwrite("../campus_out.jpg", out)

#give the names for the titles of the images
    names = ['Original', 'Transformation']

#create image list
    im_list = [im, out]

#show images and their histograms
    imutil.im_plot(im_list, names, levels)
    imutil.hist_plot(im_list, names, levels)


if __name__ == "__main__":
    main()