import datetime
from collections import defaultdict

from flask import current_app
from flask.views import MethodView

from server.api.base.request import get_current_user_id
from server.api.base.response import ok_response
from server.database import db
from server.database.queries import get_db_user_by_id
from server.decorators.access_token_required import access_token_required
from server.database.model import DbWord, DbWordType, DbTranslation, DbUserWordRepeat


class LearnAPI(MethodView):

    def __init__(self):
        self.max_words_count = current_app.config['MAX_WORDS_TO_LEARN_BY_REQUEST']

    @access_token_required
    def get(self):
        current_user = get_db_user_by_id(get_current_user_id())

        words_to_learn = self._get_db_words_to_learn(current_user.id_user, current_user.id_language)
        grouped_words_to_learn = self._group_word_translations(words_to_learn)

        words_to_repeat = self._get_db_words_to_repeat(current_user.id_user, current_user.id_language)
        grouped_words_to_repeat = self._group_word_translations(words_to_repeat)

        return ok_response({
            'repeat': [
                {
                    'id_word': item[0],
                    'word': item[1],
                    'translations': grouped_words_to_repeat[item[0]]
                } for item in words_to_repeat
            ],
            'learn': [
                {
                    'id_word': item[0],
                    'word': item[1],
                    'translations': grouped_words_to_learn[item[0]]
                } for item in words_to_learn
            ]
        })

    def _get_db_words_to_learn(self, user_id, user_lang_id):
        db_words = db.session.query(
            DbWord.id_word,
            DbWord.word,
            DbTranslation.translation,
            DbWordType.name
        ).filter(
            DbWord.id_user == user_id,
            DbWord.is_in_use == True,
            DbWord.is_learnt == False,
            DbTranslation.is_in_use == True
        ).join(
            DbTranslation,
            (DbTranslation.id_word == DbWord.id_word) & (DbTranslation.id_language == user_lang_id)
        ).outerjoin(
            DbWordType,
            DbTranslation.id_word_type == DbWordType.id_type
        ).order_by(
            DbWord.add_db_dts.desc()
        ).limit(
            self.max_words_count
        ).all()

        return db_words

    def _get_db_words_to_repeat(self, user_id, user_lang_id):
        now = datetime.datetime.utcnow()

        db_words = db.session.query(
            DbWord.id_word,
            DbWord.word,
            DbTranslation.translation,
            DbWordType.name
        ).join(
            DbUserWordRepeat,
            DbUserWordRepeat.id_word == DbWord.id_word
        ).join(
            DbTranslation,
            (DbTranslation.id_word == DbWord.id_word) & (DbTranslation.id_language == user_lang_id)
        ).outerjoin(
            DbWordType,
            DbTranslation.id_word_type == DbWordType.id_type
        ).filter(
            DbWord.id_user == user_id,
            DbWord.is_in_use == True,
            DbWord.is_learnt == False,
            DbTranslation.is_in_use == True,
            DbUserWordRepeat.repeat_after_db_dts <= now
        ).order_by(
            DbWord.add_db_dts.desc()
        ).all()

        return db_words

    def _group_word_translations(self, words):
        grouped_words = defaultdict(list)
        for word in words:
            grouped_words[word[0]].append({'translation': word[2], 'id_type': word[3]})

        return grouped_words
