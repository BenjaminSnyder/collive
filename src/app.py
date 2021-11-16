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

# API access token authentication happens before each method.
# All methods assume Bearer token is in Authorization http header.
# Database of document is determined by access token

# Returns the most recently updated document given doc_id
# and client_id in url parameters.
# Returns an error message if client does not have access to document.


@app.route('/document/get')
@requires_auth
def get_doc():
    access_token = request.headers.get('Authorization')
    doc_id = request.args.get('doc_id')
    client_id = request.args.get('client_id')

    doc = Document(access_token)
    return jsonify(doc.loadDocument(doc_id, client_id))

# Updates document given doc_id and document content. Returns the status message.


@app.route('/document/update', methods=['POST'])
@requires_auth
def update_doc():
    access_token = request.headers.get('Authorization')
    input = request.get_json(force=True)

    doc = Document(access_token, input['client_id'])
    doc.load_document(input['doc_id'], input['client_id'])

    msg = doc.updateContent(input['content'], input['client_id'])
    return msg

# Creates a document for a client, returns status message.


@app.route('/document/create', methods=['POST'])
@requires_auth
def create_doc():
    access_token = request.headers.get('Authorization')
    input = request.get_json(force=True)

    doc = Document(access_token)
    doc.load_document(input['doc_id'], input['client_id'])

    msg = doc.createDocument(input['client_id'])
    return msg

# Deletes a document given doc_id and client_id.


@app.route('/document/delete', methods=['POST'])
@requires_auth
def delete_doc():
    access_token = request.headers.get('Authorization')
    input = request.get_json(force=True)

    doc = Document(access_token, input['client_id'])
    doc.load_document(input['doc_id'], input['client_id'])

    msg = doc.deleteDocument(input['doc_id'])
    return msg


@app.route('/client/add', methods=['POST'])
@requires_auth
def add_client():
    pass


@app.errorhandler(AuthError)
@requires_auth
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response
