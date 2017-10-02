from flask.views import MethodView

from server.api.base.errors import ObjectDoesNotExists
from server.api.base.request import get_current_user_id, get_current_request
from server.api.base.response import bad_response, ok_response
from server.database import db
from server.database.management.db_manager import save_db_changes
from server.database.model import DbWord
from server.decorators.access_token_required import access_token_required


class AddWordAPI(MethodView):

    @access_token_required
    def post(self):
        request = get_current_request()

        user_id = get_current_user_id()

        word = request.get_string('word')
        transcription = request.get_string('transcription')

        if not word:
            return bad_response('word is required')

        db_word = self.add_word_to_db(user_id, word, transcription)

        return ok_response({'id_word': db_word.id_word})

    @access_token_required
    def put(self, id_word):
        request = get_current_request()

        user_id = get_current_user_id()

        word = request.get_string('word')
        transcription = request.get_string('transcription')

        if not word:
            return bad_response('word is required')

        try:
            self.update_db_word_or_raise_exception(user_id, id_word, word, transcription)
        except ObjectDoesNotExists as e:
            return bad_response(str(e))

        return ok_response()

    def add_word_to_db(self, id_user, word, transcription=None):
        db_word = db.session.query(
            DbWord
        ).filter(
            DbWord.id_user == id_user,
            DbWord.word == word,
            DbWord.is_in_use == True
        ).first()

        if db_word:
            return db_word

        db_word = DbWord(id_user, word, transcription)
        db.session.add(db_word)
        db.session.flush()

        save_db_changes()

        return db_word

    def update_db_word_or_raise_exception(self, id_user, id_word, word, transcription=None):
        db_word = db.session.query(
            DbWord
        ).filter(
            DbWord.id_user == id_user,
            DbWord.id_word == id_word,
            DbWord.is_in_use == True
        ).first()

        if not db_word:
            raise ObjectDoesNotExists('word with id <{}> does not exists'.format(id_word))

        db_word.word = word
        db_word.transcription = transcription

        save_db_changes()
