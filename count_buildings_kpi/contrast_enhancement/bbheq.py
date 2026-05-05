'''
Equalizes histogram of an image with k levels using BBHE algorithm. Takes image and number of levels as parameters.
Returns the new image.
'''

import numpy as np
import imutil


def bbheq(im, levels):
    h, w = im.shape
    tot_pixs = h * w
#same as computing via for loops
    mean_im = im.mean()
#round it up and convert to int
    mean_im = int(round(mean_im))
#create hashmaps with ranges where each pixel can be 0 or 1
    im_l_hash = (im <= mean_im)
    im_u_hash = (im > mean_im)
#count the number of pixels for lower part and upper part
    im_l_pix_count = np.count_nonzero(im_l_hash)
    im_u_pix_count = np.count_nonzero(im_u_hash)
#allocate histograms
    im_l_hist = np.zeros(((mean_im) + 1))
    im_u_hist = np.zeros(((levels-1)-mean_im))
#create histograms according to formula
    for i in range(0,mean_im + 1):
        im_l_hist[i] = np.count_nonzero(im == i)
    for i in range(mean_im + 1, levels):
        im_u_hist[i-mean_im-1] = np.count_nonzero(im == i)
#allocate pdfs
    pdf_l = np.zeros(((mean_im) + 1))
    pdf_u = np.zeros(((levels-1)-mean_im))
#find pdfs
    for i in range(0,mean_im + 1):
        pdf_l[i] = im_l_hist[i]/im_l_pix_count
    for i in range(mean_im + 1, levels):
        pdf_u[i-mean_im-1] = im_u_hist[i-mean_im-1]/im_u_pix_count
#allocate cdfs
    cdf_l = np.zeros(((mean_im) + 1))
    cdf_u = np.zeros(((levels-1)-mean_im))
#find cdfs
    cdf_l[0] = pdf_l[0]
    for i in range(1,mean_im + 1):
        cdf_l[i] = pdf_l[i] + cdf_l[i-1]
    cdf_u[0] = pdf_u[0]
    for i in range(mean_im + 1, levels):
        cdf_u[i-mean_im-1] = pdf_u[i-mean_im-1] + cdf_u[i-mean_im-2]

#transform
    im2 = np.zeros((h, w))
    for j in range(0, h):
        for k in range(0, w):
            if (im_l_hash[j, k] == 1):
                im2[j, k] = int(round((mean_im))) * cdf_l[im[j, k]]
            elif(im_u_hash[j, k] == 1):
                im2[j, k] = int(round((mean_im) + 1)) + ((levels-1) - int(round(mean_im)+1)) * cdf_u[im[j, k]-mean_im-1]
    return im2

"""
Utility for bbheq, handles the cases for gray and RGB images
Returns the new image
"""
def bbheq_util(im, levels):
    im_out = im.copy()
    if imutil.is_gray(im):
        im = imutil.correct_gray(im)
        im_out = bbheq(im, levels)
    else:
        im_out = imutil.rgb2ycbcr(im)
        im_out[:,:,0] = bbheq(im_out[:,:,0], levels)
        im_out = imutil.ycbcr2rgb(im_out)
    return im_out
