from flask import Flask, Response, request
from functools import wraps

TOKENS = ['f2dOqweIWy65QWlwiw', 'a1wreoijWeR20lsdwq']

def valid_credentials(token):
    return token in TOKENS

def authenticate(f):
    """Determines if the access token is valid:
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.headers.get("Bearer")
        if not token or not valid_credentials(token):
            return Response('Invalid token', 401)
        return f(*args, **kwargs)
    return wrapper
