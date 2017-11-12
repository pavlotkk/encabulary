from server.database import db
from server.database.model import DbWord, DbUserWordRepeat
from server.database.model.translation_direction import TranslationDirection
from server.tests.functional_tests.base_learn import BaseRepeatTestCase


class TestRepeatUserLanguageDirectionWords(BaseRepeatTestCase):
    def test_repeat_user_language_direction_with_invalid_answer(self):
        data = {
            'direction': TranslationDirection.USER_LANGUAGE,
            'answers': [{'id_word': self.id_word, 'answer': 'bla-bla-bla'}]
        }

        response = self._api_send_user_answers(data)
        self.assertIsNone(response['error'])
        self.assertIsNotNone(response['data'].get('result'))
        result = response['data']['result']
        self.assertEqual(result['ok_count'], 0)
        self.assertEqual(result['mistakes_count'], 1)
        self.assertEqual(len(result['mistakes']), 1)
        mistake = result['mistakes'][0]
        self.assertEqual(mistake['answer'], 'bla-bla-bla')
        self.assertTrue('__translation_1__' in mistake['correct'])
        self.assertTrue('__translation_2__' in mistake['correct'])

        with self.app.app_context():
            db_word = db.session.query(DbWord).get(self.id_word)
            self.assertEqual(db_word.score, self.words_learned_score - 1)
            self.assertEqual(db_word.is_learnt, False)

            db_repeat = db.session.query(
                DbUserWordRepeat
            ).filter(
                DbUserWordRepeat.id_word == self.id_word
            ).first()

            self.assertIsNone(db_repeat)

    def test_repeat_user_language_direction_with_valid_answer(self):
        previous_repeat_id = None
        with self.app.app_context():
            previous_repeat_id = db.session.query(
                DbUserWordRepeat.id_repeat
            ).filter(
                DbUserWordRepeat.id_word == self.id_word
            ).scalar()

        data = {
            'direction': TranslationDirection.USER_LANGUAGE,
            'answers': [{'id_word': self.id_word, 'answer': '__translation_1__'}]
        }

        response = self._api_send_user_answers(data)
        self.assertIsNone(response['error'])
        self.assertIsNotNone(response['data'].get('result'))
        result = response['data']['result']
        self.assertEqual(result['ok_count'], 1)
        self.assertEqual(result['mistakes_count'], 0)
        self.assertEqual(len(result['mistakes']), 0)

        with self.app.app_context():
            db_word = db.session.query(DbWord).get(self.id_word)
            self.assertEqual(db_word.score, self.words_learned_score)

            db_repeat = db.session.query(
                DbUserWordRepeat
            ).filter(
                DbUserWordRepeat.id_word == self.id_word
            ).first()

            self.assertNotEqual(db_repeat.id_repeat, previous_repeat_id)
