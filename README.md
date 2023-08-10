# @axa-fr/ocr

[//]: # ([![Continuous Integration]&#40;https://github.com/AxaFrance/axa-fr-ocr/actions/workflows/python-publish.yml/badge.svg&#41;]&#40;https://github.com/AxaFrance/axa-fr-ocr/actions/workflows/python-publish.yml&#41;)

[//]: # ([![Quality Gate]&#40;https://sonarcloud.io/api/project_badges/measure?project=<INSERT SONAR SPLITTER PROJECT>&metric=alert_status&#41;]&#40;https://sonarcloud.io/dashboard?id=<INSERT SONAR SPLITTER PROJECT>&#41;)

[//]: # ([![Reliability]&#40;https://sonarcloud.io/api/project_badges/measure?project=<INSERT SONAR SPLITTER PROJECT>&metric=reliability_rating&#41;]&#40;https://sonarcloud.io/component_measures?id=<INSERT SONAR SPLITTER PROJECT>&metric=reliability_rating&#41;)

[//]: # ([![Security]&#40;https://sonarcloud.io/api/project_badges/measure?project=<INSERT SONAR SPLITTER PROJECT>&metric=security_rating&#41;]&#40;https://sonarcloud.io/component_measures?id=A<INSERT SONAR SPLITTER PROJECT>&metric=security_rating&#41;)

[//]: # ([![Code Coverage]&#40;https://sonarcloud.io/api/project_badges/measure?project=<INSERT SONAR SPLITTER PROJECT>&metric=coverage&#41;]&#40;https://sonarcloud.io/component_measures?id=<INSERT SONAR SPLITTER PROJECT>&metric=Coverage&#41;)

[//]: # ([![Twitter]&#40;https://img.shields.io/twitter/follow/GuildDEvOpen?style=social&#41;]&#40;https://twitter.com/intent/follow?screen_name=GuildDEvOpen&#41;)

- [About](#about)
- [How to consume](#how-to-consume)
- [Contribute](#contribute)

## About
The axa-fr-ocr is an utility library built on top of Tesseract and providing algorithms to deskew text in order to enhance OCR performance. It also provides an algorithm to determine whether an image contains text.

## How to consume
```sh
pip install axa-fr-ocr
```


```python
import time
from io import BytesIO

import cv2
import numpy as np
import logging

from axa_fr_ocr.ocr import Ocr
from axa_fr_ocr.image import normalize_size
from axa_fr_ocr.text.deskew import deskew
from axa_fr_ocr.text.orientation import orientate
from axa_fr_ocr.text.text import is_image_contain_text


with open('.path.pdf', 'w') as stream:
    nparr = np.frombuffer(stream.read(), np.uint8)
    image_origin = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    image_cv, ratio_cv = normalize_size(image_origin, 2200)
    small_img_cv, ratio = normalize_size(image_cv, 800)
    is_img_with_text, distance, img_mser_cv = is_image_contain_text(small_img_cv)
    if not is_img_with_text:
      print("No text")
    else:
        img_straighted_cv, angle_orientation, duration_orientation = orientate(img_deskew_cv)
        img_straighted = BytesIO(cv2.imencode(".png", img_straighted_cv)[1].tobytes())
        ocr = Ocr(logging)
        img_text, ocr_confidence = ocr.process_ocr(img_straighted)
        print(img_text)
   

```

## Contribute

- [How to run the solution and to contribute](./CONTRIBUTING.md)
- [Please respect our code of conduct](./CODE_OF_CONDUCT.md)