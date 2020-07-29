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
        "requests",
        "asyncio",
        "bs4",
        "lxml",
        "jwt",
    ],
)

