from flask import render_template
from flask.views import MethodView


class LearnView(MethodView):
    def get(self):
        return render_template('learn.html')
