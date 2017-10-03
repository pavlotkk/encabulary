from server.database import db
from server.database.model import DbWord, DbTranslation, DbLanguage
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


class TranslationGetTestCase(BaseAuthTestCase):
    def setUp(self):
        super().setUp()

        self.id_translation = None
        with self.app.app_context():
            db_word = DbWord(self.test_user_id, '__test__')
            db.session.add(db_word)
            db.session.flush()

            db_tr = DbTranslation(db_word.id_word, DbLanguage.RU, 1, '__translation__')
            db.session.add(db_tr)

            db.session.commit()

            self.id_translation = db_tr.id_translation

    def test_get_translation_with_error(self):
        response = self._get_translation(0)

        self.assertIsNotNone(response['error'])

    def test_get_translation(self):
        response = self._get_translation(self.id_translation)

        self.assertIsNone(response['error'])
        self.assertIsNotNone(response['data'].get('translation'))

    def _get_translation(self, id_translation):
        return self.get_json_response('/api/translation/{}'.format(id_translation), method='GET', params={})


class TranslationUpdateTestCase(BaseAuthTestCase):
    def setUp(self):
        super().setUp()

        self.id_translation = None
        with self.app.app_context():
            db_word = DbWord(self.test_user_id, '__test__')
            db.session.add(db_word)
            db.session.flush()

            db_tr = DbTranslation(db_word.id_word, DbLanguage.RU, 1, '__translation__')
            db.session.add(db_tr)

            db.session.commit()

            self.id_translation = db_tr.id_translation

    def test_update_translation_required(self):
        response = self._update_translation(self.id_translation, {})

        self.assertIsNotNone(response['error'])

    def test_update_translation(self):
        response = self._update_translation(self.id_translation, {'translation': '__edit_translation__'})

        self.assertIsNone(response['error'])
        with self.app.app_context():
            db_tr = db.session.query(DbTranslation).get(self.id_translation)
            self.assertIsNotNone(db_tr)
            self.assertEqual(db_tr.translation, '__edit_translation__')

    def _update_translation(self, id_translation, params):
        return self.get_json_response('/api/translation/{}'.format(id_translation), method='PUT', params=params)
