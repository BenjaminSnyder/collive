from database.db import Database
class User():
    def __init__(self, user_id):
        self.database = Database("users")
        self.user_id = user_id

    def deleteUser(self, content):
        self.database.insert(self.__convertToDict())
        return "SUCCESS"

    def createUser(self, user_id):
        self.database.createUser(self.__convertToDict())

    def __convertToDict(self):
        return {'user_id':self.user_id}

    def __dictToAttributes(self, dictionary):
        self.user_id = dictionary["user_id"]

    user_id = None
    database = None