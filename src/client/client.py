from urllib.parse import urlparse
from flask.helpers import send_file, url_for
from flask.json import jsonify
import requests
import os
from flask import Flask, request, render_template, g, redirect, Response, flash, session
from requests.api import get
from users import open_user_database, insert_user, validate_user, get_user_count, get_client_id
from access import open_access_database, update_access, return_access, add_doc
from doc_id import open_doc_id_database, update_doc_name, return_doc_name
from tinydb import TinyDB, Query
import json
from werkzeug.exceptions import HTTPException
import pprint
from io import BytesIO

HOSTURL = os.environ.get('PRODUCTION') or '127.0.0.1'
PORT = 5000

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)
app.config.from_mapping(SECRET_KEY='dev')

# populate user database
open_user_database()
insert_user('JamesMoriarty', 'finalproblem1', '0')
insert_user('JamesBond', 'finalproblem1', '0')

# populate user document database
open_access_database()
update_access('JamesMoriarty', [])
update_access('JamesBond', [])


@app.before_request
def before_request():
    username = session.get('username')
    if username is None:
        g.account = None
    else:
        g.account = username


@app.route('/')
@app.route('/index')
def index():
    username = session.get('username')

    headers = {'Authorization': 'Bearer f2dOqweIWy65QWlwiw', 'Connection': 'keep-alive', 'Accept': '*/*'}
    request_url = f'http://{HOSTURL}:{PORT}/client/get/documents'
    # print(get_client_id(g.account))
    response = requests.post(url=request_url, headers=headers, json={"client_id": get_client_id(g.account)})
    if not response.status_code == 200:
        return render_template('index.html', doc_list={})
    data = response.json()
    docs = data.get('documents')
    return render_template('index.html', doc_list=docs)


@app.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        isValid = validate_user(username, password)

        if not isValid:
            error = 'Invalid login.'

        if error is None:
            session.clear()
            session['username'] = username
            return redirect('index')

        flash(error)

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')


@app.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        else:
            db = open_user_database()
            user = Query()
            pair = db.search(user['username'] == username)  # check if the username already exists
            if not pair:
                client_id = str(get_user_count())
                db.insert({'username': username, 'password': password, 'client_id': client_id})
                flash('Registration successful, ' + username + '. You may proceed to login.')
                return redirect('login')
            error = 'Username already exists.'
        flash(error)
    return render_template('register.html')


@app.route('/create', methods=['POST'])
def create_document():
    doc_name = request.form['doc_name'].strip()
    client_id = get_client_id(g.account)
    bearer = {'Authorization': 'Bearer f2dOqweIWy65QWlwiw'}
    params = {'client_id': client_id, 'name': doc_name}
    response = requests.post(url=f'http://{HOSTURL}:{PORT}/document/create', headers=bearer, json=params)
    code = response.status_code
    error = response.text
    if code != 200:
        flash('{code} error: {error}'.format(code=code, error=error))
        return redirect('index')
    if response.text:
        info = json.loads(response.text)
    else:
        info = {}
    add_doc(g.account, str(info.get('document_id')))
    update_doc_name(str(info.get('document_id')), str(info.get('name')))
    flash("Document successfully created!")
    return redirect('index')


@app.route('/getupdatedcontent', methods=['GET'])
def get_updated_document_text():
    doc_id = request.args.get('doc_id')
    client_id = get_client_id(g.account)
    headers = {'Authorization': 'Bearer f2dOqweIWy65QWlwiw', 'Connection': 'keep-alive', 'Accept': '*/*'}
    request_url = f'http://{HOSTURL}:{PORT}/document/get?doc_id={doc_id}&client_id={client_id}'
    response = requests.get(url=request_url, headers=headers)
    info = json.loads(response.text)
    if info[0].get('type') == 'error':
        return render_template('document.html', doc_info=info, client_id=client_id, error='No new changes')
    # print(info)
    return jsonify(info[1]['content'])


@app.route('/document', methods=['GET'])
def display_document():
    doc_id = request.args.get('doc_id')
    client_id = get_client_id(g.account)
    headers = {'Authorization': 'Bearer f2dOqweIWy65QWlwiw', 'Connection': 'keep-alive', 'Accept': '*/*'}
    request_url = f'http://{HOSTURL}:{PORT}/document/get?doc_id={doc_id}&client_id={client_id}'
    response = requests.get(url=request_url, headers=headers)
    code = response.status_code
    error = response.text
    info = json.loads(response.text)
    if code != 200:
        flash('{code} error: {error}. {Info}'.format(code=code, error=error, Info=info))
        return redirect('index')
    info = json.loads(response.text)
    if isinstance(info, dict):
        if info.get('type') == 'error':
            flash("You don't have access to that document!")
            return redirect(url_for('index'))
    return render_template('document.html', doc_info=info, client_id=client_id)


@app.route('/send', methods=['POST'])
def send():
    data = request.values
    content = data['content']
    client_id = data['client_id']
    doc_id = data['doc_id']

    headers = {'Authorization': 'Bearer f2dOqweIWy65QWlwiw', 'Connection': 'keep-alive', 'Accept': '*/*'}
    params = {'client_id': client_id, 'doc_id': doc_id, 'content': content}
    # print(params)
    response = requests.post(url=f'http://{HOSTURL}:{PORT}/document/update', headers=headers, json=params)
    print(response)
    return jsonify({'success': True}), 200
    # request_url = f'http://{HOSTURL}:{PORT}/document/get?doc_id={doc_id}&client_id={client_id}'
    # response = requests.get(url=request_url, headers=headers)
    # info = json.loads(response.text)
    # print(info)
    # return render_template('document.html', doc_info=info, client_id=client_id)

@app.route('/exporttopdf', methods=['GET'])
def export():
    data = request.values
    doc_id = data['doc_id']
    client_id = get_client_id(g.account)

    headers = {'Authorization': 'Bearer f2dOqweIWy65QWlwiw', 'Connection': 'keep-alive', 'Accept': '*/*'}
    params = {'client_id': client_id, 'doc_id': doc_id}
    response = requests.get(url=f'http://{HOSTURL}:{PORT}/document/export/pdf', headers=headers, params=params)
    # print(response.json())
    data = json.loads(response.text)
    return data
    # response = requests.get(url=data['url'])
    # # name = urlparse(data['url']).path.rsplit('/')[-1]
    # # return send_file(BytesIO(response.text.encode()), attachment_filename=f'{name}.pdf', as_attachment=True)


@app.route('/share', methods=['POST'])
def share():
    username = request.form['username']
    doc_id = request.form['doc_id']

    db = open_user_database()
    user = Query()
    user = db.search(user['username'] == username)
    if not user:
        flash("User does not exist!")
        return redirect('document?doc_id={doc_id}'.format(doc_id=doc_id))
    new_client_id = user[0]['client_id']
    client_id = get_client_id(g.account)

    headers = {'Authorization': 'Bearer f2dOqweIWy65QWlwiw', 'Connection': 'keep-alive', 'Accept': '*/*'}
    request_url = f'http://{HOSTURL}:{PORT}/document/share'
    response = requests.post(url=request_url, headers=headers, json={'new_doc_users': [new_client_id], 'doc_id': doc_id, 'client_id': client_id})
    if response.json()['type'] == "error":
        flash(f"There was a problem! {response.json()['msg']}")
        return redirect('document?doc_id={doc_id}'.format(doc_id=doc_id))
    headers = {'Authorization': 'Bearer f2dOqweIWy65QWlwiw', 'Connection': 'keep-alive', 'Accept': '*/*'}
    request_url = f'http://{HOSTURL}:{PORT}/document/get?doc_id={doc_id}&client_id={client_id}'
    response = requests.get(url=request_url, headers=headers)
    code = response.status_code
    error = response.text
    if code != 200:
        flash('{code} error: {error}'.format(code=code, error=error))
        return redirect('index')
    info = json.loads(response.text)
    flash("Shared with " + username + "!")
    # print(info)
    return redirect('document?doc_id={doc_id}'.format(doc_id=doc_id))
