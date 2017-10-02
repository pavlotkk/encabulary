from flask import Blueprint

from server.api.auth.login import LoginAPI
from server.api.auth.logout import LogoutAPI
from server.api.dictionary.words import AddWordAPI

api_blueprint = Blueprint('api_blueprint', __name__)
api_blueprint.add_url_rule('/api/login', view_func=LoginAPI.as_view('login'), methods=['POST'])
api_blueprint.add_url_rule('/api/logout', view_func=LogoutAPI.as_view('logout'), methods=['POST'])

word_api_view = AddWordAPI.as_view('word')
api_blueprint.add_url_rule('/api/word', view_func=word_api_view, methods=['POST'])
api_blueprint.add_url_rule('/api/word/<int:id_word>', view_func=word_api_view, methods=['PUT'])
