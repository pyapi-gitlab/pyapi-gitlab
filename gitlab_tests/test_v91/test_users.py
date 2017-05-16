import responses

from gitlab.exceptions import HttpError
from gitlab_tests.base import BaseTest
from response_data.users import *


class TestGetUsers(BaseTest):
    @responses.activate
    def test_get_users(self):
        responses.add(
            responses.GET,
            self.gitlab.api_url + '/users',
            match_querystring=False,
            json=get_users,
            status=200,
            content_type='application/json')

        self.assertEqual(get_users, self.gitlab.get_users())
        self.assertEqual(get_users, self.gitlab.get_users(search='test'))
        self.assertEqual(get_users, self.gitlab.getusers())

    @responses.activate
    def test_get_users_exception(self):
        responses.add(
            responses.GET,
            self.gitlab.api_url + '/users',
            match_querystring=False,
            json='{"error": "Not found"}',
            status=404,
            content_type='application/json')

        self.assertRaises(HttpError, self.gitlab.get_users)
        self.assertEqual(False, self.gitlab.getusers())
