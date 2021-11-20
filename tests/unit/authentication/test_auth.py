import pytest # noqa
from authentication.auth import valid_credentials


def test_valid_credentials():
    result1 = valid_credentials('f2dOqweIWy65QWlwiw')
    result2 = valid_credentials('a1wreoijWeR20lsdwq')
    result3 = valid_credentials('abcdefghijklmnopqr')
    result4 = valid_credentials('1123oi;saj;oiajw;j')
    assert result1
    assert result2
    assert result3 is False
    assert result4 is False


def test_authenticate_valid():
    access_token = 'f2dOqweIWy65QWlwiw'
    headers = {
        'Authorization': 'Bearer {}'.format(access_token),
        'client_id': 1,
        'name': 'testdoc'
    }
    token = headers.get('Authorization')
    token = token.split()[1]
    assert valid_credentials(token)


def test_authenticate_invalid():
    access_token = 'arandominvalidtoken'
    headers = {
        'Authorization': 'Bearer {}'.format(access_token),
        'client_id': 1,
        'name': 'testdoc'
    }
    token = headers.get('Authorization')
    token = token.split()[1]
    assert valid_credentials(token) is False
