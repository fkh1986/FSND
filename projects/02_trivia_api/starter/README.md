# Full Stack API Final Project

## Udacitrivia

This Trivia application allows users to test their knowledge in different topics, combining knowledge and fun!

This application was orignally developed by some of Udacity team members, and work submitted for this project was done to deliver the API final project in the Full Stack Development Nanodegree.

The application is a great game of Trivia where user gets to choose one of many categories, or all categories at once and they will prompted to answer different questions that are relevant to their selection. Their answers gets checked and the final score displayed at the end of the quiz.

The application also allows to test makers to view all questions and answers, and even add more questions!

Give it a try and you will find that the sky is the limit!


_Note for contributors: Please feel free to contribute to the project since it is still in a basic form, and could use a lot of improvement. However please note that we are trying our best to follow the [PEP8 style guide](https://www.python.org/dev/peps/pep-0008/) and we would appreciate all contributions that follows the same style._


## Stack Used

Before you get started, we would like to inform you about the stack used for this project:

### Backend:

We are using the most awesome Python language (we recommend using Python 3.7), and using the Flask web framework.
As for the database, we are using the robust PostgreSQL.

### Frontend:

For this project we are using the React web framework.


## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

### Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

### Running the backend server
The Flask server can be started using the `start.sh` script or the following commands in the backend directory from your terminal:
```bash
export FLASK_ENV=development
export FLASK_APP=flaskr
export DB_USER={your-database-username}
export DB_PASS={your-database-password}
export SECRET_KEY={your-secret-key}
flask run
```

### Running the frontend server
The React server can be started from within the frontend directory by running the following commands:

_To install project dependencies_
```bash
npm install
```

_To run the server_
```bash
npm start
```

For more information, please review the README file within the frontend folder.

## Tests

Unit tests are available for the backend api endpoint, and can be very helpful for testing any additions or modifications to the code, to ensure that everything is working perfectly! The unit tests can be found in the `test_flaskr.py` file in the backend folder.
Make sure to setup a separate database for testing purposes.


## API Documentation

This document explains the different endpoints that can be used by this applicaation.

### Getting started

This project implements RESTful API endpoints to allow for different CRUD operations.

### Base URL

This should be your server's URL, if you are running the Flask development server then this could be:

`http://127.0.0.1:5000`

### Authentication

This API does not implement any authentication methods, and so all endpoints are exposed for public

### Error Codes

This API uses standard HTTP error codes including:

- **400: Bad Request**
- **404: Not Found**
- **405: Method Not Allowed**
- **422: Unprocessable**

### Endpoints

#### Categories

1. **`GET /categories`**

Returns a list of all available categories.

##### _Parameters_

- `page`: pagination parameter for categories returned

##### _Response body_
- `categories`: **Object**: { id: type } for each category.
- `success`: **Boolean**: Request Success

##### _Example Response_
```json
{
  "categories": {
    "1": "science",
    "2": "art",
  },
  "success": true
}
```

2. **`GET /categories/{category_id}/questions`**

Returns a list of all questions for a specific category with (`id = category_id`)

##### _Parameters_
- `page`: pagination parameter for categories returned

##### _Response body_
- `questions`: **List of Question Objects**: { question, answer, category, difficulty }
- `current_category`: **Integer**: Current category ID
- `total_questions`; **Integer**: Total number of available questions
- `success`: **Boolean**: Request Success

##### _Example Response_
```json
{
  "current_category": 4,
  "questions": [
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
  ],
  "success": true,
  "total_questions": 4
}

```

#### Questions

1. **`GET /questions`**

Returns a list of all available questions.

##### _Parameters_
- `page`: pagination parameter for questions returned

##### _Response body_
- `questions`: **List of Question Objects**: { question, answer, category, difficulty }
- `categories`: **Object**: { id: type } for each category.
- `current_category`: **Integer**: Current category ID
- `total_questions`; **Integer**: Total number of available questions
- `success`: **Boolean**: Request Success

##### _Example Response_
```json
{
  "categories": {
    "1": "science",
    "2": "art",
  },
  "current_category": 1,
  "questions": [
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
  ],
  "success": true,
  "total_questions": 20
}
```


2. **`POST /questions`**

Adds a new question to the list of available questions.

##### _Request Body_
- `question`: **String**: Question Text
- `answer`: **String**: Answer Text
- `category`: **Integer**: Question category ID
- `difficulty`: **Integer**: Question difficulty

##### _Response body_
- `success`: **Boolean**: Request Success

##### _Example Response_
```json
{
  "success": true
}
```

3. **`DELETE /questions/{question_id}`**

Deletes a specific question with (`id = question_id`) from the list of available questions.

##### _Request Body_
This endpoint has no request body or parameters

##### _Response body_
- `question_id`: **Integer**: ID of deleted question
- `success`: **Boolean**: Request Success

##### _Example Response_
```json
{
  "question_id": 14,
  "success": true
}
```

4. **`POST /questions/search`**

Retrieves questions with a matching search term from the list of available questions.

##### _Request Body_
- `searchTerm`: **String**: The search term to look for

##### _Response body_
- `questions`: **List of Question Objects**: { question, answer, category, difficulty }
- `total_questions`; **Integer**: Total number of available questions
- `success`: **Boolean**: Request Success

##### _Example Response_
```json
{
  "questions": [
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    }
  ],
  "success": true,
  "total_questions": 1
}

```

#### Quizzes

1. **`POST /quizzes/play`**

Starts a quiz based on the selected category.

##### _Request Body_
- `previous_questions`: **List**: list of previous questions IDs
- `quiz_category`: **Integer**: ID of selected category (0 for All categories)

##### _Response body_
- `question`: **Question Object**: { question, answer, category, difficulty } for next question
- `previous_questions`: **List**: list of previous questions IDs
- `success`: **Boolean**: Request Success

##### _Example Response_
```json
{
  "previous_questions": [
    20
  ],
  "question": {
    "answer": "Alexander Fleming",
    "category": 1,
    "difficulty": 3,
    "id": 21,
    "question": "Who discovered penicillin?"
  },
  "success": true
}
```


## Author

Fadi Haddad


## Acknowledgements

Thanks to the Udacity Team behind this great project and application




