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
        self._response = {
            'error': None,
            'data': None,
            'ver': __version__
        }

    def jsonify(self):
        """
        Convert response to json string

        :return: json string
        :rtype: str
        """

        self._flush()

        return jsonify(**self._response)

    def _flush(self):
        self._response['error'] = self.error
        self._response['data'] = self.data


class JQueryDataTableResponse(JsonResponse):
    def __init__(self):
        super().__init__()

        self.length = 0
        self.draw = 0
        self.filtered = 0

        self._response['draw'] = 0
        self._response['recordsFiltered'] = 0
        self._response['recordsTotal'] = 0

    def _flush(self):
        super()._flush()

        self._response['draw'] = self.draw
        self._response['recordsFiltered'] = self.filtered
        self._response['recordsTotal'] = self.length


def ok_response(data=None):
    response = JsonResponse()
    response.ok = True
    response.data = data

    return _jsonify(response)


def ok_jqdatatable_response(draw, filtered, length, data=None):
    response = JQueryDataTableResponse()
    response.ok = True
    response.data = data
    response.draw = draw
    response.filtered = filtered
    response.length = length

    return _jsonify(response)


def bad_response(error, http_code=200):
    response = JsonResponse()
    response.error = error

    return response.jsonify(), http_code


def un_authorized_response():
    response, code = bad_response('Unauthorized', 401)
    response.set_cookie('access_token', '', expires=0)
    return response, code


def _jsonify(response):
    token = get_current_request_token()
    if token is None:
        return response.jsonify()

    if not token.need_refresh:
        return response.jsonify()

    response.data['refresh_token'] = Jwt.generate(token.user_id, token.session_id)

    response = response.jsonify()
    response.set_cookie(
        'access_token',
        value=str(response.data['refresh_token']['access_token']),
        expires=dates.from_iso(response.data['refresh_token']['exp'])
    )

    return response
