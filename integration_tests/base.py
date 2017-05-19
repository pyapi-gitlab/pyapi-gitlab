import os
import logging
from unittest import TestCase

from gitlab import Gitlab


def log_to_term(var_name, response):
    print('\r\r{}: {}\r\r'.format(var_name, response))


class BaseTest(TestCase):
    def setUp(self):
        self.user = os.environ.get('gitlab_user', 'root')
        self.password = os.environ.get('gitlab_password', '1WmA1a3ONs9F')
        self.host = os.environ.get('gitlab_host', 'http://localhost:10080')
        self.gitlab = Gitlab(host=self.host, verify_ssl=False)

        self.gitlab.login(user=self.user, password=self.password)