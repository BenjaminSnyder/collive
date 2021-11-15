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
        dictionary = self.database.delete_document(self.__convert_to_dict())
        if dictionary["document_id"] is not None:
            return "ERROR: Document not deleted."
        return "SUCCESS"

    def update_content(self, content):
        if self.document_id is None:
            return "ERROR: Document not Loaded."
        self.revision += 1
        self.content = content
        dictionary = self.database.insert(self.__convert_to_dict())
        if dictionary["content"] is None:
            return "ERROR: Document Content not updated."
        return "SUCCESS"

    def create_document(self):
        self.revision = 0
        dictionary = self.database.create_document(self.__convert_to_dict())
        if dictionary["document_id"] is None:
            return "ERROR: Failed to create document."
        self.__dict_to_attributes(dictionary)
        return dictionary["document_id"]

    def __convert_to_dict(self):
        return {'document_id':self.document_id, 'name':self.name, 'content':self.content,
                'revision':self.revision}

    def __dict_to_attributes(self, dictionary):
        self.document_id = dictionary["document_id"]
        self.name = dictionary["name"]
        self.content = dictionary["content"]
        self.revision = dictionary["revision"]

    document_id = None
    name = None
    content = None
    database = None
    revision = None
