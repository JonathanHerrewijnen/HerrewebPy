# Herreweb Site
Internally build website for [Herreweb](https://www.herreweb.nl).

## Getting Started
To help contribute to the website, install dependencies in a ``Virtual Environment``:

```
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

## Project documentation
As with all Herreweb projects, the docs are provided in their stand-alone ``ReadTheDocs`` environment.

When contributing to the project, make sure you write your documentation.

To view the documentation, navigate to **documentation/readthedocs** and run the following commands:

```
make html
cd build/html
python3 -m http.server
```
The website can be accessed at **localhost:8000**

## Development
To run the backend server navigate to ``herreweb_backend/`` and run:

> python3 manage.py runserver

And for the frontend, navigate to ``herreweb_frontend``. Make sure you have npm and react-scripts installed, by running:

> sudo apt-get install npm
> npm i react-scripts

Then run:

> npm start

The file servers are accessible on ports 8000 and 3000 (localhost).

Create a superuser for you account using:

> python3 manage.py createsuperuser

Note: if running into an error regarding auth_user, be sure to migrate your database using one of the two following commands:

> python3 manage.py migrate
> python3 manage.py syncdbNo 