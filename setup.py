# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
setup(
    name = "pyapi-gitlab",
    version = "7.8.5",
    packages = find_packages(),
    install_requires = ['requests'],
    extras_require = {
        'markdown':  ["markdown"]
    },
    # metadata for upload to PyPI
    author = "Itxaka Serrano Garcia",
    author_email = "itxakaserrano@gmail.com",
    description = "Gitlab API wrapper for Gitlab 7.X",
    license = "Apache License 2.0",
    keywords = "gitlab git wrapper",
    url = "http://github.com/itxaka/pyapi-gitlab/",
    test_suite="gitlab_tests",
)
