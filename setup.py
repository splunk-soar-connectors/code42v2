import os

from setuptools import find_packages, setup

path_to_py42_wheel = os.path.join(os.getcwd(), 'wheels', 'py42-1.14.2-py2.py3-none-any.whl')

setup(
    name="phcode42v2",
    version="1.0.0",
    description="Code42 for Phantom",
    packages=find_packages(),
    install_requires=["requests>=2.3",
                      "pytest==4.4.0",
                      "pytest-mock==1.10.3",
                      f"py42 @ file://localhost/{path_to_py42_wheel}",
                      "phantomstubs"]
)
