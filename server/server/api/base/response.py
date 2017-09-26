from flask import jsonify

from server.version import __version__
from server.api.base.request import get_current_request_token
from server.tools import dates
from server.tools.jwt import Jwt


class JsonResponse:
    """
    Json response
    """

    def __init__(self):
        self.error = None
        self.data = {}

    def jsonify(self):
        """
        Convert response to json string

        :return: json string
        :rtype: str
        """

        response = {
            "error": self.error,
            "data": self.data,
            "ver": __version__
        }

        return jsonify(**response)


def ok_response(data=None):
    response = JsonResponse()
    response.ok = True
    response.data = data

    token = get_current_request_token()
    if token is None:
        return response.jsonify()

    if not token.need_refresh:
        return response.jsonify()

    response.data["refresh_token"] = Jwt.generate(token.user_id, token.session_id)

    response = response.jsonify()
    response.set_cookie(
        'access_token',
        value=str(response.data["refresh_token"]['access_token']),
        expires=dates.from_iso(response.data["refresh_token"]['exp'])
    )

    return response


def bad_response(error, http_code=200):
    response = JsonResponse()
    response.error = error

    return response.jsonify(), http_code


def un_authorized_response():
    return bad_response('Unauthorized', 401)
