from flask.views import MethodView
from sqlalchemy import func

from server.api.base.request import get_current_request, get_current_user_id
from server.api.base.response import ok_jqdatatable_response
from server.database import db
from server.database.model import DbWord, DbWordType, DbTranslation, DbUserWordRepeat
from server.database.queries import get_db_user_by_id
from server.decorators.access_token_required import access_token_required
from server.tools import dates


class WordsDataTableAPI(MethodView):

    @access_token_required
    def post(self):
        request = get_current_request()
        current_user = get_db_user_by_id(get_current_user_id())

        db_words_count = db.session.query(
            func.count(DbWord.id_word)
        ).filter(
            DbWord.id_user == current_user.id_user,
            DbWord.is_in_use == True
        ).scalar()

        db_words = db.session.query(
            DbWord,
            DbWordType,
            DbUserWordRepeat.repeat_after_db_dts
        ).outerjoin(
            DbWordType,
            DbWordType.id_type == DbWord.id_word_type
        ).outerjoin(
            DbUserWordRepeat,
            DbUserWordRepeat.id_word == DbWord.id_word
        ).filter(
            DbWord.id_user == current_user.id_user,
            DbWord.is_in_use == True
        )

        if request.filter_by is not None:
            filter_param = '%' + request.filter_by + '%'
            db_words = db_words.filter(
                DbWord.word.ilike(filter_param),
            )

        if request.order_by is not None:
            if request.order_by == 'id_word':
                db_words = db_words.order_by('words.id_word ' + request.order_dir)
            elif request.order_by == 'word':
                db_words = db_words.order_by('words.word ' + request.order_dir)
            elif request.order_by == 'type_name':
                db_words = db_words.order_by('dc_word_types.name ' + request.order_dir)
            elif request.order_by == 'score':
                db_words = db_words.order_by('words.score ' + request.order_dir)
            elif request.order_by == 'add_db_dts':
                db_words = db_words.order_by('words.add_db_dts ' + request.order_dir)
            elif request.order_by == 'last_learn_db_dts':
                db_words = db_words.order_by('words.last_learn_db_dts ' + request.order_dir)
            elif request.order_by == 'repeat_db_dts':
                db_words = db_words.order_by('user_words_repeats.repeat_after_db_dts ' + request.order_dir)
            elif request.order_by == 'transcription':
                db_words = db_words.order_by('words.transcription ' + request.order_dir)
            else:
                db_words = db_words.order_by(DbWord.add_db_dts.desc())

        if (request.limit is not None) and (request.limit > 0):
            db_words = db_words.limit(request.limit)

        if (request.skip is not None) and (request.skip > 0):
            db_words = db_words.offset(request.skip)

        db_words = db_words.all()

        def map_func(word_data):
            word, word_type, repeat_db_dts = word_data

            return {
                'id_word': word.id_word,
                'word': word.word,
                'transcription': word.transcription,
                'id_type': None if word_type is None else word_type.id_type,
                'type_name': None if word_type is None else word_type.name,
                'translations': list(
                    map(
                        lambda i: {'id': i[0], 'translation': i[1]},
                        self._get_db_translation(word.id_word, current_user.id_language)
                    )
                ),
                'learn_score': word.score,
                'add_db_dts': dates.to_iso_datetime_string(word.add_db_dts),
                'last_learn_db_dts': dates.to_iso_datetime_string(word.last_learn_db_dts),
                'repeat_db_dts': dates.to_iso_datetime_string(repeat_db_dts)
            }

        table = list(map(map_func, db_words))

        if request.filter_by is not None:
            db_words_filtered = len(table)
        else:
            db_words_filtered = db_words_count

        jq_table = {'table': table}

        return ok_jqdatatable_response(request.draw, db_words_filtered, db_words_count, jq_table)

    def _get_db_translation(self, id_word, id_lang):
        db_translations = db.session.query(
            DbTranslation.id_translation,
            DbTranslation.translation
        ).filter(
            DbTranslation.id_word == id_word,
            DbTranslation.id_language == id_lang,
            DbTranslation.is_in_use == True
        ).all()

        return db_translations
