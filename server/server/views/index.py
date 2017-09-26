from flask import Blueprint

index_blueprint = Blueprint('index_blueprint', __name__, template_folder='templates')


@index_blueprint.route('/', methods=['GET'])
@index_blueprint.route('/index', methods=['GET'])
def show_index_page():
    return 'Hello World!'
