from documents.document import Document
import pytest
def test_load_document():
    doc = Document("test")
    doc_id = doc.create_document()
    response = doc.update_content("load_doc.txt", "This is a a doc to load")
    doc = Document("test")
    dictionary = doc.load_document(doc_id)
    assert dictionary["document_id"] == doc_id
    assert dictionary["revision"] == "1"
    assert dictionary["name"] == "load_doc.txt"
    assert dictionary["content"] == "This is a doc to load"

    dictionary = doc.load_document("error_doc")
    assert dictionary["document_id"] == None
    assert dictionary["revision"] == None
    assert dictionary["name"] == None
    assert dictionary["content"] == None
    response = doc.delete_document(doc_id)

def test_delete_document():
    doc = Document("test")
    doc_id = doc.create_document()
    response = doc.update_content("delete_doc.txt", "This is a a doc to delete")
    response = doc.delete_document(doc_id)
    assert response == "SUCCESS"
    dictionary = doc.load_document(doc_id)
    assert dictionary["document_id"] == None
    assert dictionary["revision"] == None
    assert dictionary["name"] == None
    assert dictionary["content"] == None

    response = doc.delete_document("error_doc")
    assert response == "ERROR: Document does not exist."

def test_update_content():
    doc = Document("test")
    response = doc.update_content("delete_doc.txt", "This is a a doc to delete")
    assert response == "ERROR: Document not loaded."

    doc_id = doc.create_document()
    dictionary = doc.load_document(doc_id)
    response = doc.update_content("update_doc.txt", "This is a a doc to update")
    assert response == "SUCCESS"

    dictionary = doc.load_document(doc_id)

    assert dictionary["document_id"] == doc_id
    assert dictionary["revision"] == "1"
    assert dictionary["name"] == "update_doc_txt"
    assert dictionary["content"] == "This is a doc to update"

    response = doc.update_content("update_doc.txt", "This is a a doc to update version 2")
    assert response == "SUCCESS"
    assert dictionary["document_id"] == doc_id
    assert dictionary["revision"] == "2"
    assert dictionary["name"] == "update_doc_txt"
    assert dictionary["content"] == "This is a doc to update verion 2"

    response = doc.update_content("error_doc")
    assert response == "ERROR: Document does not exist"
    response = doc.delete_document("update_doc.txt")

def test_create_document():
    doc = Document("test")
    response = doc.create_document()
    assert response != "ERROR: Could not crate new document."
    doc_id = doc.create_document()
    dictionary = doc.load_document(doc_id)
    response = doc.update_content("update_doc.txt", "This is a a doc to update")
    assert response == "SUCCESS"

    dictionary = doc.load_document(doc_id)

    assert dictionary["document_id"] == doc_id
    assert dictionary["revision"] == "1"
    assert dictionary["name"] == "update_doc_txt"
    assert dictionary["content"] == "This is a doc to update"

    response = doc.update_content("update_doc.txt", "This is a a doc to update version 2")
    assert response == "SUCCESS"
    assert dictionary["document_id"] == doc_id
    assert dictionary["revision"] == "2"
    assert dictionary["name"] == "update_doc_txt"
    assert dictionary["content"] == "This is a doc to update verion 2"

    response = doc.update_content("error_doc")
    assert response == "ERROR: Document does not exist"
    