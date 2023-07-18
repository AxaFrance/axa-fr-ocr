import time
from io import BytesIO

import cv2
import numpy as np

from .i_ocr import IOcr
from .text.deskew import deskew
from .text.orientation import orientate
from .text.text import is_image_contain_text


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


class AttachmentsReader:
    def __init__(self, logging, ocr: IOcr):
        self.ocr = ocr
        self.logger = logging.getLogger(__name__)

    def process_file(self, file_obj, is_debug=False) -> dict:
        check_start = time.time()
        nparr = np.frombuffer(file_obj.read(), np.uint8)
        image_origin = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if not is_superior_to_min_size(image_origin, 1000):
            return {
                "check": {
                    "correct_size": False,
                    "contain_text": False,
                    "distance": 0,
                    "duration": 0,
                    "file_bytes_ocr_check": None,
                },
                "straightening": {
                    "deskew_duration": 0,
                    "orientate_duration": 0,
                    "duration": 0,
                    "angle_orientation": 0,
                    "angle_deskew": 0,
                    "file_bytes_ocr_straightening": None,
                },
                "is_debug": True,
                "ocr": {"text": "", "duration": 0, "confidence": 0},
            }

        image_cv, ratio_cv = normalize_size(image_origin, 2200)
        small_img_cv, ratio = normalize_size(image_cv, 800)
        is_img_with_text, distance, img_mser_cv = is_image_contain_text(small_img_cv)
        check_duration = time.time() - check_start
        if not is_img_with_text:
            if is_debug:
                return {
                    "check": {
                        "correct_size": True,
                        "contain_text": False,
                        "distance": distance,
                        "duration": check_duration,
                        "file_bytes_ocr_check": BytesIO(cv2.imencode(".png", img_mser_cv)[1].tobytes()),
                    },
                    "straightening": {
                        "deskew_duration": 0,
                        "orientate_duration": 0,
                        "duration": 0,
                        "angle_orientation": 0,
                        "angle_deskew": 0,
                        "file_bytes_ocr_straightening": None,
                    },
                    "is_debug": True,
                    "ocr": {"text": "", "duration": 0, "confidence": 0},
                }
            else:
                return {
                    "check": {
                        "correct_size": True,
                        "contain_text": False,
                        "distance": distance,
                    },
                    "straightening": {
                        "angle_orientation": 0,
                        "angle_deskew": 0,
                    },
                    "is_debug": False,
                    "ocr": {"text": "", "confidence": 0},
                }
        deskew_start = time.time()
        angle_deskew = deskew(image_cv)
        img_deskew_cv = rotate(angle_deskew, image_cv)
        deskew_duration = time.time() - deskew_start
        orientate_start = time.time()
        img_straighted_cv, angle_orientation, duration_orientation = orientate(img_deskew_cv)
        orientate_duration = time.time() - orientate_start
        ocr_start = time.time()
        img_straighted = BytesIO(cv2.imencode(".png", img_straighted_cv)[1].tobytes())
        img_text, ocr_confidence = self.ocr.process_ocr(img_straighted)
        ocr_duration = time.time() - ocr_start
        if ocr_confidence < 40:
            img_text = ""
        if is_debug:
            return {
                "check": {
                    "contain_text": True,
                    "distance": distance,
                    "duration": check_duration,
                    "file_bytes_ocr_check": BytesIO(cv2.imencode(".png", img_mser_cv)[1].tobytes()),
                },
                "straightening": {
                    "deskew_duration": deskew_duration,
                    "orientate_duration": orientate_duration,
                    "duration": deskew_duration + orientate_duration,
                    "filename": "straightening.png",
                    "angle_orientation": angle_orientation,
                    "angle_deskew": angle_deskew,
                    "file_bytes_ocr_straightening": img_straighted,
                },
                "is_debug": True,
                "ocr": {
                    "text": img_text,
                    "duration": ocr_duration,
                    "confidence": ocr_confidence,
                },
            }
        else:
            return {
                "check": {
                    "contain_text": True,
                    "distance": distance,
                },
                "straightening": {
                    "filename": "straightening.png",
                    "angle_orientation": angle_orientation,
                    "angle_deskew": angle_deskew,
                    "file_bytes_ocr_straightening": img_straighted,
                },
                "is_debug": False,
                "ocr": {"text": img_text, "confidence": ocr_confidence},
            }


def extract_extension_from_str(file_name):
    extension = ""
    if file_name:
        splitted_name = file_name.split(".")
        if len(splitted_name) > 1:
            extension = f".{splitted_name[len(splitted_name) - 1]}"
    return extension
