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
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.mock_question = {
            'question':'Mock Question',
            'answer':'Mock Answer',
            'difficulty':3,
            'category': 3
        }
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    # fetch the mock question from db
    def get_mock_question_from_db(self):
        mock = Question.query.filter(Question.question==self.mock_question['question'],
                                        Question.answer==self.mock_question['answer']).all()
        if mock is not None and len(mock) > 0:
            return mock[0]
        else:
            return None

    def add_mock_question_to_db(self):
        return self.client().post('/api/questions/create', json=self.mock_question)

    def delete_mock_question_in_db(self):
        mock = self.get_mock_question_from_db()
        if mock is not None:
            question_id = mock.id
            return self.client().delete('/api/questions/{}'.format(question_id))
        else: 
            return None

    # get all categories
    def test_get_all_categories(self):
        res = self.client().get('/api/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['categories'])>0)

    # test get questions by page
    def test_get_questions_by_page(self):
        res = self.client().get('/api/questions?page=2')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['questions'])>0)

    # test page error handler
    def test_get_questions_by_page_error_handlers(self):
        res = self.client().get('/api/questions?page=100')
        self.assertEqual(res.status_code, 404)

    # test deleting a question
    def test_delete_question(self):
        mock = self.get_mock_question_from_db()
        if mock is None: 
            self.add_mock_question_to_db()
            mock = self.get_mock_question_from_db()
        
        question_id = mock.id
        print("Mock Question id", question_id)
        self.assertIsNotNone(question_id)

        url = '/api/questions/{}'.format(question_id)
        print("Delete url ", url)
        res = self.client().delete(url)
        self.assertEqual(res.status_code, 200)

        question = Question.query.get(question_id)
        self.assertIsNone(question)

    # test adding a question
    def test_create_question(self):
        oldQuestions = Question.query.all()

        # add a new question
        res = self.add_mock_question_to_db()
        self.assertEqual(res.status_code, 200)

        # new question list should be longer
        newQuestions = Question.query.all()
        self.assertTrue(len(oldQuestions) < len(newQuestions))

        # make sure the mock question exist in db
        mock = self.get_mock_question_from_db()
        self.assertIsNotNone(mock)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()