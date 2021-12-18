import pytest
import os

from app import app

TOKEN = 'Bearer testtoken1'
TOKEN2 = 'Bearer testtoken2'


@pytest.fixture()
def client():
    app.config.from_mapping(SECRET_KEY='dev', TESTING=True, DEBUG=True)

    with app.test_client() as client:
        data = {"client_id": '1', "name": "initdoc"}
        headers = {'Authorization': TOKEN}
        client.post('/document/create', json=data, headers=headers)
        yield client

    db_name = TOKEN + '.json'
    os.remove(db_name)


def test_create_doc(client):
    data = {"client_id": '1', "name": "doc2"}
    headers = {'Authorization': TOKEN}
    rv = client.post('/document/create', json=data, headers=headers)
    assert rv.status_code == 200
    assert rv.data == b'1'


def test_update_and_get_doc(client):
    headers = {'Authorization': TOKEN}
    data = dict(client_id='1', doc_id='0', content='Document update!')
    rv = client.post('/document/update', json=data, headers=headers)
    assert rv.status_code == 200
    assert rv.data == b'SUCCESS'

    params = dict(doc_id=0, client_id=1)
    rv = client.get('/document/get', query_string=params, headers=headers)
    json_data = rv.get_json()
    assert rv.status_code == 200
    assert json_data[1]['content'] == 'Document update!'


'''
def test_delete_doc(client):
    headers = {'Authorization': TOKEN}
    data = dict(client_id='0', doc_id='0')
    rv = client.post('/document/delete', json=data, headers=headers)
'''


def test_create_doc_invalid_inputs(client):
    data = {"client_id": 1, "name": "doc2"}
    headers = {'Authorization': TOKEN}
    rv = client.post('/document/create', json=data, headers=headers)

    assert rv.status_code == 400
    assert rv.data == b'ERROR: client_id must be of type string'

    data = {"client_id": "1"}
    headers = {'Authorization': TOKEN}
    rv = client.post('/document/create', json=data, headers=headers)

    assert rv.status_code == 400
    assert rv.data == b'ERROR: name parameter missing'


def test_update_doc_invalid_inputs(client):
    data = {"doc_id": "", "client_id": "1", "content": "test content"}
    headers = {'Authorization': TOKEN}
    rv = client.post('/document/update', json=data, headers=headers)

    assert rv.status_code == 400
    assert rv.data == b'ERROR: doc_id cannot be an empty string'
    
    data = {"doc_id": "-1", "client_id": "1", "content": "test content"}
    headers = {'Authorization': TOKEN}
    rv = client.post('/document/update', json=data, headers=headers)

    assert rv.status_code == 404
    assert rv.data == b'ERROR: no document with id: -1'

    data = {"doc_id": "0", "client_id": "-1", "content": "test content"}
    headers = {'Authorization': TOKEN}
    rv = client.post('/document/update', json=data, headers=headers)

    assert rv.status_code == 403
    assert rv.data == b'ERROR: client does not have access to doc_id 0'


def test_get_doc_invalid_inputs(client):
    params = dict(client_id=0)
    headers = {'Authorization': TOKEN}
    rv = client.get('/document/get', query_string=params, headers=headers)

    assert rv.status_code == 400
    assert rv.data == b'ERROR: doc_id parameter missing'

    params = dict(doc_id=0)
    headers = {'Authorization': TOKEN}
    rv = client.get('/document/get', query_string=params, headers=headers)

    assert rv.status_code == 400
    assert rv.data == b'ERROR: client_id parameter missing'

    params = dict(doc_id = -1, client_id = 0)
    headers = {'Authorization': TOKEN}
    rv = client.get('/document/get', query_string=params, headers=headers)

    assert rv.status_code == 404
    assert rv.data == b'ERROR: no document with id: -1'

    params = dict(doc_id=0, client_id = -1)
    headers = {'Authorization': TOKEN}
    rv = client.get('/document/get', query_string=params, headers=headers)

    assert rv.status_code == 403
    assert rv.data == b'ERROR: client does not have access to doc_id 0'
