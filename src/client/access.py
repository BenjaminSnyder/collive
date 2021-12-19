from tinydb import TinyDB, Query


def open_access_database() -> TinyDB:
    '''opens a database connection'''
    db = TinyDB('access.json')
    return db


def add_doc(username, document):
    db = open_access_database()
    if isinstance(username, str) and isinstance(document, str):
        user = Query()
        current_access = return_access(username)
        current_access.append(document)
        current_access = list(set(current_access))
        current_access.sort()
        db.upsert({'username': username, 'documents': current_access}, user.username == username)


def update_access(username, documents):
    '''adds (or updates) username/documents pair to database'''
    documents = list(set(documents))
    documents.sort()
    db = open_access_database()
    if isinstance(username, str) and isinstance(documents, list):
        user = Query()
        db.upsert({'username': username, 'documents': documents}, user.username == username)


def return_access(username):
    '''returns list of documents a user has access to'''
    db = open_access_database()
    if isinstance(username, str):
        user = Query()
        pair = db.search(user['username'] == username)
        if not pair:
            return []
        else:
            return pair[0]['documents']
