import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
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

    # Setup CORS : Allow all origins for all routes
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
        request: the HTTP request to extract the page argument or use a default of 1
        collection (list): a list of the items to be paginated
        count (int): number of items to be returned per page (currently set to a default of 10)
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
        '''
        Retreives all available categories
        '''

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
        '''
        Retrieves all available questions
        '''

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

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        '''
        Deletes a question by its ID
        '''

        question = Question.query.get(question_id)

        if not question:
            abort(404)

        try:
            question.delete()

        except:
            abort(422)

        return jsonify({
            "success": True,
            "question_id": question.id,
        }), 200


    '''
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    '''
    @app.route('/questions', methods=['POST'])
    def add_question():
        '''
        Adds a question, its answer, category and difficulty
        '''

        question_data = request.json
        question = question_data.get('question')
        answer = question_data.get('answer')
        difficulty = question_data.get('difficulty')
        category = question_data.get('category')

        # Raise Bad Request if request body is missing the required data
        if not all([question, answer, difficulty, category]):
            abort(400)

        try:
            new_question = Question(question, answer, category, difficulty)
            new_question.insert()

        except:
            abort(422)

        return jsonify({
            "success": True,
        }), 200


    '''
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    '''
    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        '''
        Retrieves all questions that containts the search term
        '''

        data = request.json

        try:
            search_term = data['searchTerm']

        except KeyError:
            # Raise a Bad Request if searchTerm is not in request body
            abort(400)

        try:
            questions = Question.query.filter(Question.question.ilike('%{}%'.format(search_term))).all()
            paginated_questions = paginate(request, questions)

        except:
            abort(422)

        return jsonify({
            "success": True,
            "questions": [question.format() for question in paginated_questions],
            "total_questions": len(questions),
        }), 200


    '''
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    '''
    @app.route('/categories/<int:category_id>/questions')
    def get_questions_by_category(category_id):
        '''
        Retrieves questions based on the selected category
        '''

        questions = Question.query.filter_by(category=category_id).all()

        if not questions:
            abort(404)

        paginated_questions = paginate(request, questions)

        if not paginated_questions:
            abort(404)

        return jsonify({
            "success": True,
            "questions": [question.format() for question in paginated_questions],
            "total_questions": len(questions),
            "current_category": category_id,
        }), 200


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
    @app.route('/quizzes/play', methods=['POST'])
    def play_quiz():
        '''
        Starts a quiz
        '''

        data = request.json

        # Raise Bad Request if request body is missing the required data
        if not all(key in data for key in ['quiz_category', 'previous_questions']):
            abort(400)

        previous_questions = data.get('previous_questions')
        quiz_category = data.get('quiz_category')

        try:
            # Filter out all previously used questions
            possible_questions = Question.query.filter(Question.id.notin_(previous_questions))

            # Filter only questions from the selected category if not ALL categories is selected
            if quiz_category.get('id') != 0:
                possible_questions = possible_questions.filter(Question.category == quiz_category['id'])

            # Randomize the returned question to allow for variation in quizzes
            next_question = possible_questions.order_by(func.random()).first()

            next_question = next_question.format() if next_question else None

        except:
            abort(422)

        return jsonify({
            "success": True,
            "previous_questions": previous_questions,
            "question": next_question,
        }), 200

    '''
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    '''

    # Error handlers for HTTP error responses

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
