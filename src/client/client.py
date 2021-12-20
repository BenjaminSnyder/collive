import requests
import os
from flask import Flask, request, render_template, g, redirect, Response, flash, session
from users import open_user_database, insert_user, validate_user, get_user_count, get_client_id
from access import open_access_database, update_access, return_access, add_doc
from doc_id import open_doc_id_database, update_doc_name, return_doc_name
from tinydb import TinyDB, Query
import json
import pprint

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
    doc_ids = return_access(username)
    doc_list = []
    if doc_ids:
        for id in doc_ids:
            doc_name = return_doc_name(id)
            doc_list.append({'doc_id': id, 'doc_name': doc_name})
    return render_template('index.html', doc_list=doc_list)

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
            pair = db.search(user['username'] == username) # check if the username already exists
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
    response = requests.post(url='http://127.0.0.1:5000/document/create', headers=bearer, json=params)
    info = json.loads(response.text)
    add_doc(g.account, str(info['document_id']))
    update_doc_name(str(info['document_id']), str(info['name']))
    flash("Document successfully created!")
    return redirect('index')

@app.route('/document', methods=['GET'])
def display_document():
    doc_id = request.args.get('doc_id')
    client_id = get_client_id(g.account)
    headers = {'Authorization': 'Bearer f2dOqweIWy65QWlwiw', 'Connection': 'keep-alive', 'Accept': '*/*'}
    request_url = 'http://127.0.0.1:5000/document/get?doc_id={doc_id}&client_id={client_id}'.format(doc_id=doc_id, client_id=client_id)
    response = requests.get(url=request_url, headers=headers)
    info = json.loads(response.text)
    print(info)
    return render_template('document.html', doc_info=info, client_id=client_id)

@app.route('/send', methods=['POST'])
def send():
    data = request.values
    content = data['content']
    client_id = data['client_id']
    doc_id = data['doc_id']

    headers = {'Authorization': 'Bearer f2dOqweIWy65QWlwiw', 'Connection': 'keep-alive', 'Accept': '*/*'}
    params = {'client_id': client_id, 'doc_id': doc_id, 'content': content}
    print(params)
    response = requests.post(url='http://127.0.0.1:5000/document/update', headers=headers, json=params)
    print(response)

    request_url = 'http://127.0.0.1:5000/document/get?doc_id={doc_id}&client_id={client_id}'.format(doc_id=doc_id, client_id=client_id)
    response = requests.get(url=request_url, headers=headers)
    info = json.loads(response.text)
    print(info)
    return render_template('document.html', doc_info=info, client_id=client_id)

@app.route('/share', methods=['POST'])
def share():
    username = request.form['username']
    doc_id = request.form['doc_id']
    add_doc(username, doc_id)

    client_id = get_client_id(g.account)
    headers = {'Authorization': 'Bearer f2dOqweIWy65QWlwiw', 'Connection': 'keep-alive', 'Accept': '*/*'}
    request_url = 'http://127.0.0.1:5000/document/get?doc_id={doc_id}&client_id={client_id}'.format(doc_id=doc_id, client_id=client_id)
    response = requests.get(url=request_url, headers=headers)
    info = json.loads(response.text)
    flash("Shared with " + username + "!")
    print(info)
    return redirect('document?doc_id={doc_id}'.format(doc_id=doc_id))