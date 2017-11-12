from server.database.model import DbWord, DbTranslation
from server.tests.functional_tests.base import BaseAuthTestCase
from server.database import db


class TestAddWord(BaseAuthTestCase):

    def test_word_requirement(self):
        response = self._api_add_word(params={})
        self.assertIsNotNone(response['error'])

    def test_word_type_requirement(self):
        response = self._api_add_word(params={'word': 'bla-bla-bla'})
        self.assertIsNotNone(response['error'])

    def test_success_add_word(self):
        response = self._api_add_word(params={
            'word': 'hello',
            'id_type': 1
        })

        self.assertIsNone(response['error'])
        self.assertIsNotNone(response['data']['id_word'])

        id_word = response['data']['id_word']

        with self.app.app_context():
            db_word = db.session.query(DbWord).get(id_word)
            self.assertIsNotNone(db_word)

    def test_success_add_word_with_translations(self):
        response = self._api_add_word(params={
            'word': 'hello',
            'id_type': 1,
            'translations': ['привет', 'здравствуй']
        })

        self.assertIsNone(response['error'])
        self.assertIsNotNone(response['data']['id_word'])

        id_word = response['data']['id_word']

        with self.app.app_context():
            db_word = db.session.query(DbWord).get(id_word)
            self.assertIsNotNone(db_word)
            db_translations = db.session.query(DbTranslation).filter(DbTranslation.id_word == id_word).all()
            for tr in ['привет', 'здравствуй']:
                self.assertTrue(any([i for i in db_translations if i.translation == tr]))

    def _api_add_word(self, params):
        return self.get_json_response('/api/word', method='POST', params=params)


class BaseWordTestCase(BaseAuthTestCase):
    def setUp(self):
        super().setUp()

        self.id_word = None
        with self.app.app_context():
            db_word = DbWord(self.test_user_id, '__test__', 1)
            db.session.add(db_word)
            db.session.commit()

            self.id_word = db_word.id_word


class TestUpdateWord(BaseWordTestCase):

    def test_word_requirement(self):
        response = self._api_update_word(self.id_word, {})

        self.assertIsNotNone(response['error'])

    def test_word_type_requirement(self):
        response = self._api_update_word(self.id_word, {'word': 'bla-bla'})

        self.assertIsNotNone(response['error'])

    def test_word_does_not_exists(self):
        response = self._api_update_word(0, {'word': 'aaa', 'id_type': 1})

        self.assertIsNotNone(response['error'])

    def test_success_update_word(self):
        word = '__updated'
        response = self._api_update_word(self.id_word, {'word': word, 'id_type': 2})

        self.assertIsNone(response['error'])

        with self.app.app_context():
            db_word = db.session.query(DbWord).get(self.id_word)
            self.assertIsNotNone(db_word)
            self.assertEqual(db_word.word, word)
            self.assertEqual(db_word.id_word_type, 2)

    def _api_update_word(self, id_word, params):
        return self.get_json_response('/api/word/{}'.format(id_word), method='PUT', params=params)


class TestGetWord(BaseWordTestCase):

    def test_word_does_not_exists(self):
        response = self._api_get_word(0)

        self.assertIsNotNone(response['error'])

    def test_success_get_word(self):
        response = self._api_get_word(self.id_word)

        self.assertIsNotNone(response['data']['word'])

    def _api_get_word(self, id_word):
        return self.get_json_response('/api/word/{}'.format(id_word), method='GET')


class TestDeleteWord(BaseWordTestCase):

    def test_word_does_not_exists(self):
        response = self._api_delete_word(0)

        self.assertIsNotNone(response['error'])

    def test_success_delete_word(self):
        response = self._api_delete_word(self.id_word)

        self.assertIsNone(response['error'])

    def _api_delete_word(self, id_word):
        return self.get_json_response('/api/word/{}'.format(id_word), method='DELETE')
