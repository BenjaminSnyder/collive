from tinydb import TinyDB, Query
db = TinyDB('db.json')


class Database():
    def __init__(self, devID):
        self.docs = TinyDB(devID + '/docs.json')

    def create_document(self, doc):
        doc["documentID"] = len(self.docs) + 1
        self.docs.insert(doc)

    def insert_document(self, doc):
        Doc = Query()
        if(self.docs.contains((Doc.document_id == doc["documentID"])
           and (Doc["revisionID"] == doc["revisionID"]))):
            return ("Error: Document" + doc["documentID"] + ":" +
                    doc["revisionID"] + " already exists.")
        else:
            self.docs.insert(doc)

    def get_document(self, doc):
        Doc = Query()
        try:
            revisions = self.docs.search(
                Doc["documentID"] == doc["documentID"])
            return max(
                revisions, key=lambda x: x['revisionID'])

        except IndexError:
            return ("Error: No document with ID:" + doc["documentID"])

    def delete_document(self, doc):
        Doc = Query()
        if(self.docs.contains(Doc["documentID"] == doc["documentID"])):
            self.docs.remove(Doc["documentID"] == doc["documentID"])
        else:
            return ("Document" + doc["documentID"] + "not found.")

