import os

import cv2
import numpy as np
import time

def rotate(angle, image):
    if angle == 0:
        return image
    if angle == 90:
        return cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
    elif angle == 180:
        return cv2.rotate(image, cv2.ROTATE_180)
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated_img_cv = cv2.warpAffine(image, M, (w, h),
                                    flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return rotated_img_cv


def find_orientation(image, template):
    img_rgb = image
    if len(img_rgb.shape) == 3:
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    else:
        img_gray = image
    res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
    threshold = 0.6
    loc = np.where(res >= threshold)
    count = len(tuple(zip(*loc[::-1])))
    return count


BASE_PATH = os.path.dirname(os.path.abspath(__file__))
template_e = cv2.imread(os.path.join(BASE_PATH, "query_e.png"), 0)
def orientate(image):
    start_time = time.time()
    images = [image]
    counts = []
    counts.append(find_orientation(image, template_e))
    image = cv2.rotate(image, cv2.ROTATE_180)
    images.append(image)
    counts.append(find_orientation(image, template_e))

    max_count = 0
    max_index = 0
    for index, count in enumerate(counts):
        if count > max_count:
            max_count = count
            max_index = index

    duration = time.time() - start_time

    return images[max_index], (max_index*180), duration

