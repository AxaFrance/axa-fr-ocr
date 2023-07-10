import setuptools
import version

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name="ocr",
    version=version.VERSION,
    packages=["ocr", "ocr.text"],
    package_dir={"": "src"},
    package_data={"ocr.text": ["*"]},
    install_requires=requirements,
    author="AXA",
    include_package_data=True,
    python_requires=">=3.8",
)
