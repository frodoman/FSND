# Full Stack Trivia API Reference 

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


