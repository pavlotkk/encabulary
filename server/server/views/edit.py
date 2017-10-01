from flask import render_template
from flask.views import MethodView


class EditView(MethodView):
    def get(self):
        return render_template('edit.html')
