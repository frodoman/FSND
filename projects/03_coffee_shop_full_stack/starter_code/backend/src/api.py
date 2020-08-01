import os
from flask import Flask, render_template, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink, db
from .auth.auth import AuthError, requires_auth, Permission

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
@requires_auth(Permission.GET_DRINKT_DETAILS)
def get_drinks_detail(jwt):
    drinks = Drink.query.all()

    drinks_result = []
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
@requires_auth(Permission.POST_DRINKS)
def create_drink(jwt):
    details = request.json
    
    key_title = 'title'
    key_recipe = 'recipe'

    if details is None or not key_title in details or not key_recipe in details:
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

    return jsonify({
            "success": success,
            "drinks": str_recipe
            })

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
@requires_auth(Permission.UPDATE_DRINKS)
def update_drink(jwt, drink_id):
    target_drink = Drink.query.get(drink_id)

    if target_drink is None: 
        abort(404)
    
    key_title = 'title'
    key_recipe = 'recipe'
    drink_details = target_drink.long()

    new_drink = request.json
    if new_drink is None or (key_title not in new_drink and key_recipe not in new_drink): 
        abort(422)

    success = True
    try:
        if key_title in new_drink:
            target_drink.title = new_drink[key_title]
        if key_recipe in new_drink:
            target_drink.recipe = json.dumps(new_drink[key_recipe])

        target_drink.update()
    except():
        success = False
    finally:
        db.session.close()

    return jsonify({
        "success": success, 
        "drinks": [drink_details]
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
@requires_auth(Permission.DELETE_DRINKS)
def delete_drink(jwt, drink_id):
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

@app.errorhandler(401)
def error_unauthorized(error):
    return jsonify({
      "success": False,
      "error": 401,
      "message": "Unauthorized!"
    }), 401

@app.errorhandler(403)
def error_not_permitted(error):
    return jsonify({
      "success": False,
      "error": 403,
      "message": "Not permitted!"
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
@app.errorhandler(AuthError)
def handle_auth_error(error):
    return jsonify({
        "success": False,
        "error": error.status_code,
        "message": error.error['description']
    })