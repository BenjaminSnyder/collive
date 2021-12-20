from tinydb import TinyDB, Query


def r_pack(revision):
    revision["type"] = "revision"
    return revision


def m_pack(meta):
    meta["type"] = "meta"
    return meta


def unpack(data):
    del data["type"]
    return data


def open_database(token) -> TinyDB:
    '''opens a database connection'''
    db = TinyDB(token + ".json")
    return db


def open_document(token, doc_id):
    '''creates a new database table for a document by id'''
    db = open_database(token)
    t = db.table(str(doc_id))
    return t


def create_document(token, meta, revision):
    '''creates a new document given a token, metadata and intial revision'''
    db = open_database(token)
    m_id = len(db.tables())
    meta["document_id"] = str(m_id)
    t = db.table(str(m_id))

    t.insert(m_pack(meta))
    t.insert(r_pack(revision))
    return meta


def insert_revision(token, doc_id, revision):
    '''inserts a revision(rev[hash] = content) into a document by id'''
    doc = open_document(token, doc_id)
    if(len(doc) == 0):
        return error("EEXIST", doc_id)

    Rev = Query()
    if(doc.contains(Rev["revision_hash"] == revision["revision_hash"])):
        return ({"type": "warning", "msg": f"{doc_id} "
                 "<{revision['revision_hash']} >"
                 "is identical to the revision. No changes were made."})
    doc.insert(r_pack(revision))
    return revision


def update_meta(token, doc_id, meta):
    '''updates document meta data'''
    doc = open_document(token, doc_id)
    if(len(doc) == 0):
        return error("EEXIST", doc_id)

    Q = Query()
    m = doc.get(Q.type == "meta")
    doc.remove(doc_ids=[m.doc_id])
    doc.insert(m_pack(meta))
    return meta


def get_revision(token, doc_id, revision_hash):
    '''returns a document revision by hash '''
    doc = open_document(token, doc_id)
    if(len(doc) == 0):
        return error("EEXIST", doc_id)

    Rev = Query()
    try:
        revision = doc.search(Rev["revision_hash"] == revision_hash)[0]
        return revision

    except IndexError:
        return error("EDNE", f"{doc_id}: {revision_hash}")


def get_meta(token, doc_id):
    '''returns metadata for a document'''
    doc = open_document(token, doc_id)
    if(len(doc) == 0):
        return error("EEXIST", doc_id)

    Q = Query()
    meta = doc.search(Q["type"] == "meta")[0]
    return meta


def delete_document(token, doc_id):
    '''deletes a document by id'''
    db = open_database(token)
    if(doc_id in db.tables()):
        db.drop_table(str(doc_id))
        return {"type": "success", "msg": f"Deleted document with id {doc_id}"}
    return error("EEXIST", doc_id)


def error(type, arg):
    msg = ""
    if type == "ENOTLOAD":
        msg = "Document not loaded"
    elif type == "EDNE":
        msg = f"Document with id {arg} does not exist"
    elif type == "EEXIST":
        msg = (f"Document {arg} is identical to the revision. "
               "No changes were made.")
    elif type == "EACCESS":
        msg = f"Client does not have user access to doc_id: {arg}."

    return {"type": "error", "code": type, "msg": msg}
