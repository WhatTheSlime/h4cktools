from setuptools import setup

setup(
    name="h4cktools-whattheslime",
    version="0.1",
    description="Requests lib wrapper",
    url="https://github.com/WhatTheSlime/h4cktools",
    author="Sélim Lanouar",
    author_email="selim.lanouar@gmail.com",
    license="unlicense",
    packages=["h4cktools"],
    python_requires=">=3.6",
    install_requires=[
        "pytest==6.1.2",
        "urllib3==1.25.9",
        "requests_mock==1.8.0",
        "lxml==4.5.2",
        "requests==2.23.0",
        "beautifulsoup4==4.9.3",
        "progressbar33==2.4",
    ],
)

