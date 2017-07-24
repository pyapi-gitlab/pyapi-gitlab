import os
import logging
from unittest import TestCase

from gitlab import Gitlab


def log_to_term(var_name, response):
    print('\r\r', var_name, ':', response, '\r\r')


class BaseTest(TestCase):
    def setUp(self):
        self.user = os.environ.get('gitlab_user', 'root')
        self.password = os.environ.get('gitlab_password', '5iveL!fe')
        self.host = os.environ.get('gitlab_host', 'http://gitlab:20')

        self.gitlab = Gitlab(host=self.host, verify_ssl=False)

        self.gitlab.login(user=self.user, password=self.password)
