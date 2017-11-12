import datetime

from server.database import db
from server.database.model import DbWord, DbTranslation, DbLanguage, DbUserWordRepeat
from server.database.queries import get_min_db_repeat
from server.tests.functional_tests.base import BaseAuthTestCase


class BaseLearnTestCase(BaseAuthTestCase):
    def setUp(self):
        super().setUp()

        self.words_learned_score = self.app.config['WORD_LEARNED_SCORE']
        self.id_word = None
        self.db_translations = []
        with self.app.app_context():
            db_word = DbWord(self.test_user_id, '__test__', 1)
            db_word.score = 1
            db.session.add(db_word)
            db.session.flush()

            db_tr_1 = DbTranslation(db_word.id_word, DbLanguage.RU, '__translation_1__')
            db_tr_2 = DbTranslation(db_word.id_word, DbLanguage.RU, '__translation_2__')
            db.session.add(db_tr_1)
            db.session.add(db_tr_2)
            db.session.flush()

            db.session.commit()

            self.id_word = db_word.id_word
            self.db_translations = [db_tr_1.translation, db_tr_2.translation]

    def _api_get_words_to_learn(self):
        return self.get_json_response('/api/learn', method='GET', params={})

    def _api_send_user_answers(self, params):
        return self.get_json_response('/api/learn', method='POST', params=params)


class BaseRepeatTestCase(BaseLearnTestCase):
    def setUp(self):
        super().setUp()

        with self.app.app_context():
            db_word = db.session.query(DbWord).get(self.id_word)
            db_word.score = self.words_learned_score
            db_word.is_learnt = True
            db.session.flush()

            min_repeat = get_min_db_repeat()
            db_user_repeat = DbUserWordRepeat(self.id_word)
            db_user_repeat.id_repeat = min_repeat.id_repeat
            db_user_repeat.repeat_after_db_dts = datetime.datetime.utcnow() - datetime.timedelta(days=min_repeat.repeat_days)
            db.session.add(db_user_repeat)
            db.session.flush()

            db.session.commit()


class TestLearningWithInvalidParams(BaseLearnTestCase):
    def test_direction_required(self):
        invalid_directions = [None, 'unknown']

        for direction in invalid_directions:
            response = self._api_send_user_answers({'direction': direction})
            self.assertIsNotNone(response['error'])
