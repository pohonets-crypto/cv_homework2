'''
Спробувала виділити контури будівель кампусу КПІ
'''

import cv2
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image, ImageEnhance, ImageFilter


def image_read(file_name):
    image = cv2.imread(file_name)
    return image


def filter_image(img_cv):
    img_pil = Image.fromarray(cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB))

    img_contrast = ImageEnhance.Contrast(img_pil).enhance(1.5)

    img_sharpness = ImageEnhance.Sharpness(img_contrast).enhance(2.0)

    img_edges = img_sharpness.filter(ImageFilter.EDGE_ENHANCE)

    img_cv_filtered = cv2.cvtColor(np.array(img_edges), cv2.COLOR_RGB2BGR)
    return img_cv_filtered


def image_processing(image):

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # корекція кольору
    gray = cv2.GaussianBlur(gray, (7, 7), 0)  # Гаусова фільтрація
    edged = cv2.Canny(gray, 50, 250)  # фільтр Кенні - векторизація
    plt.imshow(edged)
    plt.show()


    contours, _ = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    min_area = 500
    building_count = 0

    for cnt in contours:
        if cv2.contourArea(cnt) > min_area:
            building_count += 1
            cv2.drawContours(image, [cnt], -1, (0, 255, 0), 2)

    print(f"Знайдено будівель: {building_count}")
    cv2.imshow("Result", image)
    # cv2.waitKey(0)



if __name__ == "__main__":
    image = image_read("campus_out.jpg")
    # fltr = filter_image(image)
    # cv2.imwrite("campus_fltr.jpg", fltr)
    plt.imshow(image, cmap='gray')
    plt.show()
    image_processing(image)
