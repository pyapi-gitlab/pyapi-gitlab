from integration_tests.base import BaseTest, log_to_term


class TestGitlabV91(BaseTest):
    def test_add_remove_user(self):
        """Add and remove a user"""
        response = self.gitlab.edituser(1, password='1WmA1a3ONs9F')
        log_to_term('update_password:', response)
        self.assertTrue(response)

        response = self.gitlab.createuser(
            'test', 'test', 'TestPassword1', 'test@example.com')
        log_to_term('create_user', response)

        response = self.gitlab.delete_user(response['id'])
        log_to_term('delete_user', response)
        self.assertTrue(isinstance(response, dict))
        self.assertEqual({}, response)
