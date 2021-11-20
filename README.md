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

API Entry Points:

Refer to 'index.html' for documentation on all entry points in the API.
