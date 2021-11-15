from os import name
from flask import Flask, request, Response, session, jsonify

from documents.document import Document
from authentication.auth import Auth  # is this a class?
from users.user import User

from authentication.auth import AuthError, requires_auth

AUTH0_DOMAIN = 'dev-47fkm009.us.auth0.com'
API_AUDIENCE = 'https://collive/api'
ALGORITHMS = ["RS256"]

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
@requires_auth
def get_doc(doc_id):
    auth_token = request.headers.get('Authorization')
    user_id = None # get user_id from auth, using auth_token
    doc = Document(user_id)
    return jsonify(doc.loadDocument(doc_id))

@app.route('/document/update', methods=['POST'])
@requires_auth
def update_doc():
    auth_token = request.headers.get('Authorization')
    user_id = None # get user_id from auth, using auth_token
    data = request.get_json(force=True)
    doc = Document(user_id)
    msg = doc.updateContent(data['data'])
    return msg

@app.route('/document/create', methods=['POST'])
@requires_auth
def create_doc():
    auth_token = request.headers.get('Authorization')
    user_id = None # get user_id from auth, using auth_token
    doc = Document(user_id)
    msg = doc.createDocument()
    return msg

@app.route('/document/delete/<int:doc_id>')
@requires_auth
def delete_doc(doc_id):
    auth_token = request.headers.get('Authorization')
    user_id = None # get user_id from auth, using auth_token
    doc = Document(user_id)
    msg = doc.deleteDocument(doc_id)
    return msg

@app.route('/getUser/<int:user_id>')
@requires_auth
def get_user():
    pass

@app.errorhandler(AuthError)
@requires_auth
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response