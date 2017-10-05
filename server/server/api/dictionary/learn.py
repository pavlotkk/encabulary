import datetime

from flask import current_app
from flask.views import MethodView

from server.api.base.request import get_current_user_id, get_current_request
from server.api.base.response import ok_response, bad_response
from server.database import db
from server.database.management.db_manager import save_db_changes
from server.database.model import DbWord, DbWordType, DbTranslation, DbUserWordRepeat
from server.database.model.translation_direction import TranslationDirection
from server.database.queries import get_db_user_by_id, get_db_user_word_by_id, get_min_db_repeat
from server.decorators.access_token_required import access_token_required
from server.tools import types


class LearnException(Exception):
    def __init__(self, correct_values=None):
        self.connect_value = correct_values


class LearnAPI(MethodView):

    def __init__(self):
        self.max_words_count = current_app.config['MAX_WORDS_TO_LEARN_BY_REQUEST']
        self.words_learned_score = current_app.config['WORD_LEARNED_SCORE']

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
                    'type_name': item[2],
                    'transcription': item[3],
                    'translations': [
                        tr for (tr, ) in self._get_db_translation(item[0], current_user.id_language)
                    ]
                } for item in words_to_repeat
            ],
            'learn': [
                {
                    'id_word': item[0],
                    'word': item[1],
                    'type_name': item[2],
                    'transcription': item[3],
                    'translations': [
                        tr for (tr,) in self._get_db_translation(item[0], current_user.id_language)
                    ]
                } for item in words_to_learn
            ]
        })

    @access_token_required
    def post(self):
        request = get_current_request()
        current_user = get_db_user_by_id(get_current_user_id())

        direction = request.get_string('direction')
        if direction is None:
            return bad_response('direction is required')

        direction = direction.lower()
        if direction not in [TranslationDirection.ORIGINAL, TranslationDirection.USER_LANGUAGE]:
            return bad_response('unknown direction type. Supported types are "original", "user_language"')

        user_answers = request.get_obj_list('answers')
        result_mistakes = []
        result_ok_count = 0

        for answer_obj in user_answers:
            word_id = types.to_int(answer_obj.get('id_word'))
            answer = answer_obj.get('answer')

            if word_id is None:
                continue

            db_word = get_db_user_word_by_id(current_user.id_user, word_id)

            if db_word is None:
                continue

            try:
                if direction == TranslationDirection.ORIGINAL:
                    self._process_original_direction_answer_or_raise_exception(
                        db_word,
                        answer
                    )
                elif direction == TranslationDirection.USER_LANGUAGE:
                    self._process_user_language_direction_answer_or_raise_exception(
                        db_word,
                        current_user.id_language,
                        answer
                    )

                result_ok_count += 1
            except LearnException as e:
                result_mistakes.append({
                    'answer': answer,
                    'correct': e.connect_value
                })

                db_word.is_learnt = False

                if db_word.score > 0:
                    db_word.score -= 1

                db.session.query(
                    DbUserWordRepeat
                ).filter(
                    DbUserWordRepeat.id_word == db_word.id_word
                ).delete(synchronize_session='fetch')

                db.session.flush()

        save_db_changes()

        return ok_response({
            'result': {
                'ok_count': result_ok_count,
                'mistakes_count': len(result_mistakes),
                'mistakes': result_mistakes
            }
        })

    def _get_db_words_to_learn(self, user_id):
        db_words = db.session.query(
            DbWord.id_word,
            DbWord.word,
            DbWordType.name,
            DbWord.transcription
        ).join(
            DbWordType,
            DbWord.id_word_type == DbWordType.id_type
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
            DbTranslation.translation
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
            DbWord.word,
            DbWordType.name,
            DbWord.transcription
        ).join(
            DbUserWordRepeat,
            DbUserWordRepeat.id_word == DbWord.id_word
        ).join(
            DbWordType,
            DbWord.id_word_type == DbWordType.id_type
        ).filter(
            DbWord.id_user == user_id,
            DbWord.is_in_use == True,
            DbWord.is_learnt == True,
            DbUserWordRepeat.repeat_after_db_dts <= now
        ).order_by(
            DbWord.add_db_dts.desc()
        ).all()

        return db_words

    def _process_original_direction_answer_or_raise_exception(self, db_word, answer):
        if db_word.word != answer:
            raise LearnException(db_word.word)

        db_word.score += 1
        if db_word.score >= self.words_learned_score:
            db_word.score = self.words_learned_score
            db_word.is_learnt = True

            self._update_repeat_table(db_word)

    def _process_user_language_direction_answer_or_raise_exception(self, db_word, id_lang, answer):
        db_translations = db.session.query(
            DbTranslation.translation
        ).filter(
            DbTranslation.id_word == db_word.id_word,
            DbTranslation.id_language == id_lang,
            DbTranslation.is_in_use == True
        ).all()

        is_correct_answer = any([tr for (tr, ) in db_translations if tr == answer])

        if not is_correct_answer:
            raise LearnException([tr for (tr, ) in db_translations])

        db_word.score += 1
        if db_word.score >= self.words_learned_score:
            db_word.score = self.words_learned_score
            db_word.is_learnt = True

            self._update_repeat_table(db_word)

    def _update_repeat_table(self, db_word):
        db_repeat = db.session.query(
            DbUserWordRepeat
        ).filter(
            DbUserWordRepeat.id_word == db_word.id_word
        ).first()

        if db_repeat is not None:
            db_repeat.set_next_repeat_dts()
        else:
            min_repeat = get_min_db_repeat()
            db_repeat = DbUserWordRepeat(db_word.id_word)
            db_repeat.set_repeat(min_repeat)
            db.session.add(db_repeat)
            db.session.flush()
