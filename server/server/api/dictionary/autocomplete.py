from flask.views import MethodView

from server.api.base.response import ok_response
from server.autocomplete.oxford_dictionary import OxfordDictionary
from server.autocomplete.linguee import LingueeDictionary
from server.database.model import DbWordType


class AutoCompleteAPI(MethodView):
    def get(self, word, id_word_type=None):
        if ' ' in word:
            word = word.replace(' ', '-')

        oxford_dictionary = OxfordDictionary()
        oxford_item = oxford_dictionary.get_item(word)

        if not id_word_type:
            id_word_type = DbWordType.get_id_by_name(oxford_item.word_type_name)

        linguee_dictionary = LingueeDictionary()
        linguee_items = linguee_dictionary.get_items(word)

        translations = [item.translations for item in linguee_items if
                        DbWordType.get_id_by_name(item.word_type_name) == id_word_type]

        if translations:
            translations = translations[0]

        return ok_response({
            'word': {
                'transcription': oxford_item.transcription,
                'id_word_type': id_word_type,
                'translations': translations
            }
        })
