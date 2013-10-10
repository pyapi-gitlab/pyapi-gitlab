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
    description = "Gitlab API wrapper for Gitlab 6.X",
    license = "GPL3",
    keywords = "gitlab git wrapper",
    url = "http://github.com/itxaka/pyapi-gitlab/",
)
