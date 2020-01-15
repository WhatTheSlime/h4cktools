from setuptools import setup

setup(
    name='rqhelper-whattheslime',
    version='0.0.1',
    description='Requests lib wrapper',
    url='git@github.com:WhatTheSlime/rqhelper.git',
    author='Sélim Lanouar',
    author_email='selim.lanouar@gmail.com',
    license='unlicense',
    packages=['rqhelper'],
    python_requires=">=3.6",
	install_requires=[
		'requests',
		'asyncio',
        'bs4',
	],
	zip_safe=False
)

