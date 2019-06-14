# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open("README.md") as f:
    readme = f.read()


setup(
    name="item-catalog",
    version="0.1.0",
    py_modules=["flaskapp"],
    description="Item cataloging engine",
    long_description=readme,
    author="Łukasz Hen",
    author_email="lukasz.hen@gmail.com",
    url="https://github.com/lukhen/item-catalog",
    packages=find_packages(exclude=("tests", "docs")),
)
