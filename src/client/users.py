from tinydb import TinyDB, Query


def open_user_database() -> TinyDB:
    '''opens a database connection'''
    db = TinyDB('users.json')
    return db


def insert_user(username, password, client_id):
    '''adds username/password pair to database'''
    db = open_user_database()
    if isinstance(username, str) and isinstance(password, str) and isinstance(client_id, str):
        user = Query()
        pair = db.search(user['username'] == username)  # check if the username already exists
        if not pair:
            db.insert({'username': username, 'password': password, 'client_id': client_id})


def validate_user(username, password):
    '''validates username/password pair'''
    db = open_user_database()
    if isinstance(username, str) and isinstance(password, str):
        user = Query()
        pair = db.search(user['username'] == username)
        if not pair:
            return False
        if pair[0]['password'] == password:
            return True


def get_user_count():
    '''returns the total number of users'''
    db = open_user_database()
    return len(db)


def get_client_id(username):
    '''returns the client_id associated with the provided username'''
    db = open_user_database()
    if isinstance(username, str):
        user = Query()
        client = db.search(user['username'] == username)
        if client:
            return client[0]['client_id']
    return ''
