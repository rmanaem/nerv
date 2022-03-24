from setuptools import setup, find_packages
import codecs
import os
try:  # for pip >= 10
    from pip._internal.req import parse_requirements
except ImportError:  # for pip <= 9.0.3
    from pip.req import parse_requirements

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as file:
    long_description = "\n" + file.read()

with open('requirements.txt', 'r') as file:
    install_requires = file.read().split('\n')

VERSION = '0.0.1'
DESCRIPTION = 'Neuroimaging Results Visualization'
LONG_DESCRIPTION = long_description

setup(
    name="nerv",
    version=VERSION,
    author="(rmanaem) Arman Jahanpour",
    author_email="<armanjahanpour7@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    url="https://github.com/rmanaem/nerv",
    packages=find_packages(),
    install_requires=install_requires,
    license="MIT",
    keywords=['python', 'dash', 'pandas', 'data visualization'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
