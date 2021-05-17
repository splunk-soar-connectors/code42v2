from setuptools import find_packages, setup

setup(
    name="phcode42v2",
    version="1.0.0",
    description="Code42 for Phantom",
    packages=find_packages(),
    install_requires=["requests>=2.3",
                      "pytest==4.4.0",
                      "pytest-mock==1.10.3",
                      "py42>=1.14.1",
                      "phantomstubs"]
)
