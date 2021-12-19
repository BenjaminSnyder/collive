from documents.document import Document
import pytest  # noqa


def test_load_document():
    doc = Document("test")
    create_meta = doc.create_document("load_doc.txt", "client")
    _ = doc.update_content("This is a doc to load", "client")
    doc = Document("test")
    dictionaries = doc.load_document(create_meta["document_id"], "client")
    meta = dictionaries[0]
    rev = dictionaries[1]
    assert meta["document_id"] == create_meta["document_id"]
    assert rev["revision_hash"] == doc.revision_hash
    assert meta["name"] == "load_doc.txt"
    assert rev["content"] == "This is a doc to load"

    create_meta = doc.create_document("load_doc2.txt", "client1")
    doc = Document("test")
    dictionaries = doc.load_document(create_meta["document_id"], "client1")
    meta = dictionaries[0]
    rev = dictionaries[1]
    assert meta["document_id"] == create_meta["document_id"]
    assert rev["revision_hash"] == doc.revision_hash
    assert meta["name"] == "load_doc2.txt"
    assert rev["content"] == ""
    assert meta["viewers"] == ["client1"]
    assert meta["users"] == ["client1"]

    dictionaries = doc.load_document("error_doc", "client")
    dictionary = dictionaries[0]
    assert dictionary["type"] == "error"

    dictionary = doc.load_document(create_meta["document_id"], "client222")
    assert dictionary[1]["type"] =="error"
    _ = doc.delete_document("client")


def test_get_most_recent_revision():
    doc = Document("test")
    assert doc.get_most_recent_revision() is None
    doc.content = "content"
    assert doc.get_most_recent_revision() == "content"


def test_get_revision_by_hash():
    doc = Document("test")
    create_meta = doc.create_document("rev_doc.txt", "client")
    _ = doc.update_content("This is a doc to rev", "client")
    dictionary = doc.get_revision_by_hash(
        create_meta["document_id"], doc.revision_hash)
    assert dictionary["revision_hash"] == doc.revision_hash
    assert dictionary["content"] == "This is a doc to rev"

    response = doc.get_revision_by_hash("docyError", "error")
    assert response['type'] == "error"
    assert response["code"] == "EEXIST"
    assert response["msg"] == (f"Document docyError is identical to the revision. "
                               "No changes were made.")

    response = doc.get_revision_by_hash(create_meta["document_id"], "error")
    assert response['type'] == "error"
    assert response["code"] == "EDNE"
    assert response["msg"] == f"Document with id {create_meta['document_id']}: error does not exist"


def test_delete_document():
    doc = Document("test")
    response = doc.delete_document("client")
    assert response['type'] == "error"
    assert response["code"] == "ENOTLOAD"
    assert response["msg"] == "Document not loaded"

    create_meta = doc.create_document('delete_doc.txt', "client")
    response = doc.update_content("This is a doc to delete", "client")
    dictionaries = doc.load_document(create_meta["document_id"], "client")

    response = doc.delete_document("client2")
    assert response["type"] == "error"
    assert response["code"] == "EACCESS"
    assert response["msg"] == f"Client does not have user access to doc_id: {doc.document_id}."

    response = doc.delete_document("client")
    assert response["type"] == "success"
    assert response["msg"] == f"Deleted document with id {create_meta['document_id']}"

    dictionaries = doc.load_document(create_meta["document_id"], "client")
    assert dictionaries[1]["type"] == "error"

    response = doc.delete_document("client")
    assert response["type"] == "error"
    assert response["code"] == "EEXIST"
    assert response["msg"] == f"Document {doc.document_id} is identical to the revision. No changes were made."


def test_update_content():
    doc = Document("test")
    response = doc.update_content("This is a doc to error", "client")
    assert response['type'] == "error"
    assert response["code"] == "ENOTLOAD"
    assert response["msg"] == "Document not loaded"

    create_meta = doc.create_document("update_doc.txt", "client")
    doc = Document("test")
    dictionaries = doc.load_document(create_meta["document_id"], "client")
    response = doc.update_content("This is a doc to update", "client")
    assert doc.content == "This is a doc to update"

    dictionaries = doc.load_document(create_meta["document_id"], "client")
    meta = dictionaries[0]
    rev = dictionaries[1]
    revision_hash = doc.revision_hash
    assert meta["document_id"] == create_meta["document_id"]
    assert rev["revision_hash"] == doc.revision_hash
    assert rev["content"] == "This is a doc to update"

    response = doc.update_content(
        "This is a doc to update version 2", "client")
    assert doc.content == "This is a doc to update version 2"
    assert doc.document_id == create_meta["document_id"]
    assert doc.revision_hash != revision_hash

    response = doc.update_content(
        "This is a doc to update unauthorized", "client123")
    assert response["type"] == "error"
    assert response["code"] == "EACCESS"
    assert response["msg"] == f"Client does not have user access to doc_id: {doc.document_id}."

    response = doc.delete_document("update_doc.txt")


def test_update_meta():
    doc = Document("test")
    response = doc.update_meta("newName.txt", ["client", "client2"],
                               ["client", "client2"], "client")
    assert response['type'] == "error"
    assert response["code"] == "ENOTLOAD"
    assert response["msg"] == "Document not loaded"

    create_meta = doc.create_document("update_doc.txt", "client")
    dictionaries = doc.load_document(create_meta["document_id"], "client")
    response = doc.update_meta("newName.txt", ["client", "client2"],
                               ["client", "client2"], "client")
    assert response["document_id"] == create_meta["document_id"]

    dictionaries = doc.load_document(create_meta["document_id"], "client")

    meta = dictionaries[0]
    rev = dictionaries[1]
    old_revision = doc.revision_hash
    assert meta["document_id"] == create_meta["document_id"]
    assert rev["revision_hash"] == doc.revision_hash
    assert meta["name"] == "newName.txt"
    assert meta["users"][0] == "client"
    assert meta["users"][1] == "client2"
    assert meta["viewers"][0] == "client"
    assert meta["viewers"][1] == "client2"

    response = doc.update_meta("newName2.txt", ["client3", "client4"],
                               ["client3", "client4"], "client")
    assert response["document_id"] == create_meta["document_id"]
    assert doc.document_id == create_meta["document_id"]
    assert doc.revision_hash == old_revision
    assert doc.name == "newName2.txt"

    assert doc.viewers[0] == "client3"
    assert doc.viewers[1] == "client4"
    assert doc.users[0] == "client3"
    assert doc.users[1] == "client4"

    response = doc.update_meta("This is a doc to update unauthorized", ["client3", "client4"],
                               ["client3", "client4"], "client123")
    assert response["type"] == "error"
    assert response["code"] == "EACCESS"
    print(response['msg'])
    assert response["msg"] == f"Client does not have user access to doc_id: {doc.document_id}."

    _ = doc.delete_document("client3")


def test_create_document():
    doc = Document("test")
    meta = doc.create_document("create_doc.txt", "client")
    assert meta["document_id"] is not None
    _ = doc.load_document(meta["document_id"], "client")
    response = doc.update_content(
        "This is a a doc to update", "client")
    assert response["document_id"] == meta["document_id"]
    _ = doc.delete_document("client")
