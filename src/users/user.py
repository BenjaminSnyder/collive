from database.db import Database
class User():
    def __init__(self, user_id):
        self.database = Database("users")
        self.user_id = user_id
    def loadDocument(self, document_id):
        dictionary = self.database.getDocument(document_id)
        self.__dictToAttributes(dictionary)
        return dictionary

    def deleteDocument(self, document_id):
        self.document_id = document_id
        self.database.deleteDocument(self.__convertToDict())

    def deleteUser(self, content):
        if self.document_id is None:
            return "ERROR: Document not Loaded"
        self.revision += 1
        self.content = content
        self.database.insert(self.__convertToDict())
        return "SUCCESS"

    def createUser(self, user_id):
        self.database.createUser(self.__convertToDict())

    def __convertToDict(self):
        return {'document_id':self.document_id, 'name':self.name, 'content':self.content,
                'users':self.users, 'revision':self.revision}

    def __dictToAttributes(self, dictionary):
        self.document_id = dictionary["document_id"]
        self.name = dictionary["name"]
        self.content = dictionary["content"]
        self.users = dictionary["users"]
        self.users = dictionary["users"]

    user_id = None
    database = None