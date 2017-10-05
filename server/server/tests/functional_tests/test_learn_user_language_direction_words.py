from server.database import db
from server.database.model import DbWord, DbUserWordRepeat
from server.database.model.translation_direction import TranslationDirection
from server.tests.functional_tests.base_learn import BaseLearnTestCase


class TestLearningUserLanguageDirectionWords(BaseLearnTestCase):
    def test_learning_user_language_direction_with_invalid_answer(self):
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

        with self.app.app_context():
            db_word = db.session.query(DbWord).get(self.id_word)
            self.assertEqual(db_word.score, 0)
            self.assertEqual(db_word.is_learnt, False)

    def test_learning_user_language_direction_with_valid_answer(self):
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
            self.assertEqual(db_word.score, 2)

            db_repeat = db.session.query(
                DbUserWordRepeat
            ).filter(
                DbUserWordRepeat.id_word == self.id_word
            ).first()

            self.assertIsNone(db_repeat)

    def test_learning_user_language_direction_with_valid_answer_and_adding_word_to_repeat_table(self):
        with self.app.app_context():
            db_word = db.session.query(DbWord).get(self.id_word)
            db_word.score = self.words_learned_score - 1
            db.session.commit()

        data = {
            'direction': TranslationDirection.USER_LANGUAGE,
            'answers': [{'id_word': self.id_word, 'answer': '__translation_2__'}]
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

            self.assertIsNotNone(db_repeat)
