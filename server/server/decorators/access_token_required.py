from functools import wraps

from server.api.base.request import is_authenticated
from server.api.base.response import un_authorized_response


class AccessTokenRequired:
    def __init__(self, redirect=False):
        self.redirect = redirect

    def __call__(self, fn, *args, **kwargs):
        @wraps(fn)
        def is_token_accepted(*args, **kwargs):
            if not is_authenticated():
                return self.un_authorized_response_or_redirect()

            return fn(*args, **kwargs)
        return is_token_accepted

    def un_authorized_response_or_redirect(self):
        if self.redirect:
            from flask import redirect as flask_redirect
            return flask_redirect('/')
        return un_authorized_response()
