from flask import Blueprint

from server.api.auth.login import LoginAPI

api_blueprint = Blueprint('api_blueprint', __name__)
api_blueprint.add_url_rule('/api/login', view_func=LoginAPI.as_view('login'), methods=['POST'])

