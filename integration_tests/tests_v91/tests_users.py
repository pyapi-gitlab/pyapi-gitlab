from integration_tests.base import BaseTest, log_to_term


class TestGitlabV91(BaseTest):
    def test_add_remove_user(self):
        """Add and remove a user"""
        response = self.gitlab.login(user=self.user, password=self.password)
        log_to_term('login:', response)
        self.assertTrue(isinstance(response, dict))

        response = self.gitlab.createuser(
            'test', 'test', 'TestPassword1', 'test@example.com')
        log_to_term('create_user', response)

        response = self.gitlab.delete_user(response['id'])
        log_to_term('delete_user', response)
        self.assertTrue(isinstance(response, dict))
        self.assertEqual({}, response)
