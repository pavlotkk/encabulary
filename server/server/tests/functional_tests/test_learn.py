from server.tests.functional_tests.base import BaseAuthTestCase


class TestLearnWord(BaseAuthTestCase):

    def test_learn(self):
        response = self._learn_words()

        self.print_json(response)
        self.assertIsNone(response['error'])

    def _learn_words(self):
        return self.get_json_response('/api/learn', method='GET', params={})
