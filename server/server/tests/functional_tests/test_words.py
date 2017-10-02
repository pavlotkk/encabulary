from server.database.model import DbWord
from server.tests.functional_tests.base import BaseAuthTestCase
from server.database import db


class TestAddWord(BaseAuthTestCase):

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
        return self.get_json_response('/api/word', method='POST', params=params)


class TestUpdateWord(BaseAuthTestCase):

    def setUp(self):
        super().setUp()

        self.id_word = None
        with self.app.app_context():
            db_word = DbWord(self.test_user_id, '__test__')
            db.session.add(db_word)
            db.session.commit()

            self.id_word = db_word.id_word

    def test_word_requirement(self):
        response = self.update_word(self.id_word, {})

        self.assertIsNotNone(response['error'])

    def test_word_does_not_exists(self):
        response = self.update_word(0, {'word': 'aaa'})

        self.assertIsNotNone(response['error'])

    def test_success_update_word(self):
        word = '__updated'
        response = self.update_word(self.id_word, {'word': word})

        self.assertIsNone(response['error'])

        with self.app.app_context():
            db_word = db.session.query(DbWord).get(self.id_word)
            self.assertIsNotNone(db_word)
            self.assertEqual(db_word.word, word)

    def update_word(self, id_word, params):
        return self.get_json_response('/api/word/{}'.format(id_word), method='PUT', params=params)
