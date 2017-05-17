import responses

from gitlab.exceptions import HttpError
from gitlab_tests.base import BaseTest
from response_data.projects import *


class TestDeleteProject(BaseTest):
    @responses.activate
    def test_delete_project_true(self):
        responses.add(
            responses.DELETE,
            self.gitlab.api_url + '/projects/1',
            json=True,
            status=200,
            content_type='application/json')

        self.assertEqual({}, self.gitlab.delete_project(1))
        self.assertEqual(True, self.gitlab.deleteproject(1))

    @responses.activate
    def test_delete_project_json(self):
        responses.add(
            responses.DELETE,
            self.gitlab.api_url + '/projects/1',
            json={},
            status=200,
            content_type='application/json')

        self.assertEqual({}, self.gitlab.delete_project(1))
        self.assertEqual(True, self.gitlab.deleteproject(1))

    @responses.activate
    def test_delete_project_exception(self):
        responses.add(
            responses.DELETE,
            self.gitlab.api_url + '/projects/1',
            json=delete_project,
            status=404,
            content_type='application/json')

        self.assertRaises(HttpError, self.gitlab.delete_project, 1)
        self.assertEqual(True, self.gitlab.deleteproject(1))


class TestGetProject(BaseTest):
    @responses.activate
    def test_delete_project_true(self):
        responses.add(
            responses.GET,
            self.gitlab.api_url + '/projects/1',
            json=get_project,
            status=200,
            content_type='application/json')

        self.assertEqual(get_project, self.gitlab.get_project(1))
        self.assertEqual(get_project, self.gitlab.getproject(1))

    @responses.activate
    def test_delete_project_json(self):
        responses.add(
            responses.GET,
            self.gitlab.api_url + '/projects/1',
            body='{"error": "Not found"}',
            status=404,
            content_type='application/json')

        self.assertRaises(HttpError, self.gitlab.get_project, 1)
        self.assertFalse(self.gitlab.getproject(1))
