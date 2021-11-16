from database.db import Database
import queue
from documents.diff import doc_util

class Document():
    '''Intermediate class for operations between the server actions and the database operations.'''

    def __init__(self, token):
        '''Initialize a Document with a developer API token that dictates which database the Document will
        connect to.
        '''

        self.token = token

    def load_document(self, document_id, client_id):
        '''Return a dictionary containing the document information retrieved from the database.'''

        doc = Database.get_document(self.token, document_id)
        if self.__authorize_client(doc, client_id, 'v'):
            self.__dict_to_attributes(doc)
            return doc
        else:
            return dict.fromkeys(doc, None)

    def delete_document(self, client_id):
        '''Delete this document from the database if the given client is authenticated.'''

        if self.document_id is None:
            return "ERROR: Document not loaded."
        if self.__authorize_client(client_id, "u"):
            result = Database.delete_document(self.token, self.__convert_to_dict())
            if result is not None:
                return result
        else:
            return "ERROR: Client does not have user access."
        return "SUCCESS"

    def update_content(self, content, client_id):
        '''Update the contents of the document stored in the database with a client's contents.'''

        if self.document_id is None:
            return "ERROR: Document not loaded."

        if self.__authorize_client(client_id, "u"):
            self.content = content
            self.revision = doc_util.create_hash(content)
            result = Database.insert_content(self.token, self.__convert_to_dict()[1])
            if result is not None:
                return result
        return "SUCCESS"

    def update_meta(self, name, users, viewers, client_id):
        '''Update the meta data of the document stored in the database with a client's meta data.'''
        
        if self.document_id is None:
            return "ERROR: Document not loaded."

        if self.__authorize_client(client_id, "u"):
            self.name = name
            self.users = users
            self.viewers = viewers
            self.revision = create_hash(content)
            result = Database.insert_meta(self.token,
                                          self.__convert_to_dict()[0])
            if result is not None:
                return result
        return "SUCCESS"

    def get_diff_to_patch(self, content):
        pass

    def create_document(self, name, client_id):
        self.revision = doc_util.create_hash("")
        self.users = [client_id]
        dictionary = self.database.create_document(self.token, self.__convert_to_dict())
        if dictionary["document_id"] is None:
            return "ERROR: Could not create new document."
        self.__dict_to_attributes(dictionary)
        return dictionary["document_id"]

    def __authorize_client(self, client_id, mode):
        if mode == "u":
            return client_id in self.users
        elif mode == "v":
            return client_id in self.viewers
        return False

    def __convert_to_dict(self):
        return {'document_id':self.document_id, 'curr_revision':self.revision, 'name':self.name, 
                'users': self.users, "viewers": self.viewers}, {'content':self.content,
                'revision':self.revision}

    def __dict_to_attributes(self, meta, doc):
        self.document_id = meta["document_id"]
        self.name = meta["name"]
        self.content = doc["content"]
        self.revision = doc["revision"]
        self.users = meta["users"]
        self.viewers = meta["viewers"]

    document_id = None
    name = None
    content = None
    database = None
    revision = None
    users = None
    revisionHistory = {}
    viewers = None

