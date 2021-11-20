from flask import Response, request
from functools import wraps

TOKENS = ['f2dOqweIWy65QWlwiw', 'a1wreoijWeR20lsdwq']


def valid_credentials(token):
    '''
    Given a token, verifies if the token is valid
    '''
    return token in TOKENS


def authenticate(f):
    """
    Grabs token from request header and validates it
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        headers = request.headers
        bearer = headers.get('Authorization')
        token = bearer.split()[1]
        if not token or not valid_credentials(token):
            return Response('Invalid token', 401)
        return f(*args, **kwargs)
    return wrapper
