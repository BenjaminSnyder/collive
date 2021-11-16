from documents.document import Document
import pytest


def test_load_document():
    doc = Document("test")
    doc_id = doc.create_document("load_doc.txt", "client")
    _ = doc.update_content("This is a a doc to load", "client")
    doc = Document("test")
    dictionary = doc.load_document(doc_id, "client")
    assert dictionary["document_id"] == doc_id
    assert dictionary["revision"] == "1"
    assert dictionary["name"] == "load_doc.txt"
    assert dictionary["content"] == "This is a doc to load"

    dictionary = doc.load_document("error_doc", "client")
    assert dictionary is None
    _ = doc.delete_document(doc_id, "client")


def test_get_most_recent_revision():
    doc = Document("test")
    assert doc.get_most_recent_revision() is None
    doc.content = "content"
    assert doc.get_most_recent_revision() == "content"


def test_get_revision_by_hash():
    doc = Document("test")
    doc_id = doc.create_document("rev_doc.txt", "client")
    _ = doc.update_content("This is a a doc to rev", "client")
    dictionary = doc.get_revision_by_hash(doc.revision)
    assert dictionary["document_id"] == doc_id
    assert dictionary["revision"] == doc.revision
    assert dictionary["name"] == "rev_doc.txt"
    assert dictionary["content"] == "This is a doc to rev"


def test_delete_document():
    doc = Document("test")
    doc_id = doc.create_document('delete_doc.txt', "client")
    response = doc.update_content("This is a a doc to delete", "client")
    dictionary = doc.load_document(doc_id, "client")
    response = doc.delete_document("client")
    assert response == "SUCCESS"
    dictionary = doc.load_document(doc_id, "client")
    assert dictionary is None
    response = doc.delete_document("client")
    assert response == "ERROR: Document does not exist."

    response = doc.delete_document("client")
    assert response == "ERROR: Document not loaded."


def test_update_content():
    doc = Document("test")
    response = doc.update_content("This is a a doc to error", "client")
    assert response == "ERROR: Document not loaded."

    doc_id = doc.create_document("update_doc.txt", "client")
    dictionary = doc.load_document(doc_id, "client")
    response = doc.update_content("This is a a doc to update", "client_id")
    assert response == "SUCCESS"

    dictionary = doc.load_document(doc_id, "client")
    rev = doc.revision
    assert dictionary["document_id"] == doc_id
    assert dictionary["revision"] == doc.revision
    assert dictionary["content"] == "This is a doc to update"

    response = doc.update_content(
        "This is a a doc to update version 2", "client")
    assert response == "SUCCESS"
    assert doc.document_id == doc_id
    assert doc.revision != rev
    assert dictionary["content"] == "This is a doc to update verion 2"

    response = doc.update_content("error_doc", "client")
    assert response == "ERROR: Document does not exist"
    response = doc.delete_document("update_doc.txt")


def test_update_meta():
    doc = Document("test")
    response = doc.update_meta("newName.txt", ["client", "client2"],
                               ["client", "client2"], "client")
    assert response == "ERROR: Document not loaded."

    doc_id = doc.create_document("update_doc.txt", "client")
    dictionary = doc.load_document(doc_id, "client")
    response = doc.update_meta("newName.txt", ["client", "client2"],
                               ["client", "client2"], "client")
    assert response == "SUCCESS"

    dictionary = doc.load_document(doc_id, "client")
    rev = doc.revision
    print(dictionary)
    assert dictionary["document_id"] == doc_id
    assert dictionary["revision"] == doc.revision
    assert dictionary["name"] == "newName.txt"
    assert dictionary["users"][0] == "client"
    assert dictionary["users"][1] == "client2"
    assert dictionary["viewers"][0] == "client"
    assert dictionary["viewers"][1] == "client2"

    response = doc.update_meta("newName2.txt", ["client3", "client4"],
                               ["client3", "client4"], "client")
    assert response == "SUCCESS"
    assert doc.document_id == doc_id
    assert doc.revision != rev
    assert dictionary["name"] == "newName2.txt"

    assert dictionary["viewers"][0] == "client3"
    assert dictionary["viewers"][1] == "client4"
    assert dictionary["users"][0] == "client3"
    assert dictionary["users"][1] == "client4"

    response = doc.update_meta("error_doc", "client")
    assert response == "ERROR: Document does not exist"
    response = doc.delete_document("client3")


def test_create_document():
    doc = Document("test")
    doc_id = doc.create_document("create_doc.txt", "client")
    assert doc_id != "ERROR: Could not crate new document."
    dictionary = doc.load_document(doc_id, "client")
    response = doc.update_content(
        "This is a a doc to update", "client")
    assert response == "SUCCESS"