from flask import Flask, json, request, jsonify

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

    if not doc_id:
        return jsonify({"type": "error",
                        "msg": "doc_id parameter missing"}), 400
    elif not client_id:
        return jsonify({"type": "error",
                        "msg": "client_id parameter missing"}), 400

    doc = Document(access_token)
    out = doc.load_document(doc_id, client_id)
    if out[0]["type"] == "error":
        if out[0]["code"] == "EACCESS":
            return out[0], 403
        else:
            return out[0], 404
    return jsonify(out)


@app.route('/document/update', methods=['POST'])
@authenticate
def update_doc():
    '''Updates document given doc_id and document
     content. Returns the status message'''
    access_token = request.headers.get('Authorization')
    input = request.get_json(force=True)

    err = check_input(['doc_id', 'client_id', 'content'], input)
    if err is not None:
        return err, 400

    if 'content' not in input:
        return jsonify({"type": "error",
                        "msg": "content parameter needed"}), 400

    doc = Document(access_token)
    msg = doc.load_document(input['doc_id'], input['client_id'])
    if msg[0]["type"] == "error":
        if msg[0]["code"] == "EACCESS":
            return msg[0], 403
        else:
            return msg[0], 404

    msg = doc.update_content(input['content'], input['client_id'])
    if msg["type"] == "error":
        return jsonify(msg), 400
    else:
        return jsonify(msg), 200


@app.route('/document/create', methods=['POST'])
@authenticate
def create_doc():
    '''Creates a document for a client, returns status message'''
    access_token = request.headers.get('Authorization')
    input = request.get_json(force=True)

    err = check_input(['client_id', 'name'], input)
    if err is not None:
        return err, 400

    doc = Document(access_token)

    doc_id = doc.create_document(input['name'], input['client_id'])
    return doc_id


@app.route('/document/delete', methods=['POST'])
@authenticate
def delete_doc():
    '''Deletes a document given doc_id and client_id'''
    access_token = request.headers.get('Authorization')
    input = request.get_json(force=True)

    err = check_input(['doc_id', 'client_id'], input)
    if err is not None:
        return jsonify(err), 400

    doc = Document(access_token)
    msg = doc.load_document(input['doc_id'], input['client_id'])
    if msg[0]["type"] == "error":
        if msg[0]["code"] == "EACCESS":
            return msg[0], 403
        else:
            return msg[0], 404
    msg = doc.delete_document(input['client_id'])
    if msg["type"] == "error":
        return jsonify(msg), 400
    return jsonify(msg)


@app.route('/token/create')
def create_token():
    '''Generates a database and returns the access_token'''
    pass


@app.route('/client/create', methods=['POST'])
@authenticate
def create_client():
    pass


def check_input(keys: list, dict: dict):
    for key in keys:
        try:
            val = dict[key]

            if type(val) != str:
                return {"type": "error",
                        "msg": f"{key} must be of type string"}
            elif len(val) == 0:
                return {"type": "error", "msg": f"{key} cannot be an empty string"}

        except KeyError:
            return {"type": "error", "msg": f"{key} parameter missing"}

    return None
