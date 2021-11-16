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
    return "" + str(m_id)


def insert_revision(token, doc_id, revision):
    '''inserts a revision(rev[hash] = content) into a document by id'''
    doc = open_document(token, doc_id)
    if(len(doc) == 0):
        return ("Error, no document with id: " + doc_id)

    Rev = Query()
    if(doc.contains(Rev["revision_hash"] == revision["revision_hash"])):
        return ("Error: Document" + doc_id + "<" +
                revision["revision_hash"] + "> already exists.")
    else:
        doc.insert(r_pack(revision))


def get_revision(token, doc_id, revision_hash):
    '''returns a document revision by hash '''
    doc = open_document(token, doc_id)
    if(len(doc) == 0):
        return ("Error, no document with id: " + str(doc_id))

    Rev = Query()
    try:
        revision = doc.search(Rev["revision_hash"] == revision_hash)[0]
        return unpack(revision)

    except IndexError:
        return ("Error: No revision with hash:" + revision_hash)


def update_meta(token, doc_id, meta):
    '''updates document meta data'''
    doc = open_document(token, doc_id)
    if(len(doc) == 0):
        return ("Error, no document with id: " + str(doc_id))

    Q = Query()
    m = doc.get(Q.type == "meta")
    doc.remove(doc_ids=m.doc_id)
    doc.insert(m_pack(meta))


def get_meta(token, doc_id):
    '''returns metadata for a document'''
    doc = open_document(token, doc_id)
    if(len(doc) == 0):
        return ("Error, no document with id: " + str(doc_id))

    Q = Query()
    meta = doc.search(Q["type"] == "meta")[0]
    return unpack(meta)


def delete_document(token, doc_id):
    '''deletes a document by id'''
    db = open_database(token)
    db.drop_table(str(doc_id))
