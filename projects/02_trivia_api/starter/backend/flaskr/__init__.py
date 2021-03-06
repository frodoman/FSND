import os
from flask import Flask, render_template, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import sys

from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  CORS(app, resources={r"/api/*": {"origins": "*"}})

  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request 
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PUT, PATCH, DELETE, OPTIONS')
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

  @app.route('/')
  def index():
    return render_template('home.html')

  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/api/categories', methods=['GET'])
  def get_all_categories():
    formated_categories = []
    categories = Category.query.all()
    if categories is not None:
      formated_categories = [oneCate.type for oneCate in categories]

    return jsonify({
      "categories": formated_categories
    })
  
  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route('/api/questions', methods=['GET'])
  def get_questions_by_page():

    # prepare indexes
    page_index = request.args.get('page', 1, type=int)
    start = (page_index - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    # find all the questions
    questions = Question.query.order_by(Question.id).all()
    total_questions = len(questions)

    # format questions
    if questions is None or len(questions) < start:
      abort(404)
    # filter all questions for the current page index
    else:
      formated_questions = [question.format() for question in questions[start: end]]

    # categories
    formated_categories = []
    categories = Category.query.all()
    if categories is not None:
      formated_categories = [oneCate.type for oneCate in categories]

    result = {
      "questions": formated_questions,
      "total_questions": total_questions,
      "categories": formated_categories,
      "current_category": formated_questions[-1]['category'],
      "page_index": page_index
    }
    return jsonify(result)

  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/api/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    error = False
    try:
      question = Question.query.get(question_id) 
      if question is None:
        abort(404)

      db.session.delete(question)
      db.session.commit()
    except():
      db.session.rollback()
      error = True
    finally:
      db.session.close()

    if error: 
      abort(500)
    else: 
      return jsonify({
      "message": "Question deleted!",
      "question_id": question_id
      })


  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/api/questions/create', methods=['POST'])
  def create_question():
    details = request.json

    if not is_valid_question(details):
      abort(422)

    try:
      question = Question(question = details['question'],
                          answer = details['answer'],
                          difficulty = int(details['difficulty']),
                          category = int(details['category']))
      
      db.session.add(question)
      db.session.commit()
    except:
      db.session.rollback()   
      abort(500)
    finally:
      db.session.close()

    return jsonify({
      "status": "Create Suceeded!",
      "details": "Question: " + details['question'] + ""
    })

  def is_valid_question(dict_question):
    if 'question' in dict_question and 'answer' in dict_question and 'difficulty' in dict_question and 'category' in dict_question: 
       return True
    else:
      return False

  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route('/api/questions/search', methods=['POST'])
  def search_question():

    # make sure we have valid search terms
    key = 'searchTerm'
    if key in request.json:
      searchTerms = request.json[key]
    else: 
      abort(422)
    
    if searchTerms is None or len(searchTerms) == 0:
      abort(422)
    
    # find the question by search terms
    keywords = "%" + searchTerms + "%"
    results = Question.query.filter(Question.question.ilike(keywords)).order_by(Question.question).all()

    viewItems = []
    if len(results) > 0:
      for result in results:
        viewItems.append(result.format())

    return jsonify({
      'questions': viewItems,
      'total_questions': len(viewItems),
      'current_category': 2,
    })
  

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  
  @app.route('/api/categories/<int:category_id>/questions', methods=['GET'])
  def get_questions_by_category(category_id):

    db_questions = Question.query.filter(Question.category==category_id).all()

    if db_questions is None or len(db_questions) == 0:
      abort(404)

    formated_questions = [oneQuestion.format() for oneQuestion in db_questions]

    result = {
      "questions": formated_questions,
      "total_questions": len(formated_questions),
      "current_category": category_id
    }

    return jsonify(result)

  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/api/quizzes', methods=['POST'])
  def play_quizzes():
    request_data = request.json
    key_previous = 'previous_questions'
    key_category = 'quiz_category'

    previous = None
    if key_previous in request_data:
      previous = request_data[key_previous]

    category = None
    if key_category in request_data:
      category = request_data[key_category]

    question = None
    # category is provided
    if category is not None:
      query = Question.query.filter(Question.category==category)
      # filter out previouse questions
      if previous is not None and len(previous) > 0:
        questions = query.filter(Question.id.notin_(previous)).all()
        if questions is not None and len(questions) > 0:
          question = random.choice(questions)
      # randomly return a question when no prameters are provided
      else: 
        question = random.choice(query.all())
    
    # category is not provided
    else: 
      query = Question.query
      # filter out previouse questions
      if previous is not None and len(previous) > 0: 
        questions = query.filter(Question.id.notin_(previous)).all()
        if questions is not None and len(questions) > 0:
          question = random.choice(questions)
      # randomly return a question when no prameters are provided
      else: 
        question = random.choice(query.all())
    
    format_question:dict = None
    if question is not None: 
      format_question = question.format()
    
    return jsonify({
      "previousQuestions": previous, 
      "question": format_question
    })

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(400)
  def error_not_found(error):
    return jsonify({
      "success": False,
      "error": 400,
      "message": "Bad request!"
    }), 400

  @app.errorhandler(404)
  def error_not_found(error):
    return jsonify({
      "success": False,
      "error": 404,
      "message": "Not found!"
    }), 404
  
  @app.errorhandler(405)
  def error_not_found(error):
    return jsonify({
      "success": False,
      "error": 405,
      "message": "Method not allowed!"
    }), 405

  @app.errorhandler(422)
  def error_not_found(error):
    return jsonify({
      "success": False,
      "error": 422,
      "message": "Unprocessable Entity!"
    }), 422

  @app.errorhandler(500)
  def error_server(error):
    return jsonify({
      "success": False,
      "error": 500,
      "message": "Internal server error."
    }), 500

  return app

    