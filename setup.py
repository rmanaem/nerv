import codecs
import os

from setuptools import find_packages, setup

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as file:
    long_description = "\n" + file.read()

with open("requirements.txt", "r") as file:
    install_requires = file.read().split("\n")

VERSION = "0.1.1"
DESCRIPTION = "Neuroimaging Results Visualization"
LONG_DESCRIPTION = long_description

setup(
    name="nerv",
    version=VERSION,
    author="rmanaem",
    author_email="<rmanaem@protonmail.ch>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    url="https://github.com/rmanaem/nerv",
    packages=find_packages(),
    include_package_data=True,
    package_data={"nerv": ["assets/*"]},
    install_requires=install_requires,
    license="MIT",
    keywords=[
        "python",
        "dash",
        "pandas",
        "data visualization",
        "plotly",
        "neuroscience",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "License :: OSI Approved :: MIT License",
    ],
)
