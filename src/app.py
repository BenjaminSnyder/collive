from os import name
from flask import Flask, request, Response, session, jsonify

from documents.document import Document
from authentication.auth import Auth # is this a class?
from users.user import User

app = Flask(__name__)
app.config.from_mapping(SECRET_KEY='dev')

'''
# before each request, check if user (API caller/developer) is authenticated
@app.before_request
def check_user_login():
    if 'user_id' not in session:
        print('Developer not logged in.')

# login the user 
@app.route('/login', methods=['POST'])
def login():
    user = request.get_json(force=True)
    # auth
    
    # if no issues, new session
    if True:
        session['user_id'] = user['user_id']
    return 'Logins successful.'
'''

@app.route('/document/get/<int:doc_id>')
def get_doc(doc_id):
    auth_token = request.headers.get('Authorization')
    user_id = None # get user_id from auth, using auth_token
    doc = Document(user_id)
    return jsonify(doc.loadDocument(doc_id))

@app.route('/document/update', methods=['POST'])
def update_doc():
    auth_token = request.headers.get('Authorization')
    user_id = None # get user_id from auth, using auth_token
    data = request.get_json(force=True)
    doc = Document(user_id)
    msg = doc.updateDocument(data['data'])
    return msg

@app.route('/document/create', methods=['POST'])
def create_doc():
    auth_token = request.headers.get('Authorization')
    user_id = None # get user_id from auth, using auth_token
    doc = Document(user_id)
    msg = doc.createDocument()
    return msg

@app.route('/document/delete/<int:doc_id>')
def delete_doc(doc_id):
    auth_token = request.headers.get('Authorization')
    user_id = None # get user_id from auth, using auth_token
    doc = Document(user_id)
    msg = doc.deleteDocument(doc_id)
    return msg

@app.route('/getUser/<int:user_id>')
def get_user():
    pass
