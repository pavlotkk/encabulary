from flask import Blueprint

from server.views.index import IndexView
from server.views.learn import LearnView
from server.views.edit import EditView

view_blueprint = Blueprint('view_blueprint', __name__, template_folder='templates')

view_blueprint.add_url_rule('/', view_func=IndexView.as_view('default'), methods=['GET'])
view_blueprint.add_url_rule('/index', view_func=IndexView.as_view('index'), methods=['GET'])
view_blueprint.add_url_rule('/learn', view_func=LearnView.as_view('learn'), methods=['GET'])
view_blueprint.add_url_rule('/edit', view_func=EditView.as_view('edit'), methods=['GET'])
