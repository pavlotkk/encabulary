from flask.views import MethodView

from server.api.base.request import get_current_user_id, get_current_request
from server.api.base.response import bad_response, ok_response
from server.database import db
from server.database.management.db_manager import save_db_changes
from server.database.model import DbWord, DbUserWord
from server.decorators.access_token_required import access_token_required
import server.database.queries.users as users_query


class AddWordAPI(MethodView):

    @access_token_required
    def post(self):
        request = get_current_request()

        user_id = get_current_user_id()

        word = request.get_string('word')
        transcription = request.get_string('transcription')

        if not word:
            return bad_response('word is required')

        current_user = users_query.get_db_user_by_id(user_id)

        db_word = self.add_word_to_db(
            word,
            current_user.id_language,
            transcription
        )

        return ok_response({'id_word': db_word.id_word})

    def put(self):
        request = get_current_request()

        user_id = get_current_user_id()

        id_word = request.get_int('id_word')
        word = request.get_string('word')
        transcription = request.get_string('transcription')

        if not word:
            return bad_response('word is required')

        current_user = users_query.get_db_user_by_id(user_id)

        db_word = self.add_word_to_db(
            word,
            current_user.id_language,
            transcription
        )

        return ok_response({'id_word': db_word.id_word})

    def add_word_to_db(self, word, lang_id, transcription=None):
        db_word = db.session.query(
            DbWord
        ).filter(
            DbWord.word == word,
            DbWord.is_in_use == True
        ).first()

        if db_word:
            return db_word

        db_word = DbWord(word, transcription)
        db.session.add(db_word)
        db.session.flush()

        db_user_word = DbUserWord(db_word.id_word, lang_id)
        db.session.add(db_user_word)
        db.session.flush()

        save_db_changes()

        return db_word
