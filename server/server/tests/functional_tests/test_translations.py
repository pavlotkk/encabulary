from server.database import db
from server.database.model import DbWord, DbTranslation
from server.tests.functional_tests.base import BaseAuthTestCase


class TranslationAddTestCase(BaseAuthTestCase):
    def setUp(self):
        super().setUp()

        self.id_word = None
        with self.app.app_context():
            db_word = DbWord(self.test_user_id, '__test__')
            db.session.add(db_word)
            db.session.commit()

            self.id_word = db_word.id_word

    def test_word_required(self):
        response = self._add_translation({})

        self.assertIsNotNone(response['error'])

    def test_translation_required(self):
        response = self._add_translation({
            'id_word': self.id_word
        })

        self.assertIsNotNone(response['error'])

    def test_word_does_not_exists(self):
        response = self._add_translation({
            'id_word': 0,
            'translation': '__translation__'
        })

        self.assertIsNotNone(response['error'])

    def test_success_add_translation(self):
        response = self._add_translation({
            'id_word': self.id_word,
            'translation': '__translation__'
        })

        self.assertIsNone(response['error'])
        translation_id = response['data'].get('id_translation')
        self.assertIsNotNone(translation_id)

        with self.app.app_context():
            db_tr = db.session.query(DbTranslation).get(translation_id)
            self.assertIsNotNone(db_tr)
            self.assertEqual(db_tr.translation, '__translation__')

    def _add_translation(self, params):
        return self.get_json_response('/api/translation', method='POST', params=params)
