import os

from setuptools import find_packages, setup

setup(
    name="stubs",
    version="1.0.0",
    description="Phantom Stubs for Code42 for Phantom",
    packages=find_packages(),
    install_requires=["requests>=2.3"]
)
