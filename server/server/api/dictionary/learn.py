import datetime
from collections import defaultdict
from sqlalchemy import func
from flask import current_app
from flask.views import MethodView

from server.api.base.request import get_current_user_id, get_current_request
from server.api.base.response import ok_response, bad_response
from server.database import db
from server.database.queries import get_db_user_by_id
from server.decorators.access_token_required import access_token_required
from server.database.model import DbWord, DbWordType, DbTranslation, DbUserWordRepeat
from server.tools import types


class LearnAPI(MethodView):

    def __init__(self):
        self.max_words_count = current_app.config['MAX_WORDS_TO_LEARN_BY_REQUEST']

    @access_token_required
    def get(self):
        current_user = get_db_user_by_id(get_current_user_id())

        words_to_learn = self._get_db_words_to_learn(current_user.id_user)
        words_to_repeat = self._get_db_words_to_repeat(current_user.id_user)

        return ok_response({
            'repeat': [
                {
                    'id_word': item[0],
                    'word': item[1],
                    'translations': [
                        {
                            'translation': tr,
                            'id_type': id_type
                        } for (tr, id_type) in self._get_db_translation(item[0], current_user.id_language)
                    ]
                } for item in words_to_repeat
            ],
            'learn': [
                {
                    'id_word': item[0],
                    'word': item[1],
                    'translations': [
                        {
                            'translation': tr,
                            'id_type': id_type
                        } for (tr, id_type) in self._get_db_translation(item[0], current_user.id_language)
                    ]
                } for item in words_to_learn
            ]
        })

    def _get_db_words_to_learn(self, user_id):
        db_words = db.session.query(
            DbWord.id_word,
            DbWord.word
        ).filter(
            DbWord.id_user == user_id,
            DbWord.is_in_use == True,
            DbWord.is_learnt == False
        ).order_by(
            DbWord.add_db_dts.desc()
        ).limit(
            self.max_words_count
        ).all()

        return db_words

    def _get_db_translation(self, id_word, id_lang):
        db_translations = db.session.query(
            DbTranslation.translation,
            DbWordType.name
        ).outerjoin(
            DbWordType,
            DbTranslation.id_word_type == DbWordType.id_type
        ).filter(
            DbTranslation.id_word == id_word,
            DbTranslation.id_language == id_lang,
            DbTranslation.is_in_use == True
        ).all()

        return db_translations

    def _get_db_words_to_repeat(self, user_id):
        now = datetime.datetime.utcnow()

        db_words = db.session.query(
            DbWord.id_word,
            DbWord.word
        ).join(
            DbUserWordRepeat,
            DbUserWordRepeat.id_word == DbWord.id_word
        ).filter(
            DbWord.id_user == user_id,
            DbWord.is_in_use == True,
            DbWord.is_learnt == False,
            DbUserWordRepeat.repeat_after_db_dts <= now
        ).order_by(
            DbWord.add_db_dts.desc()
        ).all()

        return db_words

    def _get_db_word(self, word_id, user_id, user_lang_id):
        db_words = db.session.query(
            DbWord.id_word,
            DbWord.word,
            DbTranslation.translation,
            DbWordType.name
        ).filter(
            DbWord.id_word == word_id,
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
        ).all()

        return db_words

