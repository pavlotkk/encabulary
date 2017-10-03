from flask import Blueprint

from server.api.auth.login import LoginAPI
from server.api.auth.logout import LogoutAPI
from server.api.dictionary.words import WordAPI
from server.api.dictionary.translations import TranslationsAPI

api_blueprint = Blueprint('api_blueprint', __name__)
api_blueprint.add_url_rule('/api/login', view_func=LoginAPI.as_view('login'), methods=['POST'])
api_blueprint.add_url_rule('/api/logout', view_func=LogoutAPI.as_view('logout'), methods=['POST'])

word_api_view = WordAPI.as_view('word')
api_blueprint.add_url_rule('/api/word', view_func=word_api_view, methods=['POST'])
api_blueprint.add_url_rule('/api/word/<int:id_word>', view_func=word_api_view, methods=['PUT', 'GET', 'DELETE'])

translation_api_view = TranslationsAPI.as_view('translation')
api_blueprint.add_url_rule('/api/translation', view_func=translation_api_view, methods=['POST'])
api_blueprint.add_url_rule('/api/translation/<int:id_translation>', view_func=translation_api_view,
                           methods=['GET', 'PUT'])
