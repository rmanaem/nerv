from setuptools import find_packages, setup

with open("CHANGELOG.md", "r") as file:
    changelog = file.readlines()[9:20]

with open("README.md", "r") as file:
    readme = file.read()


with open("requirements.txt", "r") as file:
    install_requires = file.read().split("\n")

VERSION = "0.2.5"
DESCRIPTION = "Neuroimaging Results Visualization"
LONG_DESCRIPTION = f"## What's new in {VERSION}\n\n{''.join(changelog)}\n\n{readme}"

setup(
    name="nerv",
    version=VERSION,
    author="rmanaem",
    author_email="<rmanaem@protonmail.ch>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    url="https://github.com/rmanaem/nerv",
    packages=find_packages(),
    include_package_data=True,
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
