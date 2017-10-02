from flask import Blueprint

from server.api.auth.login import LoginAPI
from server.api.auth.logout import LogoutAPI
from server.api.dictionary.words import AddWordAPI

api_blueprint = Blueprint('api_blueprint', __name__)
api_blueprint.add_url_rule('/api/login', view_func=LoginAPI.as_view('login'), methods=['POST'])
api_blueprint.add_url_rule('/api/logout', view_func=LogoutAPI.as_view('logout'), methods=['POST'])
api_blueprint.add_url_rule('/api/words', view_func=AddWordAPI.as_view('words'), methods=['POST'])
