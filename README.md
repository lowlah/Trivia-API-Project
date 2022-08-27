# Trivia App API Development and Documentation 

This  project is a project for Udacity's full stack nanodegree program.It tests my skills on API Development and Documentation. I have been able to apply the skills  to structure and implement  API endpoints,testing the endpoints using unittest while also maintaining  API development best practices.

All backend code follows [PEP8 style guidelines](https://www.python.org/dev/peps/pep-0008/). 

## Trivia App

Trivia is a game quiz that tests your general knowledge.Currently,questions are based on 6 categories: Science,Art,Geography,History,Entertainment,Sports.

The application does the following :

1. Displays questions - It shows all questions and the category,difficulty rating  and can show/hide the answer.
2. Questions can be deleted using the delete icon button
3. A new qestion can be added on a particular category and this requires that you fill the question and answer fields and you chose a difficulty level.
4. Search for questions based on a text query string.
5. Play the quiz game, randomizing either all questions or within a specific category.

## Getting Started

### Pre-requisites and Local Development 
Developers using this project should already have Python3, pip and node installed on their local machines.

#### Backend

From the backend folder run `pip install requirements.txt`. This installs the reqirements in a virtual environment. All required packages are included in the requirements file. 

To run the application run the following commands: 
***For window users: replace "export" with "set"***
```
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

These commands put the application in  development and directs our application to use the `__init__.py` file in our flaskr folder. Working in development mode shows an interactive debugger in the console and restarts the server whenever changes are made. If running locally on Windows, look for the commands in the [Flask documentation](http://flask.pocoo.org/docs/1.0/tutorial/factory/).

The application is run on `http://127.0.0.1:5000/` by default and is a proxy in the frontend configuration. 

> View the [Backend README](./backend/README.md) for more details.

#### Frontend

From the frontend folder, run the following commands to start the client: 
```
npm install // only once to install dependencies
npm start 
```

By default, the frontend will run on localhost:3000. 

> View the [Frontend README](./frontend/README.md) for more details.

### Tests
In order to run tests navigate to the backend folder and run the following commands: 

***For window users,replace dropdb with "DROP DATABASE" and createdb with " CREATE DATABASE"***
```
dropdb bookshelf_test
createdb bookshelf_test
psql bookshelf_test < books.psql
python test_flaskr.py
```

The first time you run the tests, omit the dropdb command. 

All tests are kept in that file and should be maintained as updates are made to app functionality. 

## API Reference

### Getting Started
- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration. 
- Authentication: This version of the application does not require authentication or API keys. 

### Error Handling
Errors are returned as JSON objects in the following format:

Example: **Bad Request**
```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}

```
The API will return these error types when requests fail:
- 400: Bad Request
- 404: Resource Not Found
- 422: Not Processable
- 405: Method not allowed
- 500: Internal Server Error

### Endpoints 

#### GET `/categories`
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains an object of id: category_string key:value pairs.
- Sample: `curl http://127.0.0.1:5000/categories`

```
{
	'1' : "Science",
	'2' : "Art",
	'3' : "Geography",
	'4' : "History",
	'5' : "Entertainment",
	'6' : "Sports"
}
```

#### GET `/categories/<int:id>/questions`
- Gets all questions in a specified category by id ,returns success values and total questions
- Returns a JSON object with results paginated in 10: questions are from a specified category
- Sample: `curl http://127.0.0.1:5000/categories/3/questions`

```
{
  "current_category": "Geography",
  "questions": [
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    },
    {
      "answer": "Agra",
      "category": 3,
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    }
  ],
  "success": true,
  "total_questions": 20
}
```

#### GET `/questions`
- Returns a list of question objects,success values paginated in groups of 10
  - Includes a list of all categories  
- Sample: `curl http://127.0.0.1:5000/questions`

```
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": {},
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    {
      "answer": "George Washington Carver",
      "category": 4,
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    },
    {
      "answer": "Agra",
      "category": 3,
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    }
  ],
  "success": true,
  "total_questions": 20
}
```

#### GET `/questions?page=${integer}`
- Fetches a paginated set of questions, a total number of questions, all categories and current category string.
- Request Arguments: `page` - integer
- Returns: An object with 10 paginated questions, total questions, object including all categories, and current category string
- Sample:  `curl http://127.0.0.1:5000/questions?page=3`

```
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": {},
  "questions": [
    {
      "answer": "paris,france",
      "category": 3,
      "difficulty": 1,
      "id": 32,
      "question": "where is the eiffel tower"
    },
    {
      "answer": " Reginald Dwight",
      "category": 5,
      "difficulty": 3,
      "id": 33,
      "question": "what is Elton Johns real name?"
    }
  ],
  "success": true,
  "total_questions": 22
}
```

#### POST `/questions`
- Creates a new question using the submitted question, answer,difficulty and category. Returns the id of the created question,question created, success value, total questions and  a randomized question list based on category.
- Sample: `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"question": "What is the capital of canada?", "answer": "ottawa", "difficulty": 1, "category": "3" }'`

```
{
 "created": 27,
  "question_created": "What is the capital of canada?",
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    {
      "answer": "George Washington Carver",
      "category": 4,
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    },
    {
      "answer": "Agra",
      "category": 3,
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    }
  ],
  "success": true,
  "total_questions": 21
}

```

#### POST `/questions/search`
- Searches for questions using a search term, 
- Returns a JSON object with paginated questions matching the search term
- Sample: `curl http://127.0.0.1:5000/questions/search -X POST -H "Content-Type: application/json" -d '{"searchTerm": "city"}'`

```
{
"current_category": null,
  "questions": [
    {
      "answer": "Agra",
      "category": 3,
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    }
  ],
  "success": true,
  "total_questions": 1
}
```

#### DELETE `/questions/<int:id>`
- Deletes a question by id if it exists
- Returns id of deleted questions ,success value,total questions if successful
- Sample: `curl http://127.0.0.1:5000/questions/27 -X DELETE`

```
{
  "deleted": 27,
  "success": true,
  "total_questions": 20
}
```

#### POST `/quizzes`
- Returns a random quiz question based on previous questions and  category parameters
- Sample: `curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions": [], "quiz_category": {"type": "Geography", "id": "3"}}'`

```
 "question": {
    "answer": "Lake Victoria",
    "category": 3,
    "difficulty": 2,
    "id": 13,
    "question": "What is the largest lake in Africa?"
  },
  "success": true
}
```

## Deployment N/A

## Authors
The todos for the project as instructed by Udacity were completed by **Omolola Oladeinde** 
All other project files were created by Udacity for the Full Stack Web Developer Nanodegree. Also some methods for endpoints used may seem similar , based on my understanding in the examples in class,I followed the same principles. 

## Acknowledgements 
Udacity for the opportunity! ALX slack channel(students and session Leads) for all the help and suggestions.