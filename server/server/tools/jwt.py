from datetime import datetime

from jose import jwt as jose_jwt
from server.tools import dates
from flask import current_app


class Jwt:
    def __init__(self, user_id, session_id, iat, exp):
        self._user_id = user_id
        self._session_id = session_id
        self._created_at = datetime.utcfromtimestamp(iat)
        self._expired_at = datetime.utcfromtimestamp(exp)


    @classmethod
    def from_http_request(cls, http_request):
        """
        Create Jwt manager
        :param http_request: flask http request
        :raises ValueError, JWTError, ExpiredSignatureError
        :return: Jwt
        """

        if http_request is None:
            raise ValueError("Http request can not be None")

        encoded_access_token = Jwt.get_encoded_token(http_request)
        access_token = Jwt.decode(encoded_access_token)

        return cls(
            user_id=access_token.get('user_id', 0),
            session_id=access_token.get('session_id', None),
            iat=access_token.get('iat', 0),
            exp=access_token.get('exp', 0)
        )

    @property
    def user_id(self):
        return self._user_id

    @property
    def session_id(self):
        return self._session_id

    @property
    def created_at(self):
        return self._created_at

    @property
    def expired_at(self):
        return self._created_at

    @property
    def need_refresh(self):
        """:rtype: bool"""

        if self._created_at is None:
            return False

        update_after = self._created_at + current_app.config['JWT_AUTO_UPDATE_AFTER']
        now = datetime.utcnow()

        return now > update_after

    @staticmethod
    def create_refreshed(user_id, session_id):

        iat = datetime.utcnow()
        token_expired = iat + current_app.config['JWT_ACCESS_TOKEN_EXPIRES']

        payload = {
            'exp': token_expired,
            'iat': iat,
            'user_id': user_id,
            'session_id': session_id
        }

        try:
            access_token = jose_jwt.encode(
                payload,
                current_app.config['SECRET_KEY'],
                algorithm=current_app.config['JWT_ALGORITHM']
            )

            return {
                'access_token': access_token,
                'exp': dates.to_iso_datetime_string(token_expired)
            }
        except jose_jwt.JWTError:
            return None

    @staticmethod
    def generate(user_id, session_id):
        iat = datetime.utcnow()
        expires = iat + current_app.config['JWT_TOKEN_EXPIRES']

        payload = {
            'exp': expires,
            'iat': iat,
            'user_id': user_id,
            'session_id': session_id
        }

        try:
            access_token = jose_jwt.encode(
                payload,
                current_app.config['SECRET_KEY'],
                algorithm=current_app.config['JWT_ALGORITHM']
            )

            return {
                'access_token': access_token,
                'exp': dates.to_iso_datetime_string(expires)
            }
        except jose_jwt.JWTError as e:
            return None

    @staticmethod
    def get_encoded_token(http_request):
        header_token = http_request.headers.get('Authorization')
        cookie_token = http_request.cookies.get('access_token')

        if cookie_token is not None:
            return cookie_token

        if header_token is not None:
            if current_app.config['JWT_HEADER_TYPE'] not in header_token:
                raise ValueError('Token with invalid header')

            return header_token.split(' ')[1]

        raise ValueError('Token can not be None')

    @staticmethod
    def decode(encoded_token):
        return jose_jwt.decode(
            encoded_token,
            current_app.config['SECRET_KEY'],
            algorithms=current_app.config['JWT_ALGORITHM']
        )
