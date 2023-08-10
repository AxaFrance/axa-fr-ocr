import cv2


def image_resize(image, width=None, height=None, inter=cv2.INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    (h, w) = image.shape[:2]

    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image, 1

    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        ratio = height / float(h)
        dim = (int(w * ratio), height)

    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        ratio = width / float(w)
        dim = (width, int(h * ratio))

    # resize the image
    resized = cv2.resize(image, dim, interpolation=inter)

    # return the resized image
    return resized, ratio


def normalize_size(target_img, max_size):
    ratio = 1
    if target_img.shape[1] > target_img.shape[0] and target_img.shape[1] > max_size:
        target_img, ratio = image_resize(target_img, width=max_size)

    if target_img.shape[0] >= target_img.shape[1] or target_img.shape[0] > max_size:
        target_img, ratio = image_resize(target_img, height=max_size)

    return target_img, ratio


def is_superior_to_min_size(target_img, max_size):
    if target_img.shape[0] > max_size and target_img.shape[1] > max_size:
        return True
    return False


def rotate(angle, image):

    if angle == 0:
        return image

    if angle >= 180:
        image = cv2.rotate(image, cv2.ROTATE_180)
        angle = angle - 180

    if angle <= -180:
        image = cv2.rotate(image, cv2.ROTATE_180)
        angle = angle + 180

    if 67.5 <= angle:
        image = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
        angle = angle - 90

    if angle <= -67.5:
        image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
        angle = angle + 90

    if angle == 0:
        return image

    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated_img_cv = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

    return rotated_img_cv
