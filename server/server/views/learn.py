from flask import render_template
from flask.views import MethodView

from server.decorators.access_token_required import access_token_required


class LearnView(MethodView):
    @access_token_required
    def get(self):
        return render_template('learn.html')
