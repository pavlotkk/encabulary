from server.database import db
from server.database.model import DbWord, DbTranslation, DbLanguage
from server.tests.functional_tests.base import BaseAuthTestCase


class BaseLearnTestCase(BaseAuthTestCase):
    def setUp(self):
        super().setUp()

        self.id_word = None
        self.db_translations = []
        with self.app.app_context():
            db_word = DbWord(self.test_user_id, '__test__')
            db.session.add(db_word)
            db.session.flush()

            db_tr_1 = DbTranslation(db_word.id_word, DbLanguage.RU, 1, '__translation_1__')
            db_tr_2 = DbTranslation(db_word.id_word, DbLanguage.RU, 2, '__translation_2__')
            db.session.add(db_tr_1)
            db.session.add(db_tr_2)
            db.session.flush()

            db.session.commit()

            self.id_word = db_word.id_word
            self.db_translations = [db_tr_1.translation, db_tr_2.translation]


class TestLearnWord(BaseLearnTestCase):

    def test_learn(self):
        response = self._learn_words()

        self.assertIsNone(response['error'])
        self.assertIsNotNone(response['data'].get('learn'))
        self.assertEqual(len(response['data']['learn']), 1)

        data_learn = response['data']['learn'][0]
        self.assertEqual(data_learn['id_word'], self.id_word)
        data_translations = data_learn['translations']

        for tr in self.db_translations:
            self.assertTrue(any([item for item in data_translations if item['translation'] == tr]))

    def _learn_words(self):
        return self.get_json_response('/api/learn', method='GET', params={})
