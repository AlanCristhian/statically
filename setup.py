"""Installation script."""

from setuptools import setup
from sys import version_info

assert version_info >= (3, 6), \
"Python 3.6+ is required. Got %s.%s" % (version_info.major, version_info.minor)

setup(
    name="statically",
    version="1.0a1",
    py_modules=["statically"],
    zip_safe=True,
    author="Alan Cristhian",
    author_email="alan.cristh@gmail.com",
    description="Compiles a python function with cython using only a decorator.",
    license="MIT",
    keywords="cython decorator compilation",
    url="https://github.com/AlanCristhian/statically",
    install_requires=["cython"],
)
