import os
from flask import Flask, render_template, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink, db
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app, resources={r"/api/*": {"origins": "*"}})

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
#db_drop_and_create_all()

@app.after_request 
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PUT, PATCH, DELETE, OPTIONS')
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/')
def index():
    return jsonify({
        "Index": "HOME"
    })

## ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['GET'])
def get_drinks():
    drinks = Drink.query.all()

    drinks_result = []

    if drinks is not None and len(drinks) > 0:
        for drink in drinks:
            drinks_result.append(drink.short())
    
    return jsonify({
        "success": True,
        "drinks": drinks_result
    })


'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks-detail', methods=['GET'])
def get_drinks_detail():
    drinks = Drink.query.all()

    drinks_result = []

    if drinks is not None and len(drinks) > 0:
        for drink in drinks:
            drinks_result.append(drink.long())
    
    return jsonify({
        "success": True,
        "drinks": drinks_result
    })

'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['POST'])
def create_drink():
    details = request.json
    
    key_title = 'title'
    key_recipe = 'recipe'

    if not key_title in details or not key_recipe in details:
        abort(422)

    str_recipe = json.dumps(details[key_recipe])
    success = True

    try:
        drink = Drink(title=details[key_title], recipe=str_recipe)
        drink.insert()
    except():
        success = False
    finally:
        db.session.close()

    result = jsonify({
      "success": success,
      "drinks": str_recipe
    })
    
    return result
'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
def update_drink(drink_id):
    target_drink = Drink.query.get(drink_id)

    if target_drink is None: 
        abort(404)
    
    new_drink = request.json
    if new_drink is None: 
        abort(422)

    success = True
    try:
        target_drink.title = new_drink['title']
        target_drink.recipe = json.dumps(new_drink['recipe'])
        target_drink.update()
    except():
        success = False
    finally:
        db.session.close()

    return jsonify({
        "success": success, 
        "drinks": target_drink.long()
    })

'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:drink_id>', methods=['DELETE'])
def delete_drink(drink_id):
    target_drink = Drink.query.get(drink_id)

    if target_drink is None:
        abort(404)
    
    success = True
    try:
        target_drink.delete()
    except():
        success = False
    finally:
        db.session.close()

    return jsonify({
        "success": success,
        "delete": drink_id
    })
    


## Error Handling
'''
Example error handling for unprocessable entity
'''
@app.errorhandler(422)
def error_unprocessable(error):
    return jsonify({
                    "success": False, 
                    "error": 422,
                    "message": "unprocessable"
                    }), 422

'''
@TODO implement error handler for 404
    error handler should conform to general task above 
'''
@app.errorhandler(404)
def error_not_found(error):
    return jsonify({
      "success": False,
      "error": 404,
      "message": "Not found!"
    }), 404

@app.errorhandler(403)
def error_unauthorized(error):
    return jsonify({
      "success": False,
      "error": 403,
      "message": "Unauthorized!"
    }), 403

@app.errorhandler(400)
def error_bad_request(error):
    return jsonify({
      "success": False,
      "error": 400,
      "message": "Bad request!"
    }), 400
  
@app.errorhandler(405)
def error_not_allowed(error):
    return jsonify({
      "success": False,
      "error": 405,
      "message": "Method not allowed!"
    }), 405

@app.errorhandler(500)
def error_server(error):
    return jsonify({
      "success": False,
      "error": 500,
      "message": "Internal server error."
    }), 500

'''
@TODO implement error handler for AuthError
    error handler should conform to general task above 
'''