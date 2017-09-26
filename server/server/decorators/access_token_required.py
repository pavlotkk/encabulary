from functools import wraps

from server.api.base.request import get_current_request_token
from server.api.base.response import un_authorized_response, invalid_token_response
import server.database.queries as db_query
from jose import jwt as jose_jwt


def access_token_required(fn):

    @wraps(fn)
    def is_token_accepted(*args, **kwargs):
        try:
            token = get_current_request_token(silent=False)
        except ValueError or jose_jwt.ExpiredSignatureError or jose_jwt.JWTError:
            return un_authorized_response()

        db_user = db_query.get_db_user_by_id(token.user_id)
        if db_user.id_session is None:
            return un_authorized_response()

        return fn(*args, **kwargs)
    return is_token_accepted
