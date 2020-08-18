import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)

  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  cors = CORS(app, resources={r"*": {"origins":"*"}})

  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  def after_request(response):
    response.headers.set('Access-Control-Allow-Origin', '*')
    return response


  def paginate(request, collection, count=QUESTIONS_PER_PAGE):
    '''
    This is a helper function to paginate any collection returning a single page of items

    The function expects:
    collection (list): a list of the items to be paginated
    page (int): an integer indicating the number of the page requested (returns first page if not provided)
    count (int): number of items to be returned (currently set to a default of 10)
    '''
    page = request.args.get('page', default=1, type=int)
    start = (page-1) * count
    end = start + count
    return collection[start:end]

  '''
  @TODO:
  Create an endpoint to handle GET requests
  for all available categories.
  '''
  @app.route('/categories')
  def get_categories():

    categories = Category.query.all()

    if not categories:
      abort(404)


    paginated_categories = paginate(request, categories)

    if not paginated_categories:
      abort(404)

    return jsonify({
        "success": True,
        "categories": {category.id: category.type.lower() for category in paginated_categories},
      }), 200

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
  @app.route('/questions')
  def get_questions():

    questions = Question.query.all()
    categories = Category.query.all()

    if not questions:
      abort(404)

    paginated_questions = paginate(request, questions)

    if not paginated_questions:
      abort(404)

    return jsonify({
        "success": True,
        "questions": [question.format() for question in paginated_questions],
        "total_questions": len(questions),
        "current_category": categories[0].id,
        "categories": {category.id: category.type.lower() for category in categories},
      }), 200


  '''
  @TODO:
  Create an endpoint to DELETE question using a question ID.

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page.
  '''

  '''
  @TODO:
  Create an endpoint to POST a new question,
  which will require the question and answer text,
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab,
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.
  '''

  '''
  @TODO:
  Create a POST endpoint to get questions based on a search term.
  It should return any questions for whom the search term
  is a substring of the question.

  TEST: Search by any phrase. The questions list will update to include
  only question that include that string within their question.
  Try using the word "title" to start.
  '''

  '''
  @TODO:
  Create a GET endpoint to get questions based on category.

  TEST: In the "List" tab / main screen, clicking on one of the
  categories in the left column will cause only questions of that
  category to be shown.
  '''


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

  '''
  @TODO:
  Create error handlers for all expected errors
  including 404 and 422.
  '''
  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "Bad request",
      }), 400

  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "Not found",
      }), 404

  @app.errorhandler(405)
  def invalid_method(error):
    return jsonify({
        "success": False,
        "error": 405,
        "message": "Method not allowed",
      }), 405

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "Unprocessable",
      }), 422

  return app
