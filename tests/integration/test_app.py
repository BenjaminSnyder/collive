import pytest
import os
from urllib.parse import urlparse
from convertapi.exceptions import ApiError

from app import app

TOKEN = 'Bearer testtoken1'
TOKEN2 = 'Bearer testtoken2'


@pytest.fixture()
def client():
    app.config.from_mapping(SECRET_KEY='dev', TESTING=True, DEBUG=True)

    with app.test_client() as client:
        '''
        Before each test case,
        create a document with doc_id = 0,
        client_id = 1 and name = initdoc
        '''

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
    assert rv.get_json()['document_id'] == '1'


def test_update_and_get_doc(client):
    headers = {'Authorization': TOKEN}
    data = dict(client_id='1', doc_id='0', content='Document update!')
    rv = client.post('/document/update', json=data, headers=headers)
    assert rv.status_code == 200
    assert rv.get_json()['type'] == 'meta'

    params = dict(doc_id=0, client_id=1)
    rv = client.get('/document/get', query_string=params, headers=headers)
    json_data = rv.get_json()
    assert rv.status_code == 200
    assert json_data[1]['content'] == 'Document update!'


def test_delete_doc(client):
    headers = {'Authorization': TOKEN}
    data = dict(doc_id='0', client_id='1')
    rv = client.post('/document/delete', json=data, headers=headers)
    print(rv.data)
    assert rv.status_code == 200
    assert rv.data == b'{\n  "msg": "Deleted document with id 0", \n  "type": "success"\n}\n'


def test_share(client):
    headers = {'Authorization': TOKEN}
    data = dict(client_id='1', doc_id='0', new_doc_users=['client22'], new_doc_viewers=['client23'])
    rv = client.post('/document/share', json=data, headers=headers)
    js = rv.get_json()
    assert rv.status_code == 200
    assert js['type'] == 'meta'
    assert js['document_id'] == '0'
    assert 'client22' in js['users']
    assert 'client23' in js['viewers']


def test_delete_doc_invalid_inputs(client):
    headers = {'Authorization': TOKEN}
    data = dict(client_id='1')
    rv = client.post('/document/delete', json=data, headers=headers)

    assert rv.status_code == 400
    assert rv.data == b'{\n  "msg": "doc_id parameter missing", \n  "type": "error"\n}\n'

    data = dict(doc_id='-1', client_id='1')
    rv = client.post('/document/delete', json=data, headers=headers)

    assert rv.status_code == 404
    assert rv.data == b'{\n  "code": "ENOTLOAD", \n  "msg": "Document not loaded", \n  "type": "error"\n}\n'

    data = dict(doc_id='0', client_id='-1')
    rv = client.post('/document/delete', json=data, headers=headers)

    assert rv.status_code == 403
    assert rv.data == b'{\n  "code": "EACCESS", \n  "msg": "Client does not have user access to doc_id: 0.", \n  "type": "error"\n}\n'


def test_create_doc_invalid_inputs(client):
    data = {"client_id": 1, "name": "doc2"}
    headers = {'Authorization': TOKEN}
    rv = client.post('/document/create', json=data, headers=headers)

    assert rv.status_code == 400
    assert rv.get_json()['msg'] == 'client_id must be of type string'
    assert rv.get_json()['type'] == 'error'


def test_update_doc_invalid_inputs(client):
    data = {"doc_id": "", "client_id": "1", "content": "test content"}
    headers = {'Authorization': TOKEN}
    rv = client.post('/document/update', json=data, headers=headers)

    assert rv.status_code == 400
    assert rv.get_json()['msg'] == 'doc_id cannot be an empty string'
    assert rv.get_json()['type'] == 'error'

    data = {"doc_id": "-1", "client_id": "1", "content": "test content"}
    rv = client.post('/document/update', json=data, headers=headers)

    assert rv.status_code == 404
    assert rv.get_json()['type'] == 'error'

    data = {"doc_id": "0", "client_id": "-1", "content": "test content"}
    rv = client.post('/document/update', json=data, headers=headers)

    assert rv.status_code == 403
    assert rv.get_json()['msg'] == 'Client does not have user access to doc_id: 0.'
    assert rv.get_json()['type'] == 'error'


def test_get_doc_invalid_inputs(client):
    params = dict(client_id=0)
    headers = {'Authorization': TOKEN}
    rv = client.get('/document/get', query_string=params, headers=headers)

    assert rv.status_code == 400
    assert rv.data == b'{\n  "msg": "doc_id parameter missing", \n  "type": "error"\n}\n'

    params = dict(doc_id=0)
    rv = client.get('/document/get', query_string=params, headers=headers)

    assert rv.status_code == 400
    assert rv.data == b'{\n  "msg": "client_id parameter missing", \n  "type": "error"\n}\n'

    params = dict(doc_id=-1, client_id=0)
    rv = client.get('/document/get', query_string=params, headers=headers)
    assert rv.status_code == 404
    assert rv.data == b'{\n  "code": "ENOTLOAD", \n  "msg": "Document not loaded", \n  "type": "error"\n}\n'

    params = dict(doc_id=0, client_id=-1)
    rv = client.get('/document/get', query_string=params, headers=headers)

    assert rv.status_code == 403
    assert rv.data == b'{\n  "code": "EACCESS", \n  "msg": "Client does not have user access to doc_id: 0.", \n  "type": "error"\n}\n'


def test_export_pdf(client):
    params = dict(doc_id="0", client_id="1")
    headers = {'Authorization': TOKEN}
    with pytest.raises(ApiError):
        rv = client.get('/document/export/pdf', query_string=params, headers=headers)

        url = rv.get_json['url']
        assert rv.status_code == 401
        assert urlparse(url).hostname == 'v2.convertapi.com'

    headers = {'Authorization': os.environ.get('CONVERT_API_SECRET')}
    rv = client.get('/document/export/pdf', query_string=params, headers=headers)
    assert rv.status_code == 200

