import unittest
import os

from gitlab import Gitlab
from gitlab.exceptions import HttpError


class BaseTest(unittest.TestCase):
    def setUp(self):
        self.user = os.environ.get('gitlab_user', 'root')
        self.password = os.environ.get('gitlab_password', '5iveL!fe')
        self.host = os.environ.get('gitlab_host', 'http://localhost:10080')
        self.gitlab = Gitlab(host=self.host, verify_ssl=False)
        self.gitlab.host = self.host


class TestLogin(BaseTest):
    def test_login(self):
        self.assertTrue(self.gitlab.login(user=self.user, password=self.password))

    def test_login_email(self):
        self.assertRaises(
            HttpError, self.gitlab.login, email='test@test.com', password='test')

    def test_login_with_no_values(self):
        self.assertRaises(ValueError, self.gitlab.login)
