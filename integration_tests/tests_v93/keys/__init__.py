from requests.exceptions import HTTPError

from integration_tests.base import BaseTest
from response_data.keys import get_keys


class TestKeys(BaseTest):
    def test_get(self):
        self.assertEqual(
            get_keys.keys(),
            self.gitlab.keys(1).keys())

        self.assertRaises(
            HTTPError,
            self.gitlab.keys, 100
        )
