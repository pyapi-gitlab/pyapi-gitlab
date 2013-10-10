# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
setup(
    name = "pyapi-gitlab",
    version = "6.1-2",
    packages = find_packages(),
    install_requires = ['requests', 'markdown'],
    # metadata for upload to PyPI
    author = "Itxaka Serrano Garcia",
    author_email = "itxakaserrano@gmail.com",
    description = "See the README.md file for more information",
    license = "GPL3",
    keywords = "gitlab git wrapper",
    url = "http://github.com/itxaka/pyapi-gitlab/",
)
