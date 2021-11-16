from documents.document import Document
import pytest # noqa


def test_load_document():
    doc = Document("test")
    doc_id = doc.create_document("load_doc.txt", "client")
    _ = doc.update_content("This is a doc to load", "client")
    doc = Document("test")
    dictionaries = doc.load_document(doc_id, "client")
    print(dictionaries)
    meta = dictionaries[0]
    rev = dictionaries[1]
    assert meta["document_id"] == doc_id
    assert rev["revision_hash"] == doc.revision_hash
    assert meta["name"] == "load_doc.txt"
    assert rev["content"] == "This is a doc to load"

    dictionary = doc.load_document("error_doc", "client")
    assert dictionary  == "Error, no document with id: error_doc"
    _ = doc.delete_document("client")


def test_get_most_recent_revision():
    doc = Document("test")
    assert doc.get_most_recent_revision() is None
    doc.content = "content"
    assert doc.get_most_recent_revision() == "content"


def test_get_revision_by_hash():
    doc = Document("test")
    doc_id = doc.create_document("rev_doc.txt", "client")
    _ = doc.update_content("This is a doc to rev", "client")
    dictionary = doc.get_revision_by_hash(doc_id, doc.revision_hash)
    assert dictionary["revision_hash"] == doc.revision_hash
    assert dictionary["content"] == "This is a doc to rev"


def test_delete_document():
    doc = Document("test")
    response = doc.delete_document("client")
    assert response == "ERROR: Document not loaded."

    doc_id = doc.create_document('delete_doc.txt', "client")
    response = doc.update_content("This is a doc to delete", "client")
    dictionaries = doc.load_document(doc_id, "client")
    response = doc.delete_document("client")
    assert response == "SUCCESS"

    dictionaries = doc.load_document(doc_id, "client")
    assert dictionaries == "Error, no document with id: " + doc_id

    response = doc.delete_document("client")
    assert response == "SUCCESS"

    


def test_update_content():
    doc = Document("test")
    response = doc.update_content("This is a doc to error", "client")
    assert response == "ERROR: Document not loaded."

    doc_id = doc.create_document("update_doc.txt", "client")
    dictionaries = doc.load_document(doc_id, "client")
    response = doc.update_content("This is a doc to update", "client")
    assert response == "SUCCESS"

    dictionaries = doc.load_document(doc_id, "client")
    meta = dictionaries[0]
    rev = dictionaries[1]
    revision_hash = doc.revision_hash
    assert meta["document_id"] == doc_id
    assert rev["revision_hash"] == doc.revision_hash
    assert rev["content"] == "This is a doc to update"

    response = doc.update_content(
        "This is a doc to update version 2", "client")
    assert response == "SUCCESS"
    assert doc.document_id == doc_id
    assert doc.revision_hash != revision_hash
    assert doc.content == "This is a doc to update version 2"
    
    response = doc.delete_document("update_doc.txt")


def test_update_meta():
    doc = Document("test")
    response = doc.update_meta("newName.txt", ["client", "client2"],
                               ["client", "client2"], "client")
    assert response == "ERROR: Document not loaded."

    doc_id = doc.create_document("update_doc.txt", "client")
    dictionaries = doc.load_document(doc_id, "client")
    response = doc.update_meta("newName.txt", ["client", "client2"],
                               ["client", "client2"], "client")
    assert response == "SUCCESS"

    dictionaries = doc.load_document(doc_id, "client")

    meta = dictionaries[0]
    rev = dictionaries[1]
    old_revision = doc.revision_hash
    assert meta["document_id"] == doc_id
    assert rev["revision_hash"] == doc.revision_hash
    assert meta["name"] == "newName.txt"
    assert meta["users"][0] == "client"
    assert meta["users"][1] == "client2"
    assert meta["viewers"][0] == "client"
    assert meta["viewers"][1] == "client2"

    response = doc.update_meta("newName2.txt", ["client3", "client4"],
                               ["client3", "client4"], "client")
    assert response == "SUCCESS"
    assert doc.document_id == doc_id
    assert doc.revision_hash == old_revision
    assert doc.name == "newName2.txt"

    assert doc.viewers[0] == "client3"
    assert doc.viewers[1] == "client4"
    assert doc.users[0] == "client3"
    assert doc.users[1] == "client4"

    response = doc.delete_document("client3")


def test_create_document():
    doc = Document("test")
    doc_id = doc.create_document("create_doc.txt", "client")
    assert doc_id != "ERROR: Could not crate new document."
    _ = doc.load_document(doc_id, "client")
    response = doc.update_content(
        "This is a a doc to update", "client")
    assert response == "SUCCESS"