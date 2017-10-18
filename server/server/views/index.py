from flask import render_template, redirect
from flask.views import MethodView

from server.api.base.request import is_authenticated, get_current_request


class IndexView(MethodView):
    def get(self):
        if not is_authenticated():

            path = 'desktop'
            if get_current_request().is_from_mobile_device():
                path = 'mobile'

            return render_template('{}/index.html'.format(path))

        return redirect('/learn')
