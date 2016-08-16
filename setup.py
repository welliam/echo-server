# -*- coding: utf-8 -*-
"""Package for implementing a echo server"""
from setuptools import setup

setup(
    name="echo-server",
    description="Package for implementing a echo server",
    version="0.1.0",
    author="Steven Than, Justin Lange",
    author_email="steventhan@gmail.com, well1912@gmail.com",
    license="MIT",
    py_modules=["echo_server"],
    package_dir={'': 'src'},
    install_requires=[],
    extras_require={'test': ['pytest', 'pytest-watch', 'tox']},
)
