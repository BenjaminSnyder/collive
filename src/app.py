from flask import Flask, request, jsonify

from documents.document import Document

from authentication.auth import authenticate


app = Flask(__name__)
app.config.from_mapping(SECRET_KEY='dev')

# API access token authentication happens before each method.
# All methods assume Bearer token is in Authorization http header.
# Database of document is determined by access token


@app.route('/document/get')
@authenticate
def get_doc():
    '''Returns the most recently updated document
     given doc_id and client_id in url parameters'''
    access_token = request.headers.get('Authorization')
    doc_id = request.args.get('doc_id')
    client_id = request.args.get('client_id')

    doc = Document(access_token)
    return jsonify(doc.load_document(doc_id, client_id))


@app.route('/document/update', methods=['POST'])
@authenticate
def update_doc():
    '''Updates document given doc_id and document
     content. Returns the status message'''
    access_token = request.headers.get('Authorization')
    input = request.get_json(force=True)

    doc = Document(access_token, input['client_id'])
    doc.load_document(input['doc_id'], input['client_id'])

    msg = doc.updateContent(input['content'], input['client_id'])
    return msg


@app.route('/document/create', methods=['POST'])
@authenticate
def create_doc():
    '''Creates a document for a client, returns status message'''
    access_token = request.headers.get('Authorization')
    input = request.get_json(force=True)

    doc = Document(access_token)

    doc_id = doc.createDocument(input['client_id'])
    return doc_id


@app.route('/document/delete', methods=['POST'])
@authenticate
def delete_doc():
    '''Deletes a document given doc_id and client_id'''
    access_token = request.headers.get('Authorization')
    input = request.get_json(force=True)

    doc = Document(access_token, input['client_id'])
    doc.load_document(input['doc_id'], input['client_id'])

    msg = doc.deleteDocument(input['doc_id'])
    return msg


@app.route('/token/create')
def create_token():
    '''Generates a database and returns the access_token'''
    pass


@app.route('/client/add', methods=['POST'])
@authenticate
def add_client():
    pass
