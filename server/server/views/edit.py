from flask import render_template
from flask.views import MethodView

from server.database import db
from server.database.model import DbWordType
from server.decorators.access_token_required import access_token_required


class EditView(MethodView):
    @access_token_required
    def get(self):
        word_types = db.session.query(
            DbWordType
        ).order_by(
            DbWordType.name
        ).all()

        return render_template('edit.html', word_types=word_types)
