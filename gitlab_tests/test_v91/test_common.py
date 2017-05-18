from unittest import mock

import responses

from gitlab.exceptions import HttpError
from gitlab_tests.base import BaseTest
from response_data.users import *


class TestSuccessOrRaise(BaseTest):
    def test_success_or_raise_without_error(self):
        response = mock.MagicMock()
        response_config = {
            'status_code': 200,
            'json.return_value': post_users_error
        }
        response.configure_mock(**response_config)

        self.gitlab.success_or_raise(response, [200])

    def test_success_or_raise_with_error(self):
        response = mock.MagicMock()
        response_config = {
            'status_code': 404,
            'text': post_users_error
        }
        response.configure_mock(**response_config)

        self.assertRaises(HttpError, self.gitlab.success_or_raise, response, [200])


class TestLogin(BaseTest):
    def test_login(self):
        self.assertTrue(self.gitlab.login(user=self.user, password=self.password))

    def test_login_email(self):
        self.assertRaises(
            HttpError, self.gitlab.login, email='test@test.com', password='test')

    def test_login_with_no_values(self):
        self.assertRaises(ValueError, self.gitlab.login)


class TestGet(BaseTest):
    @responses.activate
    def test_get_with_200(self):
        responses.add(
            responses.GET,
            self.gitlab.api_url + '/users',
            json=get_users,
            status=200,
            content_type='application/json')

        self.assertEqual(get_users, self.gitlab.get('/users'))
        self.assertEqual(get_users, self.gitlab.get('/users', default_response={}))

    @responses.activate
    def test_get_with_404(self):
        responses.add(
            responses.GET,
            self.gitlab.api_url + '/users',
            body='{"error": "Not here"}',
            status=404,
            content_type='application/json')

        self.assertRaises(HttpError, self.gitlab.get, '/users')


class TestPost(BaseTest):
    @responses.activate
    def test_post_with_201(self):
        responses.add(
            responses.POST,
            self.gitlab.api_url + '/users',
            json=post_users,
            status=201,
            content_type='application/json')
        data = {
            'name': 'test',
            'username': 'test1',
            'password': 'MyTestPassword1',
            'email': 'example@example.com'
        }

        self.assertEqual(post_users, self.gitlab.post('/users', **data))
        self.assertEqual(post_users, self.gitlab.post('/users', default_response={}, **data))

    @responses.activate
    def test_get_with_404(self):
        responses.add(
            responses.POST,
            self.gitlab.api_url + '/users',
            body=post_users_error,
            status=409,
            content_type='application/json')
        data = {
            'name': 'test',
            'username': 'test1',
            'password': 'MyTestPassword1',
            'email': 'example@example.com'
        }

        self.assertRaises(HttpError, self.gitlab.post, '/users', **data)


class TestDelete(BaseTest):
    @responses.activate
    def test_delete(self):
        responses.add(
            responses.DELETE,
            self.gitlab.api_url + '/users/5',
            json=None,
            status=204,
            content_type='application/json')

        self.assertEqual({}, self.gitlab.delete('/users/5'))
        self.assertEqual({}, self.gitlab.delete('/users/5', default_response={}))

    @responses.activate
    def test_delete_404(self):
        responses.add(
            responses.POST,
            self.gitlab.api_url + '/users',
            body=post_users_error,
            status=409,
            content_type='application/json')

        self.assertRaises(HttpError, self.gitlab.post, '/users')


class TestFormatString(BaseTest):
    def test__format_string(self):
        self.assertEqual('foo%2Fbar', self.gitlab._format_string('foo/bar'))
        self.assertEqual(1, self.gitlab._format_string(1))
