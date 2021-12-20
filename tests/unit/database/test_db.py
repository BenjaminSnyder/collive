import database.db as db
import pytest  # noqa


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
    create_meta = db.create_document(token, meta, rev)

    rev["revision_hash"] = "2222"
    rev["content"] = "second document, rev 2"
    db.insert_revision(token, create_meta["document_id"], rev)

    meta["name"] = "test document 3"
    rev["content"] = "third test document"

    meta["users"].append("xyz_user")
    db.create_document(token, meta, rev)

    rev["revision_hash"] = "3333"
    rev["content"] = "second document, rev 3"
    db.insert_revision(token, create_meta["document_id"], rev)

    meta = db.get_meta(token, create_meta["document_id"])
    rev = db.get_revision(token, create_meta["document_id"], "3333")
    assert meta["document_id"] == create_meta["document_id"]
    assert meta["name"] == "test document 3"
    assert rev["revision_hash"] == "3333"
    assert rev["content"] == "second document, rev 3"

    test = db.get_user_documents(token, "xyz_user")
    highest = -1
    for doc in test["documents"]:
        highest = max(int(doc['document_id']), highest)
    assert str(highest) == create_meta["document_id"]


def test_delete():
    meta = {'document_id': "",
            'curr_revision': "",
            'name': "test document Delete",
            'users': ["test_user1", "test_user2"],
            'viewers': ["test_user1", "test_user2"]}
    rev = {'revision_hash': "1111",
           'content': "test document contents"}

    token = "token"
    db.open_database(token)
    create_meta = db.create_document(token, meta, rev)
    meta = db.get_meta(token, create_meta["document_id"])
    rev = db.get_revision(token, create_meta["document_id"], "1111")
    assert meta["type"] != "error"
    assert rev["type"] != "error"

    result = db.delete_document(token, create_meta["document_id"])
    assert result["type"] == "success"

    meta = db.get_meta(token, create_meta["document_id"])
    assert meta["type"] == "error"


def test_error():
    error = db.error("ENOTLOAD", None)
    assert error["type"] == "error"
    assert error["code"] == "ENOTLOAD"
    assert error["msg"] == "Document not loaded"

    error = db.error("EDNE", "er")
    assert error["type"] == "error"
    assert error["code"] == "EDNE"
    assert error["msg"] == "Document with id er does not exist"

    error = db.error("EEXIST", "er")
    assert error["type"] == "error"
    assert error["code"] == "EEXIST"
    assert error["msg"] == ("Document er is identical to the revision. "
                            "No changes were made.")

    error = db.error("EACCESS", "er")
    assert error["type"] == "error"
    assert error["code"] == "EACCESS"
    assert error["msg"] == "Client does not have user access to doc_id: er."
