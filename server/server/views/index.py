from flask import render_template, redirect
from flask.views import MethodView

from server.api.base.request import is_authenticated


class IndexView(MethodView):
    def get(self):
        if not is_authenticated():
            return render_template('index.html')

        return redirect('/learn')
