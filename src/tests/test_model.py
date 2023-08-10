import logging
import unittest
from pathlib import Path

import cv2

from axa_fr_ocr.text import text, orientation

BASE_PATH = Path(__file__).resolve().parent


class TestModel(unittest.TestCase):
    # Set log level to info
    logging.getLogger().setLevel(logging.INFO)

    def test_is_image(self):
        input_file = str(BASE_PATH / 'input/specimen.png')
        img = cv2.imread(input_file, cv2.IMREAD_COLOR)
        contain_text, distance, img_mser = text.is_image_contain_text(img)
        self.assertEqual(True, contain_text)

    def test_orientate_image(self):
        input_file = str(BASE_PATH / 'input/specimen_180.png')
        img = cv2.imread(input_file, cv2.IMREAD_COLOR)
        img_straighted_cv, angle_orientation, duration_orientation = orientation.orientate(img)
        self.assertEqual(180, angle_orientation)
