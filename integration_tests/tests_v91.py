import os
import logging
from unittest import TestCase

from gitlab import Gitlab


logger = logging.getLogger(__name__)


def log_to_term(var_name, response):
    print('\r{}: {}\r'.format(var_name, response))


class TestGitlabV91(TestCase):
    def setUp(self):
        self.user = os.environ.get('gitlab_user', 'root')
        self.password = os.environ.get('gitlab_password', '5iveL!fe')
        self.host = os.environ.get('gitlab_host', 'http://localhost:10080')
        self.gitlab = Gitlab(host=self.host, verify_ssl=False)
        self.gitlab.login(user=self.user, password=self.password)

    def test_gitlab_v91(self):
        create_user = self.gitlab.createuser(
            'test', 'test', 'TestPassword1', 'test@example.com')
        log_to_term('create_user', create_user)

        delete_user = self.gitlab.deleteuser(create_user['id'])
        log_to_term('delete_user', delete_user)
