# Backend - Trivia API

## Setting up the Backend

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

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

```bash
createdb trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Run the Server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## API Documentation

With the server running per the above instructions, all API operations are accessible with the following base path:

`http://localhost:5000`

This version of the application does not require authentication.

*Note:* All response json has been truncated for brevity.

### Categories

`GET '/categories'`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, `categories`, that contains an object of `id: category_string` key: value pairs.

```bash
curl http://localhost:5000/categories
```

```json
{
  "1": "Science",
  "2": "Art",
  "3": "Geography",
  "4": "History",
  "5": "Entertainment",
  "6": "Sports"
}
```

`GET '/categories/{categoryId}/questions'`

- Fetch all questions for a given category
- Request Arguements: `categoryId` must be replaced with an integer in the range returned by `GET /categories`
- Returns: An array of questions for the given category. Results are paginated into groups of 10.

```bash
curl http://localhost:5000/categories/5/questions
```

```json
{
  "currentCategory": "Entertainment",
  "questions": [
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
    }
  ],
  "totalQuestions": 2
}
```

### Questions

`GET /questions`

- Fetch an array questions...
- Request Arguments: None
- Returns: An object containing an array of questions paginated into groups of 10, the number of total questions, possible categories, the currently selected category (if any)

```bash
curl http://localhost:5000/questions
```

```json
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "currentCategory": "",
  "questions": [
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Agra",
      "category": 3,
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    }
  ],
  "totalQuestions": 18
}
```
`DELETE /questions/{questionId}`

- Delete the specified question from the collection.
- Request Arguements: `questionId` must be replaced with the id of a question in the collection.
- Returns: The id of the deleted question, an array of paginated questions, and the new number of questions in the collection.

```bash
curl -X DELETE http://localhost:5000/questions/15
```

```json
{
  "deleted": 15,
  "questions": [
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }
  ],
  "totalQuestions": 17
}
```

`POST /questions - Create`

- Create and store a new question into the databased question
- Request Arguements: question, answer, difficulty, category in the body of the request
- Returns: Returns a 200 status code on success

```bash
curl -X POST http://localhost:5000/questions \
-d '{"question": "Whats my age again?", "answer": "23", "category": 5, "difficulty": 1}' \
-H 'Content-Type: application/json'
```

```json
{}
```

`POST /questions - Search`

- Search the question collection for a given string
- Request Arguments: searchTerm - the term to search for
- Returns: An array of questions matching the search string and a count of matching results

```bash
curl -X POST http://localhost:5000/questions \
-d '{"searchTerm": "what"}' \
-H 'Content-Type: application/json'
```
```json
{
  "currentCategory": "",
  "questions": [
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "23",
      "category": 5,
      "difficulty": 1,
      "id": 30,
      "question": "Whats my age again?"
    }
  ],
  "totalQuestions": 8
}
```

`POST /quizzes`

- Fetches the next question in a quiz game for the frontend application.
- Request Arguments: `previous_questions` an array of questionIds of previously asked questions, `quiz_category` an object containing the `name` and `id` of the current question category (0 if all categories)
- Returns: One question to be rendered by the frontend

```bash
curl -X POST http://localhost:5000/quizzes \
-d '{"previous_questions": [], "quiz_category": { "id": 4, "type": "entertainment" } }' \
-H 'Content-Type: application/json'
```

```json
{
  "question": {
    "answer": "Maya Angelou",
    "category": 4,
    "difficulty": 2,
    "id": 5,
    "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
  }
}
```

## Testing

[test_flasker.py](./test_flaskr.py) contains unit tests covering error and success behaviors of each endpoint using the unittest library.

To execute the tests, run the following commands:

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
