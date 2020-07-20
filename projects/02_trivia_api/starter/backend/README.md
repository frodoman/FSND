# Full Stack Trivia API Backend

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

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

REVIEW_COMMENT
```
This README is missing documentation of your endpoints. Below is an example for your endpoint to get all categories. Please use it as a reference for creating your documentation and resubmit your code. 

Endpoints
GET '/categories'
GET ...
POST ...
DELETE ...

GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}

```

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

# Trivia API Reference 

## Getting Started
* Base URL: Currently this app can only run locally. The backend is host at the default url: [http://127.0.0.1:5000/](http://127.0.0.1:5000/), which is configured as the proxy of the frontend app.
* Authentication: No authentication required to access the API end points.

## Error Handling
Errors are returned as JSON object in the following format: 
```bash
{
  "error": 404, 
  "message": "Not found!", 
  "success": false
}
```
Currently the API can return these error if failed: 
* 404: Not found
* 422: Unprocessable Entity
* 500: Internal server error


## Endpoints

### GET /api/categories 
* General
    - Return a list of available question categories
    - Results will be an array of string objects
* Sample 
    ```bash
    curl http://127.0.0.1:5000/api/categories
    ```
    ```bash 
    {
    "categories": [
        "Science", 
        "Art", 
        "Geography", 
        "History", 
        "Entertainment", 
        "Sports"
    ]
    }
    ```

### GET /api/questions
* General
    - Return a list of max 10 questions of the provided page index; a list of available categories and pagination information
* Parameter
    - ``` page ```, data type ``` int ```, indicate the page index, start from and default to 1
* Sample
    ```bash 
    curl http://127.0.0.1:5000/api/questions?page=2
    ```
```bash
{
  "categories": [
    "Science", 
    "Art", 
    "Geography", 
    "History", 
    "Entertainment", 
    "Sports"
  ], 
  "current_category": 4, 
  "page_index": 2, 
  "questions": [
    {
      "answer": "Agra", 
      "category": 3, 
      "difficulty": 2, 
      "id": 15, 
      "question": "The Taj Mahal is located in which Indian city?"
    }, 
    ...
  ], 
  "total_questions": 19
}
```

### DELETE /api/questions/{question_id}


* General
    - Delete a question with the provided question id
* Sample
    ```curl -X DELETE http://127.0.0.1:5000/api/questions/2 ```
* If successfuly, eturn
```bash
{
    "message": "Question deleted!",
    "question_id": 2
}
```
* if failed, return ``` 500 ``` error code.

### POST /api/questions/create

* General
    - Create a new question with the provided parameters
* Request body
    - Type: Json object
    - Sample: 
    ```bash 
    {
        "question": "how old was michael jackson when he died",
        "answer":"50",
        "difficulty": 2, 
        "category": 3
    } 
    ``` 
* Sample: 
```bash
curl --request POST --header "Content-Type: application/json" --data '{"question":"how old", "answer":"50", "difficulty":2, "category":3}' http://127.0.0.1:5000/api/questions/create
```
If successful, return
```bash
{
  "details": "Question: how old", 
  "status": "Create Suceeded!"
}
```

### POST /api/questions/search
* General
    - Return a list of questions by the provided search keywords/terms.

* Sample: 
```bash
curl --request POST --header "Content-Type: application/json" --data '{"searchTerm":"how old"}' http://127.0.0.1:5000/api/questions/search
```
If successful, return (questions may be an empty array)
```bash
{
  "current_category": 2, 
  "questions": [
    {
      "answer": "50", 
      "category": 3, 
      "difficulty": 2, 
      "id": 43, 
      "question": "how old"
    }
  ], 
  "total_questions": 1
}
```

### GET /api/categories/{category_id}/questions
* General
    - Return a list of questions by the provided category id

* Sample: 
```bash
curl --request GET http://127.0.0.1:5000/api/categories/3/questions
```
```bash
{
  "current_category": 3, 
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
    ...
  ], 
  "total_questions": 4
}
```

### POST /api/quizzes 

* General
    - Return one question based on the provided previous question IDs and category
    - Result qestion is randomly selected and not in the previous question IDs

* Sample
```bash
curl --request POST --header "Content-Type: application/json" --data '{"previous_questions":[3, 7, 10], "quiz_category":null }' http://127.0.0.1:5000/api/quizzes
```
Return
```bash
{
  "previousQuestions": [
    3, 
    7, 
    10
  ], 
  "question": {
    "answer": "Scarab", 
    "category": 4, 
    "difficulty": 4, 
    "id": 23, 
    "question": "Which dung beetle was worshipped by the ancient Egyptians?"
  }
}
```
