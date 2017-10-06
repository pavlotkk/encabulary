from server.database.model import DbWordType
from server.tests.functional_tests.base import BaseTestCase


class TestAutoComplete(BaseTestCase):

    def test_autocomplete_word_noun(self):
        response = self._api_autocomplete('malfunction', DbWordType.NOUN)

        self.assertIsNone(response['error'])
        self.assertIsNotNone(response['data'].get('word'))

        data_word = response['data']['word']
        self.assertEqual(data_word['id_word_type'], DbWordType.NOUN)
        self.assertTrue(len(data_word['translations']) > 0)

    def test_autocomplete_word_verb(self):
        response = self._api_autocomplete('malfunction', DbWordType.VERB)

        self.assertIsNone(response['error'])
        self.assertIsNotNone(response['data'].get('word'))

        data_word = response['data']['word']
        self.assertEqual(data_word['id_word_type'], DbWordType.VERB)
        self.assertTrue(len(data_word['translations']) > 0)

    def _api_autocomplete(self, word, id_word_type=None):
        if not id_word_type:
            return self.get_json_response('/api/autocomplete/{}'.format(word), method='GET')

        return self.get_json_response('/api/autocomplete/{}/{}'.format(word, id_word_type), method='GET')