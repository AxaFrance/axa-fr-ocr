import setuptools
from version import VERSION

print(f"version =============== {VERSION}")

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name="axa-fr-ocr",
    version=VERSION,
    packages=["axa_fr_ocr", "axa_fr_ocr.text"],
    package_dir={"": "src"},
    package_data={"axa_fr_ocr.text": ["*"]},
    install_requires=requirements,
    author="AXA",
    author_email="guillaume.chervet@axa.fr",
    url="https://github.com/AxaFrance/axa-fr-ocr",
    description="AXA France OCR library",
    long_description="Utility library built on top of Tesseract and providing "
                     "algorithms to deskew text in order to enhance OCR "
                     "performance. It also provides an algorithm to determine "
                     "whether an image contains text.",
    platforms="POSIX",
    classifiers=["Programming Language :: Python :: 3 :: Only",
                 "Programming Language :: Python :: 3.8",
                 "Topic :: Scientific/Engineering :: Information Analysis",
                 ],
    include_package_data=True,
    python_requires=">=3.8",
)
