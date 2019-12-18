import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="aiorequests", # Replace with your own username
    version="0.0.1",
    author="Slime",
    author_email="selim.lanouar@gmail.com",
    description="Requests lib wrapper to make asynchronus requests and provide useful requests",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/WhatTheSlime/aiorequests",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
