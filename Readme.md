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
