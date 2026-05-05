'''
Equalizes histogram of an image with k levels using DSIHE algorithm. Takes image and number of levels as parameters.
Returns the new image.
'''

import numpy as np
import imutil

def dsiheq(im, levels):
    h, w = im.shape
    tot_pixs = h * w
#allocate histogram, calculate pdf and cdf as done in classical HE algorithm
    im_hist = np.zeros((levels))
    for i in range(0,levels):
        im_hist[i] = np.count_nonzero(im == i)
    pdf = np.zeros((levels))
    for i in range(0,levels):
        pdf[i] = im_hist[i]/tot_pixs
    cdf = np.zeros((levels))
    cdf[0] = pdf[0]
    for i in range(1, levels):
        cdf[i] = pdf[i] + cdf[i-1]
    median = 0
    argmin_d = 1
#find the median according to the formula
    for i in range(0, levels):
        if abs(cdf[i]-((cdf[levels-1]+cdf[0])/2))<argmin_d:
            argmin_d = abs(cdf[i]-((cdf[levels-1]+cdf[0])/2))
            median = i
#same steps in BBHE, now divide image to two parts using median value and keep hashmaps
    im_l_hash = (im <= median - 1)
    im_u_hash = (im > median - 1)
#count number of pixels for each part
    im_l_pix_count = np.count_nonzero(im_l_hash)
    im_u_pix_count = np.count_nonzero(im_u_hash)
#allocate histograms
    im_l_hist = np.zeros((median))
    im_u_hist = np.zeros(((levels)-median))
#find histograms
    for i in range(0,median):
        im_l_hist[i] = np.count_nonzero(im == i)
    for i in range(median, levels):
        im_u_hist[i-median] = np.count_nonzero(im == i)
#allocate pdfs
    pdf_l = np.zeros((median))
    pdf_u = np.zeros(((levels)-median))

#find pdfs
    for i in range(0,median):
        pdf_l[i] = im_l_hist[i]/im_l_pix_count
    for i in range(median, levels):
        pdf_u[i-median] = im_u_hist[i-median]/im_u_pix_count
#allocate cdfs
    cdf_l = np.zeros((median))
    cdf_u = np.zeros(((levels)-median))
#find cdffs
    cdf_l[0] = pdf_l[0]
    for i in range(1,median):
        cdf_l[i] = pdf_l[i] + cdf_l[i-1]
    cdf_u[0] = pdf_u[0]
    for i in range(median + 1, levels):
        cdf_u[i-median] = pdf_u[i-median] + cdf_u[i-median-1]
#transform
    im2 = np.zeros((h,w))
    for j in range(0,h):
        for k in range(0,w):
            if(im_l_hash[j, k] == 1):
                im2[j, k] = int(round((median-1))) * cdf_l[im[j, k]]
            elif(im_u_hash[j, k] == 1):
                im2[j, k] = int(round((median))) +  ((levels-1) - int(round(median))) * cdf_u[im[j, k]-median]
    return im2
"""
Utility for dsiheq, handles the cases for gray and RGB images
Returns the new image
"""
def dsiheq_util(im, levels):
    im_out = im.copy()
    if imutil.is_gray(im):
        im = imutil.correct_gray(im)
        im_out = dsiheq(im, levels)
    else:
        im_out = imutil.rgb2ycbcr(im)
        im_out[:,:,0] = dsiheq(im_out[:,:,0], levels)
        im_out = imutil.ycbcr2rgb(im_out)
    return im_out
