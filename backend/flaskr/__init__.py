import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_
from flask_cors import CORS

import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]
    return current_questions


def get_and_format_categories():
    selection = Category.query.order_by(Category.id).all()
    # Format as one object with n keys rather than an array of n objects
    categories = {}
    for category in selection:
        categories[category.id] = category.type
    return categories


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    # @TODO: Set up CORS. Allow '*' for origins.
    # Delete the sample route after completing the TODOs
    CORS(app)

    # @TODO: Use the after_request decorator to set Access-Control-Allow
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,POST,DELETE"
        )
        return response

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route("/categories")
    def retrieve_categories():
        categories = get_and_format_categories()

        if len(categories) == 0:
            abort(404)

        return jsonify(
            {
                "categories": categories
            }
        )

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at
    the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route("/questions")
    def retrieve_questions():
        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, selection)

        if len(current_questions) == 0:
            abort(404)

        return jsonify(
            {
                "questions": current_questions,
                "totalQuestions": len(selection),
                "categories": get_and_format_categories(),
                "currentCategory": ""
            }
        )

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question,
    the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_question(question_id):
        question = Question.query.filter(
            Question.id == question_id
            ).one_or_none()
        if question is None:
            abort(404)

        question.delete()

        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, selection)

        return jsonify(
            {
                "deleted": question_id,
                "questions": current_questions,
                "totalQuestions": len(selection),
            }
        )

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear
    at the end of the last page
    of the questions list in the "List" tab.

    AND

    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.
    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route("/questions", methods=["POST"])
    def create_question():
        body = request.get_json()

        # Determine if we're searching or creating
        search = body.get("searchTerm", None)

        if search:
            selection = Question.query.filter(
                            Question.question.ilike("%{}%".format(search))
                            ).all()

            if selection is None:
                abort(404)

            current_questions = paginate_questions(request, selection)

            if len(current_questions) == 0:
                abort(404)

            return jsonify({
                "questions": current_questions,
                "totalQuestions": len(selection),
                "currentCategory": ""
            })

        else:
            new_question = body.get("question", None)
            new_answer = body.get("answer", None)
            new_difficulty = body.get("difficulty", None)
            new_category = body.get("category", None)

            if (
                    (new_question is None) or (new_answer is None) or
                    (new_difficulty is None) or (new_category is None)):
                abort(400)

            question = Question(question=new_question,
                                answer=new_answer,
                                difficulty=new_difficulty,
                                category=new_category)
            question.insert()

            return jsonify({})

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route("/categories/<int:category_id>/questions")
    def retrieve_questions_by_category(category_id):
        selection = Question.query.filter(
                        category_id == Question.category).all()
        current_questions = paginate_questions(request, selection)

        category = Category.query.filter(
                    category_id == Category.id).one_or_none()

        # Ensure a valid cateory was entered
        if ((len(current_questions) == 0) or (category is None)):
            abort(404)

        return jsonify(
            {
                "questions": current_questions,
                "totalQuestions": len(selection),
                "currentCategory": category.type
            }
        )

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route("/quizzes", methods=["POST"])
    def play_quizz():
        body = request.get_json()

        if body is not None:
            previous_questions = body.get("previous_questions", None)
            category = body.get("quiz_category", None)
            if (category is not None) and (previous_questions is not None):
                category_id = category["id"]
            else:
                abort(400)

            filters = []
            filters.append(Question.id.notin_(previous_questions))
            if category_id != 0:
                filters.append(Question.category == category["id"])

            selections = Question.query.filter(and_(*filters)).all()

            # If we've done all the questions from a category
            # Return an empty object which will force the UI to end game
            if len(selections) == 0:
                return jsonify({})

            questions = [question.format() for question in selections]

            return jsonify({
                "question": questions[random.randint(0, len(questions)-1)]
            })
        else:
            abort(400)

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(400)
    def bad_request(error):
        return (jsonify({"success": False,
                         "error": 400,
                         "message": "bad request"}),
                400,
                )

    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"success": False,
                     "error": 404,
                     "message": "resource not found"}),
            404,
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False,
                     "error": 422,
                     "message": "unprocessable"}),
            422,
        )

    @app.errorhandler(500)
    def bad_request(error):
        return (jsonify({"success": False,
                         "error": 500,
                         "message": "internal server error"}),
                500,
                )

    return app
