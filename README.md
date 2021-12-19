[![Python Build](https://github.com/BenjaminSnyder/collive/actions/workflows/python-app.yml/badge.svg)](https://github.com/BenjaminSnyder/collive/actions/workflows/python-app.yml) [![codecov](https://codecov.io/gh/BenjaminSnyder/collive/branch/main/graph/badge.svg?token=UCNGGNO8VM)](https://codecov.io/gh/BenjaminSnyder/collive)
# Welcome to Collive! 
	
Collive is a real-time editing REST API for developers who want to add real-time editing to their service.
\
Pyoneer's Team Project for Advanced Software Engineering
\
\
Getting Started:

 - To get started, run `pip install -r requirements.txt` to install the
   required modules for this project. 
  - To run the service: In the `/src`
   directory, do `export FLASK_APP=app`. Then do `flask run`. To run the
   test suite and generate coverage report: `pytest --cov=src tests/`
   - To run style-checking, run: `flake8 > bugs.txt`
	   - The file `bugs.txt` will contain the list of all style and bug
   errors.
  - For system checking: The result of the Postman tests can be found in
  `postman_test_result.json`

## API  Overview
| Method | Endpoint   | Action
|--|--|--|
| POST | `/token/create`    | Create API token.
| POST | `/document/create` | Create a new document.
| POST | `/document/delete` | Deletes a document.
| GET  | `/document/get`    | Gets current revision of a document.
| POST | `/document/update` | Commits an update to a document
-----

### POST `/token/create` ([create_client](https://github.com/BenjaminSnyder/collive/blob/main/src/app.py#L120)) 
 
Creates a new API token and associated developer database that is mapped to that token. Returns the Bearer token that was generated. Returns code `200` on success, `400` on error.

----- 

### POST `/document/create` ([create_doc](https://github.com/BenjaminSnyder/collive/blob/main/src/app.py#L75)) 

Expects json input specifying client_id and creates a new document in that client's database. Returns the metadata json of created file. Returns code `200` on success, `400` on error.

#### Request:
```json
{
    "client_id": "client id",
    "name": "name of document"
}
```
#### Response:
```json
{
	"curr_revision": "revision hash",
	"document_id": "document id",
	"name": "document name",
	"type": "meta",
	"users": [ "user" ],
	"viewers": [ "viewer" ]
}
```

-----
###  POST `/document/delete` ([delete_doc](https://github.com/BenjaminSnyder/collive/blob/main/src/app.py#L92))

Expects json input specifying client_id and doc_id. Deletes document. Returns json containing result. Returns code `200` on success, `400` on error.
#### Request:
```json
{
    "client_id": "client id",
    "name": "name of document"
}
```
#### Response:
```json
{
	"type": "sucess|error",
	"msg" : "success message or error message"
}
```

-----

###  GET `/document/get` ([get_doc](https://github.com/BenjaminSnyder/collive/blob/main/src/app.py#L18))
Given doc_id and client_id in url parameters, returns json with document metadata and data for most recently updated document version Returns code `200` on success, `400` on error.

#### Query Parameters:

 - `doc_id`: document ID
 - `client_id` client ID
 
 #### Response:
```json
[{
	"curr_revision": "revision hash",
	"document_id": "document id",
	"name": "document name",
	"type": "meta",
	"users": [ "user" ],
	"viewers": [ "viewer" ]
},
{
	"content": "Document's current content",
	"revision_hash": "Document's current revision hash",
	"type": "revision"

}
```

-----

### POST `/document/update` ([update_doc](https://github.com/BenjaminSnyder/collive/blob/main/src/app.py#L44)) 

Expects json input specifying client_id, doc_id, and content to update the document with. Returns json of document's updated meta data, or error otherwise. Returns code `200` on success, `400` on error.
#### Request:
```json
{
    "client_id": "client id",
    "doc_id": "document id"
    "content": "Content to submit"
}
```
#### Response:
```json
{
	"curr_revision": "revision hash",
	"document_id": "document id",
	"name": "document name",
	"type": "meta",
	"users": [ "user" ],
	"viewers": [ "viewer" ]
}
```
