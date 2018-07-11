# iqvia

An API to handle contacts.
We consider all the fields as mandatory (first name, surname, username and email address) which sounds realistic for
a contact form.

## Installation

- virtualenv env -p python3
- source env/bin/activate
- pip install -r requirements.txt

## Generate a new sqlite database

- cd iqvia
- python dbinit.py

You'll bet a fresh iqvia.db mapped in the config.py

## Run unit tests:

- python -m pytest tests

## Start the server

- python manage runserver.py

## See the API documentation

- After starting the server locally, go on http://0.0.0.0:7000/docs/
