from flask.views import MethodView

from server.api.base.errors import ObjectDoesNotExists
from server.api.base.request import get_current_user_id, get_current_request
from server.api.base.response import bad_response, ok_response
from server.database import db
from server.database.management.db_manager import save_db_changes
from server.database.model import DbWord, DbTranslation, DbWordType
from server.database.queries import get_db_user_by_id
from server.decorators.access_token_required import AccessTokenRequired
from server.tools import dates


class WordAPI(MethodView):

    @AccessTokenRequired()
    def post(self):
        request = get_current_request()

        current_user = get_db_user_by_id(get_current_user_id())

        word = request.get_string('word')
        id_word_type = request.get_int('id_type')
        transcription = request.get_string('transcription')

        translations = request.get_obj_list('translations')

        if not word:
            return bad_response('word is required')

        word = word.lower()

        if not id_word_type:
            return bad_response('id_type is required')

        if not translations:
            db_word = self._add_word_to_db(current_user.id_user, word, id_word_type, transcription)
        else:
            db_word = self._add_word_and_translations_to_db(
                current_user.id_user,
                current_user.id_language,
                word,
                id_word_type,
                transcription,
                translations
            )

        return ok_response({'id_word': db_word.id_word})

    @AccessTokenRequired()
    def put(self, id_word):
        request = get_current_request()

        user_id = get_current_user_id()

        word = request.get_string('word')
        id_word_type = request.get_int('id_type')
        transcription = request.get_string('transcription')

        if not word:
            return bad_response('word is required')

        word = word.lower()

        if not id_word_type:
            return bad_response('id_type is required')

        try:
            self._update_db_word_or_raise_exception(user_id, id_word, word, id_word_type, transcription)
        except ObjectDoesNotExists as e:
            return bad_response(str(e))

        return ok_response()

    @AccessTokenRequired()
    def get(self, id_word):
        user_id = get_current_user_id()

        try:
            db_word = self._get_db_word_or_raise_exception(user_id, id_word)
        except ObjectDoesNotExists as e:
            return bad_response(str(e))

        word_type_name = db.session.query(
            DbWordType.name
        ).filter(
            DbWordType.id_type == db_word.id_word_type
        ).scalar()

        db_word_to_dict = {
            'id_word': db_word.id_word,
            'type_name': word_type_name,
            'word': db_word.word,
            'transcription': db_word.transcription,
            'score': db_word.score,
            'is_learnt': db_word.is_learnt,
            'last_learn_utc': dates.to_iso_datetime_string(db_word.last_learn_db_dts),
            'add_utc': dates.to_iso_datetime_string(db_word.add_db_dts)
        }

        return ok_response({
            'word': db_word_to_dict
        })

    @AccessTokenRequired()
    def delete(self, id_word):
        user_id = get_current_user_id()

        try:
            self._delete_cascade_db_word_or_raise_exception(user_id, id_word)
        except ObjectDoesNotExists as e:
            return bad_response(str(e))

        return ok_response()

    def _add_word_to_db(self, id_user, word, id_word_type, transcription=None):
        db_word = db.session.query(
            DbWord
        ).filter(
            DbWord.id_user == id_user,
            DbWord.word == word,
            DbWord.id_word_type == id_word_type,
            DbWord.is_in_use == True
        ).first()

        if db_word:
            return db_word

        db_word = DbWord(id_user, word, id_word_type, transcription)
        db.session.add(db_word)
        db.session.flush()

        save_db_changes()

        return db_word

    def _add_word_and_translations_to_db(self, id_user, id_user_lang, word, id_word_type,
                                         transcription=None, translations=None):

        db_word = self._add_word_to_db(id_user, word, id_word_type, transcription)

        for tr in translations:
            db_translation = db.session.query(
                DbTranslation
            ).filter(
                DbTranslation.id_word == db_word.id_word,
                DbTranslation.id_language == id_user_lang,
                DbTranslation.translation == tr,
                DbTranslation.is_in_use == True
            ).first()

            if db_translation is not None:
                continue

            db_translation = DbTranslation(db_word.id_word, id_user_lang, tr)
            db.session.add(db_translation)

        save_db_changes()

        return db_word

    def _get_db_word_or_raise_exception(self, id_user, id_word):
        """
        :rtype: DbWord
        """

        db_word = db.session.query(
            DbWord
        ).filter(
            DbWord.id_user == id_user,
            DbWord.id_word == id_word,
            DbWord.is_in_use == True
        ).first()

        if not db_word:
            raise ObjectDoesNotExists('word with id <{}> does not exists'.format(id_word))

        return db_word

    def _update_db_word_or_raise_exception(self, id_user, id_word, word, id_word_type, transcription=None):
        db_word = self._get_db_word_or_raise_exception(id_user, id_word)

        db_word.word = word
        db_word.transcription = transcription
        db_word.id_word_type = id_word_type

        save_db_changes()

    def _delete_cascade_db_word_or_raise_exception(self, id_user, id_word):

        db_word = self._get_db_word_or_raise_exception(id_user, id_word)

        db_word.is_in_use = False

        db.session.query(
            DbTranslation
        ).filter(
            DbTranslation.id_word == id_word
        ).update({
            DbTranslation.is_in_use: False
        })

        save_db_changes()
