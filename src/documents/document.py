from database.db import Database


class Document():
    def __init__(self, user_id):
        self.database = Database(user_id)

    def load_document(self, document_id):
        dictionary = self.database.get_document(document_id)
        self.__dict_to_attributes(dictionary)
        return dictionary

    def delete_document(self, document_id):
        self.document_id = document_id
        self.database.delete_document(self.__convert_to_dict())
        return self.__convert_to_dict()

    def update_content(self, content):
        if self.document_id is None:
            return "ERROR: Document not Loaded"
        self.revision += 1
        self.content = content
        self.database.insert(self.__convert_to_dict())
        return self.__convert_to_dict()

    def create_document(self):
        self.revision = 0
        dictionary = self.database.create_document(self.__convert_to_dict())
        self.__dict_to_attributes(dictionary)
        return self.__convert_to_dict()

    def __convert_to_dict(self):
        return {'document_id':self.document_id, 'name':self.name, 'content':self.content,
                'revision':self.revision}

    def __dict_to_attributes(self, dictionary):
        self.document_id = dictionary["document_id"]
        self.name = dictionary["name"]
        self.content = dictionary["content"]

    document_id = None
    name = None
    content = None
    database = None
    revision = None
