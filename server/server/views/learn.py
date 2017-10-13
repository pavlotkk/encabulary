from flask import render_template
from flask.views import MethodView

from server.decorators.access_token_required import AccessTokenRequired


class LearnView(MethodView):
    @AccessTokenRequired(redirect=True)
    def get(self):
        return render_template('learn.html')
