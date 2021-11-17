import database.db as db
# import queue
from documents.document_util import Document_Util


class Document():
    '''
    Intermediate class for operations between the server
    actions and the database operations.
    '''

    def __init__(self, token):
        '''
        Initialize a Document with a developer API token
        that dictates which database the Document will connect to.
        '''

        self.token = token

    def load_document(self, document_id, client_id):
        '''
        Return a dictionary containing the document
        information retrieved from the database.
        '''

        client_id = str(client_id)
        meta = db.get_meta(self.token, document_id)
        if type(meta) == str:
            return meta
        doc = db.get_revision(self.token, document_id, meta["curr_revision"])
        if type(doc) == str:
            return doc
        self.__dict_to_attributes(meta, doc)

        if self.__authorize_client(client_id, 'v'):
            return [meta, doc]
        else:
            return [dict.fromkeys(meta), dict.fromkeys(doc, None)]

    def get_most_recent_revision(self) -> str:
        '''returns the current content'''
        return self.content

    def get_revision_by_hash(self, document_id: str, hash: str) -> str:
        '''
        returns a specified revision given
        a document_id and a specific hash
        '''
        return db.get_revision(self.token, document_id, hash)

    def delete_document(self, client_id):
        '''
        Delete this document from the database
        if the given client is authenticated.
        '''

        client_id = str(client_id)
        if self.document_id is None:
            return "ERROR: Document not loaded."
        if self.__authorize_client(client_id, "u"):
            result = db.delete_document(
                self.token,
                self.document_id)
            if result is not None:
                return result
        else:
            return "ERROR: Client does not have user access."
        return "SUCCESS"

    def update_content(self, content, client_id):
        '''
        Update the contents of the document stored in
        the database with a client's contents.
        '''

        client_id = str(client_id)
        if self.document_id is None:
            return "ERROR: Document not loaded."

        if self.__authorize_client(client_id, "u"):
            self.content = Document_Util.update_document(self,
                                                         self.document_id,
                                                         self.content,
                                                         content)
            self.revision_hash = Document_Util.create_hash(self.content)
            result = db.insert_revision(
                self.token, self.document_id,
                self.__convert_to_dict()[1])
            if result is not None:
                return result
        else:
            return "ERROR: Client does not have user access."
        return "SUCCESS"

    def update_meta(self, name, users, viewers, client_id):
        '''
        Update the meta data of the document stored
        in the database with a client's meta data.
        '''

        client_id = str(client_id)
        if self.document_id is None:
            return "ERROR: Document not loaded."

        if self.__authorize_client(client_id, "u"):
            self.name = name
            self.users = users
            self.viewers = viewers
            result = db.update_meta(self.token, self.document_id, self.__convert_to_dict()[0])
            if result is not None:
                return result
        return "SUCCESS"

    def create_document(self, name, client_id):
        '''
        Creates a new document with a given
        name in the document database.
        '''

        client_id = str(client_id)
        self.name = name
        self.revision_hash = Document_Util.create_hash("")
        self.users = [client_id]
        self.viewers = [client_id]
        self.content = ""
        document_id = db.create_document(
            self.token,
            self.__convert_to_dict()[0], self.__convert_to_dict()[1])
        if document_id is None:
            return "ERROR: Could not create new document."
        self.document_id = document_id
        return document_id

    def __authorize_client(self, client_id, mode):
        if mode == "u":
            return (client_id in self.users)
        elif mode == "v":
            return (client_id in self.viewers)
        return False

    def __convert_to_dict(self):
        '''Private method to convert class attributes to a dict'''
        return [{'document_id': self.document_id,
                'curr_revision': self.revision_hash,
                'name': self.name,
                'users': self.users,
                "viewers": self.viewers}, {'content': self.content,
                                           'revision_hash': self.revision_hash}]

    def __dict_to_attributes(self, meta, doc):
        '''Private method to convert a dict to class attributes'''
        self.document_id = meta["document_id"]
        self.name = meta["name"]
        self.content = doc["content"]
        self.revision_hash = doc["revision_hash"]
        self.users = meta["users"]
        self.viewers = meta["viewers"]

    document_id = None
    name = None
    content = None
    revision_hash = None
    users = None
    viewers = None
    token = None
