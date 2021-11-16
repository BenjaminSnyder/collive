from flask import Flask, Response, request
from functools import wraps

API_KEYS = ['f2dOqweIWy65QWlwiw', 'a1wreoijWeR20lsdwq']

def valid_credentials(api_key):
    return api_key in API_KEYS

def authenticate(f):
    """Determines if the API key is valid:
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        key = request.headers.get("api_key")
        if not key or not valid_credentials(key):
            return Response('Invalid key', 401)
        return f(*args, **kwargs)
    return wrapper
