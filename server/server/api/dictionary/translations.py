from flask.views import MethodView

from server.api.base.errors import ObjectDoesNotExists
from server.api.base.request import get_current_request, get_current_user_id
from server.api.base.response import ok_response, bad_response
from server.database import db
from server.database.management.db_manager import save_db_changes
from server.database.model import DbWord, DbTranslation
from server.database.queries.users import get_db_user_by_id
from server.decorators.access_token_required import access_token_required


class TranslationsAPI(MethodView):

    @access_token_required
    def post(self):
        request = get_current_request()
        current_user = get_db_user_by_id(get_current_user_id())

        id_word = request.get_int('id_word')
        translation = request.get_string('translation')

        if id_word is None:
            return bad_response('id_word is required')

        if not translation:
            return bad_response('translation is required')

        try:
            db_translation = self._add_db_translation_or_raise_exception(
                current_user.id_user,
                id_word,
                current_user.id_language,
                translation
            )
        except ObjectDoesNotExists as e:
            return bad_response(str(e))

        return ok_response({'id_translation': db_translation.id_translation})

    @access_token_required
    def get(self, id_translation):
        current_user_id = get_current_user_id()

        try:
            db_tr = self._get_db_translation_or_raise_exception(id_translation, current_user_id)
        except ObjectDoesNotExists as e:
            return bad_response(str(e))

        db_tr_to_dic = {
            'id_translation': db_tr.id_translation,
            'id_word': db_tr.id_word,
            'id_lang': db_tr.id_language,
            'translation': db_tr.translation
        }

        return ok_response({'translation': db_tr_to_dic})

    @access_token_required
    def put(self, id_translation):
        request = get_current_request()
        current_user_id = get_current_user_id()

        translation = request.get_string('translation')

        if not translation:
            return bad_response('translation is required')

        try:
            self._update_db_translation_or_raise_exception(
                id_translation,
                current_user_id,
                translation
            )
        except ObjectDoesNotExists as e:
            return bad_response(str(e))

        return ok_response()

    @access_token_required
    def delete(self, id_translation):
        current_user_id = get_current_user_id()

        try:
            self._delete_db_translation_or_raise_exception(id_translation, current_user_id)
        except ObjectDoesNotExists as e:
            return bad_response(str(e))

        return ok_response()

    def _get_db_translation_or_raise_exception(self, id_translation, id_user):
        """:rtype: DbTranslation"""
        db_tr = db.session.query(
            DbTranslation
        ).join(
            DbWord,
            (DbTranslation.id_word == DbWord.id_word) & (DbWord.id_user == id_user)
        ).filter(
            DbTranslation.id_translation == id_translation,
            DbTranslation.is_in_use == True
        ).first()

        if db_tr is None:
            raise ObjectDoesNotExists('translation <{}> does not exists'.format(id_translation))

        return db_tr

    def _add_db_translation_or_raise_exception(self, id_user, id_word, id_lang, translation):
        """:rtype: DbTranslation"""
        db_word_exists = db.session.query(
            db.session.query(
                DbWord
            ).filter(
                DbWord.id_word == id_word,
                DbWord.id_user == id_user,
                DbWord.is_in_use == True
            ).exists()
        ).scalar()

        if not db_word_exists:
            raise ObjectDoesNotExists('word <{}> does not exists'.format(id_word))

        db_translation = db.session.query(
            DbTranslation
        ).filter(
            DbTranslation.id_word == id_word,
            DbTranslation.id_language == id_lang,
            DbTranslation.translation == translation,
            DbTranslation.is_in_use == True
        ).first()

        if db_translation is not None:
            return db_translation

        db_translation = DbTranslation()
        db_translation.id_word = id_word
        db_translation.id_language = id_lang
        db_translation.translation = translation

        db.session.add(db_translation)
        save_db_changes()

        return db_translation

    def _update_db_translation_or_raise_exception(self, id_translation, id_user, translation):
        db_translation = self._get_db_translation_or_raise_exception(id_translation, id_user)

        db_translation.translation = translation

        save_db_changes()

    def _delete_db_translation_or_raise_exception(self, id_translation, id_user):
        db_translation = self._get_db_translation_or_raise_exception(id_translation, id_user)

        db_translation.is_in_use = False

        save_db_changes()
