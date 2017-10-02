from functools import wraps

from server.api.base.request import get_current_request_token
from server.api.base.response import un_authorized_response
import server.database.queries as db_query
from jose import exceptions as jose_ex


def access_token_required(fn):

    @wraps(fn)
    def is_token_accepted(*args, **kwargs):
        try:
            token = get_current_request_token(silent=False)
        except (ValueError, jose_ex.ExpiredSignatureError, jose_ex.JWTError):
            return un_authorized_response()

        db_user = db_query.get_db_user_by_id(token.user_id)
        if db_user.id_session is None:
            return un_authorized_response()

        return fn(*args, **kwargs)
    return is_token_accepted
