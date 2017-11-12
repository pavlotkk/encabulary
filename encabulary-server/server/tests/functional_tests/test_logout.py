from server.tests.functional_tests.base import BaseTestCase


class TestLogout(BaseTestCase):

    def test_un_authorized_logout(self):
        logout_response = self.get_logout_response()
        self.assertTrue(logout_response['error'] is not None)

    def test_authorized_logout(self):
        self.get_login_response()

        logout_response = self.get_logout_response()
        self.assertTrue(logout_response['error'] is None)

    def get_logout_response(self):
        return self.get_json_response('/api/logout')
