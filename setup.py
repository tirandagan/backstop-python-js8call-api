from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="backstop-python-js8call-api",
    version="0.1.0",
    author="Tiran Dagan",
    author_email="tiran@backstopbeta.com",
    description="A Python library for interacting with JS8Call's TCP API, featuring GPS integration and automated grid square management.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tirandagan/backstop-python-js8call-api",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Communications :: Ham Radio",
    ],
    python_requires=">=3.6",
    install_requires=[
        "gpsd-py3==0.3.0",
    ],
    license="MIT",
) 