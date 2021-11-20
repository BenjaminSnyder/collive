Welcome to Collive! Collive is a real-time editing REST API for developers who want to add real-time editing to their service. 

Team Project for Advanced Software Engineering

Team Pyoneers

Shared drive folder:
https://drive.google.com/drive/folders/16GBnaf75uVPqliTXlQpbPQWAQkqMvayV?usp=sharing

To get started, run 'pip install -r requirements.txt' to install the required modules for this project.

To run the service:
In the src directory, do $$ export FLASK_APP=app $$. Then do $$ flask run $$. 

To run the test suite and generate coverage report:
pytest --cov=src tests/

To run style-checking, run:
flake8 > bugs.txt

The file "bugs.txt" will contain the list of all style and bug errors.

For system checking:
The result of the Postman tests can be found in "postman_test_result.json"

API Entry Points

*All entry points except 'token/create' expect a Bearer access token in the HTTP Authorization header. 
This bearer token is authenticated and then used to determine which database to query from. I.e. each 

GET /document/get
- Expects url parameters doc_id and client_id
- Returns most recently updated document given these parameters

POST /document/update
- Expects json input with client_id and doc_id
- Updates document in database
- Returns status message

POST /document/create
- Expects json input with client_id
- Creates new document in database
- Returns doc_id

POST /document/delete
- Expects json input with client_id and doc_id
- Deletes document from database
- Returns status message

GET /token/create
- Generates a database 
- Returns the access token

Order of operation:
- /token/create must be run before /document/create. 
- /document/create must be run before any other operation listed above. 
- Exception: there already exists a token and/or document_id (i.e. that was manually entered into the db)
