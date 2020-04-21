#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()


requirements = [
    "shapely==1.7.0",
    "geojson==2.5.0",
    "requests==2.23.0",
    "retry",
    "pyproj",
    "pandas",
]

setup(
    author="Joao Carabetta",
    author_email="joao.carabetta@gmail.com",
    python_requires=">=3",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
    ],
    description="Calculate Open Street Maps road length for any polygon",
    entry_points={},
    install_requires=requirements,
    license="MIT license",
    long_description=readme + "\n\n" + history,
    include_package_data=True,
    name="osm-road-length",
    packages=find_packages(include=["osm_road_length", "osm_road_length.*"]),
    test_suite="tests",
    url="https://github.com/JoaoCarabetta/osm-road-length",
    version="0.1.4",
    zip_safe=False,
)
