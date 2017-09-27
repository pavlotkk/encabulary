from flask import Blueprint, render_template

from server.decorators.access_token_required import access_token_required

view_blueprint = Blueprint('view_blueprint', __name__, template_folder='templates')


@view_blueprint.route('/', methods=['GET'])
@view_blueprint.route('/index', methods=['GET'])
def show_index_page():
    return render_template('index.html')


@view_blueprint.route('/learn', methods=['GET'])
@access_token_required
def show_learn_page():
    return render_template('learn.html')


@view_blueprint.route('/edit', methods=['GET'])
@access_token_required
def show_edit_page():
    return render_template('edit.html')
