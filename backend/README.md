# Backend - Trivia API

## Setting up the Backend

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - It is  recommended that you work within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/)

***please follow the instructions carefully to avoid any error***

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

With Postgres running, create a `trivia` database:

**for unix/mac os**
```bash
createdb trivia
```

**for window users**
```
CREATE DATABASE trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

**for mac users**
```bash
psql trivia < trivia.psql
```

**for windows users**
```
psql -U student trivia < trivia.psql
```

### Run the Server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## Testing

Test for the success and error behavior of each endpoint using the unittest library.

To deploy the tests, run

**For bash**
```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python3 test_flaskr.py
```

**For windows using command prompt**
```bash
DROP DATABASE trivia_test
CREATE DATABASE trivia_test
psql -U student trivia_test < trivia.psql
python test_flaskr.py
```
