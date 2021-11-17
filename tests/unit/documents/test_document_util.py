import pytest  # noqa
from documents.document_util import Document_Util


hashify_url = 'http://api.hashify.net/hash/md5/hex'


def test_create_hash(requests_mock):
    test_id = 'valid string'  # noqa
    requests_mock.get(f'{hashify_url}?value=1234beforeHashed',
                      json={'Digest': '1234'})
    result = Document_Util.create_hash("1234beforeHashed")
    expected = '1234'
    assert expected == result


def test_empty_string(requests_mock):
    test_id = 'empty string'  # noqa
    requests_mock.get(f'{hashify_url}?value=',
                      json={'Digest': 'd41d8cd98f00b204e9800998ecf8427e'})
    results = Document_Util.create_hash('')
    expected = 'd41d8cd98f00b204e9800998ecf8427e'
    assert expected == results


def test_error(requests_mock):
    test_id = 'empty string'  # noqa
    requests_mock.get(f'{hashify_url}?value=somecontent',
                      json={'status': 404})
    results = Document_Util.create_hash('somecontent')
    expected = Exception("There was an error with the Hashify API")
    assert type(expected) is type(results) and expected.args == results.args


def test_update_document(mocker):
    test_id = 'update document'  # noqa
    mock_doc = mocker.MagicMock()
    mock_doc.get_revision_by_hash.return_value = 'somecontent'
    mock_doc.get_lastest_revision.return_value = 'somecontent'

    results = Document_Util.update_document(
        mock_doc, 'somedocid', 'somehash', 'somechangedcontent')

    expected = 'somechangedcontent'
    assert results == expected
