import uuid

from flask.views import MethodView

from server.api.base.request import get_current_request
from server.api.base.response import ok_response, bad_response
from server.database.management.db_manager import save_db_changes
from server.database.queries import get_db_user_by_email
from server.tools.jwt import Jwt
from server.tools.passwords import verify_password


class LoginAPI(MethodView):
    def post(self):
        request = get_current_request()

        email = request.get_string('email')
        password = request.get_string('password')

        if email is None:
            return bad_response('Email required')
        if password is None:
            return bad_response('Password required')

        db_user = get_db_user_by_email(email)
        if db_user is None:
            return bad_response('Invalid login or password')

        is_password_verified = verify_password(password, db_user.password, db_user.password_salt)
        if not is_password_verified:
            return bad_response('Invalid login or password')

        access_token = self.create_user_session_and_access_token(db_user)

        return ok_response({
            'access_token': access_token
        })

    def create_user_session_and_access_token(self, db_user):
        if db_user.id_session is None:
            db_user.id_session = uuid.uuid4().hex
            save_db_changes()

        access_token = Jwt.generate(db_user.id_user, db_user.id_session)
        return access_token