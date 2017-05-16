import os
import unittest

from gitlab import Gitlab


class BaseTest(unittest.TestCase):
    def setUp(self):
        self.user = os.environ.get('gitlab_user', 'root')
        self.password = os.environ.get('gitlab_password', '5iveL!fe')
        self.host = os.environ.get('gitlab_host', 'http://localhost:10080')
        self.gitlab = Gitlab(host=self.host, verify_ssl=False)
        self.gitlab.host = self.host
