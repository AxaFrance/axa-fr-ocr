from typing import Tuple

from PIL import Image
from tesserocr import tesseract_version
from .i_ocr import IOcr
import re

from .py_tess_base_api_pool import PyTessBaseAPIPool, OcrParams


def clean_text_for_redis(text, confidence):
    if len(text) == 0:
        return '', 0

    text_cleaned = re.sub(r'[^a-zA-Z \n\réèçàùô\'ëî,\./@0-9:]', '', text)
    text_cleaned = '\n'.join(
        [line.strip() for line in text_cleaned.splitlines()])
    text_cleaned = re.sub(r'\n\s*\n', '\n', text_cleaned, re.MULTILINE)
    if len(text_cleaned) > 0 and len(text) / len(text_cleaned) >= 1.5:
        return '', 0

    return text_cleaned, confidence


class Ocr(IOcr):
    def __init__(self, logging,  params:OcrParams=OcrParams()):
        logger = logging.getLogger(__name__)
        self.logger = logger

        logger.info(tesseract_version())
        self.py_tess_api_pool = PyTessBaseAPIPool(logging, params)

    def process_ocr(self, image) -> Tuple[str, float]:
        logger = self.logger
        api = self.py_tess_api_pool.acquire()
        text, score = ('', 0)
        try:
            with Image.open(image) as img_pil:
                confidence, content = self.py_tess_api_pool.process_ocr(
                    api, img_pil)
                image.seek(0)
            text, score = clean_text_for_redis(content, confidence)
        except (IOError, SyntaxError) as e:
            logger.error(f'Bad file | {e}')
        except Image.DecompressionBombError as e:
            logger.error(f'Size limit exceeded | {e}')
        except Exception as e:
            logger.error(e)
        finally:
            self.py_tess_api_pool.release(api)
        return text, score
