from tinydb import TinyDB
class User():
    def deleteUser(self, user_id):
        db = TinyDB(user_id + '/docs.json')
        db.truncate()
        
    def createUser(self, user_id):
        TinyDB(user_id + '/docs.json')
