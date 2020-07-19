# Full Stack Trivia API Reference 

## Getting Started
* Base URl: Currently this app can only run locally. The backend is host at the default url: [http://127.0.0.1:5000/](http://127.0.0.1:5000/), which is configured as the proxy of the frontend app.
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
    - Return a list of supported question categories
    - Results will be an array of string objects
* Sample 
    ```bash
    curl http://127.0.0.1:5000/api/categories
    
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