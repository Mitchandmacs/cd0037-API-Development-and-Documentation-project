import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

import random

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format(
            'localhost:5432',
            self.database_name)
        setup_db(self.app, self.database_path)

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
    Tests for /questions
    GET
        - GET, no params
        - GET, Paginated
    POST
        - Create
        - Search
    """
    def test_retrieve_questions(self):
        res = self.client().get("/questions")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["totalQuestions"])

    def test_retrieve_questions_paginated(self):
        res = self.client().get("/questions?page=1")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["totalQuestions"])

    def test_retrieve_questions_paginated_oob(self):
        res = self.client().get("/questions?page=182")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)

    def test_create_question(self):
        res = self.client().post("/questions",
                                 json={"question": "What's my age again?",
                                       "answer": "23", "difficulty": 1,
                                       "category": 5})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)

    def test_create_question_error(self):
        res = self.client().post("/questions",
                                 json={"question": "What's my age again?",
                                       "difficulty": 1, "category": 5})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)

    def test_search_question(self):
        res = self.client().post("/questions", json={"searchTerm": "age"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)

    def test_search_question_noResults(self):
        res = self.client().post("/questions",
                                 json={"searchTerm":
                                       "stringThatIsUnlikelyToNaturallyOccur"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)

    """
    Tests for /questions/{question_id}
    DELETE
    """
    def test_delete_questionById(self):
        # make this test idempotent
        # create a question
        res = self.client().post("/questions",
                                 json={"question": "testQuestion",
                                       "answer": "42",
                                       "difficulty": 1,
                                       "category": 5})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

        # find that question
        res = self.client().post("/questions",
                                 json={"searchTerm": "testQuestion"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        deleteId = data["questions"][0]["id"]

        # delete this test question
        res = self.client().delete(f"/questions/{deleteId}")
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data["deleted"], deleteId)

    def test_delete_questionById_error(self):
        # delete this test question
        res = self.client().delete("/questions/182")
        self.assertEqual(res.status_code, 404)

    """
    Tests for /categories/{category_id}/questions
    GET
    """
    def test_get_questions_for_category(self):
        categoryId = random.randint(1, 6)
        res = self.client().get(f"/categories/{categoryId}/questions")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["totalQuestions"])

    def test_get_questions_for_category_error(self):
        res = self.client().get("/categories/100/questions")
        self.assertEqual(res.status_code, 404)

    """
    Tests for /quizzes
    GET
    """
    def test_quizzes_noBody(self):
        res = self.client().post("/quizzes")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)

    def test_quizzes_body_gameStart(self):
        res = self.client().post("/quizzes",
                                 json={"previous_questions": [],
                                       "quiz_category": {"id": 1}})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["question"])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
