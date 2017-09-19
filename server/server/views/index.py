from flask import Blueprint

index_blueprint = Blueprint('index_blueprint', __name__, template_folder='templates')


@index_blueprint.route('/')
@index_blueprint.route('/index')
def show_index_page():
    return 'Hello World!'
