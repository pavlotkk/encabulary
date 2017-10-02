from server.database.model import DbWord
from server.tests.functional_tests.base import BaseAuthTestCase
from server.database import db


class TestAddToDictionary(BaseAuthTestCase):

    def test_word_requirement(self):
        response = self.add_word(params={})

        self.assertIsNotNone(response['error'])
        self.assertEqual(response['error'], 'word is required')

    def test_success_add_word(self):
        response = self.add_word(params={
            'word': 'hello'
        })

        self.assertIsNone(response['error'])
        self.assertIsNotNone(response['data']['id_word'])

        id_word = response['data']['id_word']

        with self.app.app_context():
            db_word = db.session.query(DbWord).get(id_word)
            self.assertIsNotNone(db_word)

    def add_word(self, params):
        return self.get_json_response('/api/words', method='POST', params=params)
