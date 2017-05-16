import responses

from gitlab.exceptions import HttpError
from gitlab_tests.base import BaseTest
from response_data.tags import *


class TestDeleteRepositoryTag(BaseTest):
    def setUp(self):
        super(TestDeleteRepositoryTag, self).setUp()
        self.gitlab.login(user=self.user, password=self.password)

    @responses.activate
    def test_delete_repository_tag(self):
        responses.add(
            responses.DELETE,
            self.gitlab.api_url + '/projects/5/repository/tags/test',
            json=delete_repository_tag,
            status=200,
            content_type='application/json')

        self.assertEqual(delete_repository_tag, self.gitlab.delete_repository_tag(5, 'test'))

    @responses.activate
    def test_delete_repository_tag_exception(self):
        responses.add(
            responses.DELETE,
            self.gitlab.api_url + '/projects/5/repository/tags/test',
            json='{"message":"No such tag"}',
            status=404,
            content_type='application/json')

        self.assertRaises(HttpError, self.gitlab.delete_repository_tag, 5, 'test')
