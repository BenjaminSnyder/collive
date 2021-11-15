from database.db import Database
class Document():
    def __init__(self, user_id):
        self.database = Database(user_id)

    def loadDocument(self, document_id):
        dictionary = self.database.getDocument(document_id)
        self.__dictToAttributes(dictionary)
        return dictionary

    def deleteDocument(self, document_id):
        self.document_id = document_id
        self.database.deleteDocument(self.__convertToDict())
        return self.__convertToDict()

    def updateContent(self, content):
        if self.document_id is None:
            return "ERROR: Document not Loaded"
        self.revision += 1
        self.content = content
        self.database.insert(self.__convertToDict())
        return self.__convertToDict()

    def createDocument(self):
        self.revision = 0
        dictionary = self.database.createDocument(self.__convertToDict())
        self.__dictToAttributes(dictionary)
        return self.__convertToDict()

    def __convertToDict(self):
        return {'document_id':self.document_id, 'name':self.name, 'content':self.content,
                'revision':self.revision}

    def __dictToAttributes(self, dictionary):
        self.document_id = dictionary["document_id"]
        self.name = dictionary["name"]
        self.content = dictionary["content"]

    document_id = None
    name = None
    content = None
    database = None
    revision = None