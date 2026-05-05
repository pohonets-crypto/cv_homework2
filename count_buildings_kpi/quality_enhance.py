import cv2
import numpy as np
from matplotlib import pyplot as plt


#----------------- 1 Гистограма  яскравості зображення ---------
img = cv2.imread('campus.png')
# img = cv2.imread('campus_fltr.jpg')
imS = cv2.resize(img, (600, 500))
cv2.imshow("img", imS)
plt.hist(img.ravel(), 256, range=(0, 256))
plt.show()
cv2.waitKey(0)
cv2.destroyAllWindows()

#-------------------- 3 Вирівнювання гістограми  --------------
img = cv2.imread('campus.png',0)
# img = cv2.imread('campus_fltr.jpg',0)
hist,bins = np.histogram(img.flatten(),256,range=(0,256))
cdf = hist.cumsum()
cdf_normalized = cdf * hist.max() / cdf.max()        # Визначення нормалізоуючої кривої
plt.plot(cdf_normalized, color = 'b')
plt.hist(img.flatten(),bins=256,range=(0,256), color = 'r')
plt.xlim([0,256])
plt.legend(('cdf','histogram'), loc = 'upper left')
plt.show()

cdf_m = np.ma.masked_equal(cdf,0)
cdf_m = (cdf_m - cdf_m.min())*255/(cdf_m.max()-cdf_m.min())

cdf = np.ma.filled(cdf_m,0).astype('uint8')
img2 = cdf[img]

img = cv2.imread('campus.png', 0)
equ = cv2.equalizeHist(img)
res = np.hstack((img,equ))
cv2.imwrite('campus_equalizeHist.jpg',res)

imS = cv2.resize(res, (800, 300))
plt.imshow(imS)
plt.show()