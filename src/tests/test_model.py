import logging
import unittest
from pathlib import Path
from unittest.mock import MagicMock

import cv2

from ocr.reader import AttachmentsReader
from ocr.text import text, orientation

BASE_PATH = Path(__file__).resolve().parent


class TestModel(unittest.TestCase):
    # Set log level to info
    logging.getLogger().setLevel(logging.INFO)

    def test_preprocess(self):
        # Arrange
        ocr = MagicMock()
        ocr.process_ocr = lambda *args: ("REPUBLIQUE FRANCAISE", 40.89)

        attachments_reader = AttachmentsReader(logging, ocr)

        # Act
        input_file = str(BASE_PATH / 'input/specimen_cni.png')
        with open(input_file, 'rb') as file:
            result = attachments_reader.process_file(file, False)

            # Assert
            self.assertEqual("REPUBLIQUE FRANCAISE", result["ocr"]["text"])
            self.assertEqual(40.89, result["ocr"]["confidence"])

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

    def test_is_too_small_image(self):
        input_file = str(BASE_PATH / 'input/small_image_test.png')
        ocr = MagicMock()
        attachments_reader = AttachmentsReader(logging, ocr)
        with open(input_file, 'rb') as file:
            result = attachments_reader.process_file(file, False)
            self.assertEqual(False, result["check"]["correct_size"])
