from dataclasses import dataclass
from threading import Lock

from tesserocr import PyTessBaseAPI, OEM, PSM
from typing import Tuple

lock = Lock()
api_pool = []

@dataclass
class OcrParams:
    lang: str = "fra"
    psm: int = PSM.SINGLE_BLOCK
    api_pool_size: int = 10
    tess_data_path: str = '/opt/app-root/tessdata/'

class PyTessBaseAPIPool:

    def __init__(self, logging, params:OcrParams=OcrParams()):
        logger = logging.getLogger(__name__)
        self.logger = logger
        self.params = params

    def acquire(self):
        global api_pool
        with lock:
            if len(api_pool) > 0:
                return api_pool.pop()
        return self.create_tessbase_api()

    def release(self, api):
        api.Clear()
        global api_pool
        with lock:
            if len(api_pool) < self.params.api_pool_size:
                api_pool.append(api)

    def create_tessbase_api(self):
        params= self.params
        return PyTessBaseAPI(
            path=params.tess_data_path,
            lang=params.lang,
            oem=OEM.LSTM_ONLY,
            psm=params.psm
        )

    @staticmethod
    def process_ocr(api: PyTessBaseAPI, img_pil) \
            -> Tuple[float, str]:
        api.SetImage(img_pil)
        content = api.GetUTF8Text().strip()
        confidence = api.MeanTextConf()
        return confidence, content
