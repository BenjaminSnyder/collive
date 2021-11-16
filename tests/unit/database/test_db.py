import database.db as db
import pytest


def test_create_insert_and_get():
    meta = {'document_id': "",
            'curr_revision': "",
            'name': "test document",
            'users': ["test_user1", "test_user2"],
            'viewers': ["test_user1", "test_user2"]}
    rev = {'revision_hash': "1111",
           'content': "test document contents"}

    token = "token"

    db.open_database(token)
    db.create_document(token, meta, rev)

    meta["name"] = "test document 2"
    rev["content"] = "second test document"
    doc_id = db.create_document(token, meta, rev)

    rev["revision_hash"] = "2222"
    rev["content"] = "second document, rev 2"
    db.insert_revision(token, doc_id, rev)

    meta["name"] = "test document 3"
    rev["content"] = "third test document"
    db.create_document(token, meta, rev)

    rev["revision_hash"] = "3333"
    rev["content"] = "second document, rev 3"
    db.insert_revision(token, doc_id, rev)

    meta = db.get_meta(token, doc_id)
    rev = db.get_revision(token, doc_id, 3333)

    assert meta["document_id"] == doc_id
    assert meta["name"] == "test document 2"
    assert rev["revision_hash"] == "3333"
