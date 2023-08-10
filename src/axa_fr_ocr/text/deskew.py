import cv2
import numpy as np


def deskew(mser_img):
    img = mser_img
    if len(img.shape) == 2:
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    ret, thresh = cv2.threshold(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    kernel = np.ones((6, 6), np.uint8)
    erosion = cv2.dilate(thresh, kernel, iterations=1)
    contours, hier = cv2.findContours(erosion, cv2.RETR_EXTERNAL,
                                      cv2.CHAIN_APPROX_SIMPLE)

    number_higher, number_larger = count_larger_and_higher_rectangle(contours)

    is_rotated = False
    if number_higher > number_larger:
        erosion = cv2.rotate(erosion, cv2.ROTATE_90_CLOCKWISE)
        contours, hier = cv2.findContours(erosion, cv2.RETR_EXTERNAL,
                                          cv2.CHAIN_APPROX_SIMPLE)
        is_rotated = True

    angles = list_angles_from_rectangles(contours)

    if len(angles) == 0:
        return 0

    sorted_angles = np.sort(angles)
    mean_angle_threshold = compute_mean_angle(sorted_angles)

    angle_mean = compute_real_angle_from_mean(mean_angle_threshold, sorted_angles)

    if is_rotated:
        angle_mean = angle_mean + 90

    return round(angle_mean, 2)


def compute_real_angle_from_mean(mean_angle_threshold, sorted_angles):
    previous_angle = None
    final_array = [[]]
    index = 0
    for angle in sorted_angles:
        if previous_angle is not None and angle - previous_angle > mean_angle_threshold:
            index = index + 1
            final_array.append([])
        previous_angle = angle
        final_array[index].append(angle)
    max_array_length = []
    for array in final_array:
        if len(max_array_length) < len(array):
            max_array_length = array
    angle_mean = np.mean(np.array(max_array_length))
    return angle_mean


def compute_mean_angle(sorted_angles):
    previous_angle = None
    new_array = []
    for angle in sorted_angles:
        if previous_angle is not None:
            new_array.append(angle - previous_angle)
        previous_angle = angle
    return np.mean(np.array(new_array)) * 2


def list_angles_from_rectangles(contours):
    angles = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        if h * 3 < w < h * 16:
            min_rectangle = cv2.minAreaRect(contour)
            angle = min_rectangle[2] % 90
            if angle > 45:
                angle = angle - 90
            if angle < -45:
                angle = angle + 90
            angles.append(angle)
    return angles


def count_larger_and_higher_rectangle(contours):
    number_larger = 0
    number_higher = 0
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        if w > h:
            number_larger = number_larger + 1
        else:
            number_higher = number_higher + 1
    return number_higher, number_larger
