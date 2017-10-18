from flask import render_template
from flask.views import MethodView

from server.api.base.request import get_current_request
from server.database import db
from server.database.model import DbWordType
from server.decorators.access_token_required import AccessTokenRequired


class EditView(MethodView):
    @AccessTokenRequired(redirect=True)
    def get(self):
        word_types = db.session.query(
            DbWordType
        ).order_by(
            DbWordType.name
        ).all()

        path = 'desktop'
        if get_current_request().is_from_mobile_device():
            path = 'mobile'

        return render_template('{}/edit.html'.format(path), word_types=word_types)
