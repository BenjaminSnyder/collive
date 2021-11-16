Welcome to Collive! Collive is a real-time editing REST API for developers who want to add real-time editing to their service. 

To get started, run 'pip install -r requirements.txt' to install the required modules for this project.




Team Project for Advanced Software Engineering

Team Pyoneers

Shared drive folder:
https://drive.google.com/drive/folders/16GBnaf75uVPqliTXlQpbPQWAQkqMvayV?usp=sharing


API Entry Points

*All entry points except 'token/create' expect a Bearer access token in the HTTP Authorization header

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