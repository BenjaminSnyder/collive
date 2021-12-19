from tinydb import TinyDB, Query


def open_doc_id_database() -> TinyDB:
    '''opens a database connection'''
    db = TinyDB('doc_id.json')
    return db


def update_doc_name(doc_id, doc_name):
    '''adds (or updates) doc_id/doc_name pair to database'''
    db = open_doc_id_database()
    if isinstance(doc_id, str) and isinstance(doc_name, str):
        doc = Query()
        db.upsert({'doc_id': doc_id, 'doc_name': doc_name}, doc.doc_id == doc_id)


def return_doc_name(doc_id):
    '''returns name of document corresponding to provided doc_id'''
    db = open_doc_id_database()
    if isinstance(doc_id, str):
        doc = Query()
        result = db.search(doc['doc_id'] == doc_id)
        name = None
        if result:
            name = result[0]['doc_name']
        if not name:
            return None
        else:
            return name
