from flask.views import MethodView

from server.api.base.errors import ObjectDoesNotExists
from server.api.base.request import get_current_request, get_current_user_id
from server.api.base.response import ok_response, bad_response
from server.database import db
from server.database.management.db_manager import save_db_changes
from server.database.model import DbWord, DbTranslation
from server.database.queries.users import get_db_user_by_id


class TranslationsAPI(MethodView):
    def post(self):
        request = get_current_request()
        current_user = get_db_user_by_id(get_current_user_id())

        id_word = request.get_int('id_word')
        id_word_type = request.get_int('id_word_type')
        translation = request.get_string('translation')

        if id_word is None:
            return bad_response('id_word is required')

        if not translation:
            return bad_response('translation is required')

        try:
            db_translation = self._add_translation_or_raise_exception(
                current_user.id_user,
                id_word,
                id_word_type,
                current_user.id_language,
                translation
            )
        except ObjectDoesNotExists as e:
            return bad_response(str(e))

        return ok_response({'id_translation': db_translation.id_translation})

    def _add_translation_or_raise_exception(self, id_user, id_word, id_word_type, id_lang, translation):
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
        db_translation.id_word_type = id_word_type
        db_translation.translation = translation

        db.session.add(db_translation)
        save_db_changes()

        return db_translation
