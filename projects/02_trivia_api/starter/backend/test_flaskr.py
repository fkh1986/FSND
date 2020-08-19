import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}:{}@{}/{}".format('test', 'test', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.new_question = {
            "question": "How many colors are there in the rainbow?",
            "answer": "7 colors",
            "category": 1,
            "difficulty": 1,
        }

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])
        self.assertTrue(len(data['categories']))

    def test_get_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        questions = Question.query.all()
        categories = Category.query.all()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(len(data['questions']) <= 10)
        self.assertTrue(data['total_questions'])
        self.assertEqual(data['total_questions'], len(questions))
        self.assertTrue(data['current_category'])
        self.assertTrue(data['categories'])
        self.assertEqual(len(data['categories']), len(categories))

    def test_get_category_questions(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        questions = Question.query.filter_by(category=1).all()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(len(data['questions']) <= 10)
        self.assertTrue(data['total_questions'])
        self.assertEqual(data['total_questions'], len(questions))
        self.assertEqual(data['current_category'], 1)

    def test_add_question(self):
        res = self.client().post('/questions', json=self.new_question, content_type='application/json')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_question(self):
        question = Question(**self.new_question)
        question.insert()
        question_id = question.id

        res = self.client().delete('/questions/{}'.format(question_id))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['question_id'], question_id)

    def test_search_questions(self):
        search_term = 'title'
        questions = Question.query.filter(Question.question.ilike('%{}%'.format(search_term))).all()

        res = self.client().post('/search', json={'searchTerm':search_term})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertEqual(len(data['questions']), len(questions))

    def test_play_quiz(self):
        quiz_info = {
            'previous_questions': [],
            'quiz_category': {"id": 0, "type": "all"},
        }
        res = self.client().post('/quizzes', json=quiz_info)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['previous_questions'], quiz_info['previous_questions'])
        self.assertTrue(data['question'])
        self.assertTrue(data['question']['id'] not in quiz_info['previous_questions'])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()