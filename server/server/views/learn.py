from flask import render_template
from flask.views import MethodView

from server.api.base.request import get_current_request
from server.decorators.access_token_required import AccessTokenRequired


class LearnView(MethodView):
    @AccessTokenRequired(redirect=True)
    def get(self):
        path = 'desktop'
        if get_current_request().is_from_mobile_device():
            path = 'mobile'

        return render_template('{}/learn.html'.format(path))
