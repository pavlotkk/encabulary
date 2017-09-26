from server.tests.functional_tests.base import BaseTestCase


class TestLogin(BaseTestCase):
    def test_bad_login(self):
        login_response = self.get_json_response('/api/login', {'email': 'unknown@domain.com', 'password': '123'})
        self.assertFalse(login_response['error'] is None)

    def test_success_login(self):
        login_response = self.get_json_response('/api/login', {'email': 'test-user@domain.com', 'password': '123'})
        self.assertTrue(login_response['data']['access_token'] is not None)
