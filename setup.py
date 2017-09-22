#!/usr/bin/env python3

"""
Setup declaration to install Pyckup
"""

params = dict(
    name='Pyckup',
    version='0.1.0',
    packages=['pyckup', 'pyckup.syncers'],
    url='https://github.com/BenjaminSchubert/Pyckup',
    download_url="https://github.com/BenjaminSchubert/Pyckup/tar.gz/0.1",
    license='MIT',
    author='Benjamin Schubert',
    author_email='ben.c.schubert@gmail.com',
    description='A backup utility based on rsync',

    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: Unix",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],

)

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

else:
    params['scripts'] = ["bin/pyckup"]

setup(**params)