import os
from flask import Flask, request, abort, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
import random

from models import setup_db, Question, Category

# limits result to just 10 per page 
QUESTIONS_PER_PAGE = 10

#method for pagination(as shown in class example) 
def paginate(request, selection):
    #gets arguments using page number
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions

def create_app(test_config=None):
    # creates and configures the app
    app = Flask(__name__)
    setup_db(app)
    #CORS(app)

    #---------------------------------------------------------------------------------------------------
    # Sets up CORS and allows access '*' for origins. Delete the sample route after completing the TODOs
    #---------------------------------------------------------------------------------------------------
    CORS(app, resources={'/': {'origins': '*'}})
    
    
    # CORS Headers: after_request decorator sets Access-Control-Allow
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,PATCH,DELETE,OPTIONS"
        )
        return response

    #-----------------------------------------------------------
    # endpoint handles get requests for all available categories
    #-----------------------------------------------------------

    @app.route('/categories')
    def get_categories():
        #queries category
        selection = Category.query.order_by(Category.id).all()
        result = {category.id: category.type for category in selection}
        #if no category, throw an error 
        if len(selection) == 0:
            abort(404)

        return jsonify(
            {
                'success': True,
                'categories': result
            }
        )    

    #@cross_origin sample route
    @app.route('/')
    def hello_world():
        return jsonify({'message':'HELLO, WORLD!'}) 

    """
    
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """

    @app.route('/questions')
    def get_questions():
        #queries question
        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate(request, selection)
        categories = Category.query.order_by(Category.type).all()
        result= {category.id: category.type for category in categories}
        #result =  [category.type for category in Category.query.all()]

        if len(current_questions) == 0:
            abort(404)

        # This endpoint should return a list of questions,
        # number of total questions, current category, categories.
        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(selection),
            'current_category': {},
            'categories': result
        })



    """
    
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    # ---------------------------------------------
    # endpoint deletes question using a question ID
    # ---------------------------------------------

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            #check question exists else return error 404
            question = Question.query.filter(Question.id == question_id).one_or_none()
            if question is None:
                abort(404)

            # deletes and paginates
            question.delete()
            selection = Question.query.order_by(Question.id).all()
            current_questions = paginate(request, selection)
            return jsonify(
                {
                    'success': True,
                    'deleted': question_id,
                    'questions': current_questions,
                    'total_questions': Question.query.count()
                }
            )
        # if a problem occurs when deleting, return this error
        except:
            abort(422)

    """
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    # -------------------------------
    # endpoint creates a new question
    # -------------------------------

    @app.route('/questions', methods=['POST'])
    def new_question():
        body = request.get_json()
        # if no question,reply,category,difficulty score,  throw an error    
        if not ('question' in body and 'answer' in body and 'difficulty' in body and 'category' in body):
            abort(400)

        new_question = body.get('question')
        new_answer = body.get('answer')
        new_difficulty = body.get('difficulty')
        new_category = body.get('category')

        '''
        # ensures no field is left empty
        if ((new_question is None) or (new_answer is None) or
                (new_difficulty is None) or (new_category is None)):
            flash("Please fill all fields !!!!!")
            abort(400)
        '''
        try:
            question = Question(question=new_question, answer=new_answer,difficulty=new_difficulty,category=new_category)
            question.insert()

            selection = Question.query.order_by(Question.id).all()
            current_questions = paginate(request, selection)

            return jsonify(
                {
                    'success': True,
                    'created': question.id,
                    'question_created': question.question,
                    'questions': current_questions,
                    'total_questions': Question.query.count()
                }
            )
        # if a problem occurs posting a new question return this error    
        except:
            abort(422)


    """
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    # ------------------------------------------------
    # POST endpoint gets question based on search term 
    # ------------------------------------------------

    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        # gets the  user input
        body = request.get_json()
        search = body.get('searchTerm', None)

        try:
            if search:
                selection = Question.query.filter(Question.question.ilike(f'%{search}%')).all()

            current_question = paginate(request, selection)
            return jsonify({
                'success': True,
                'questions':  current_question,
                'total_questions': len(selection),
                'current_category': None
            })
        # if a problem occurs throw this error    
        except:
            abort(404)

    """
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    #--------------------------------------------------
    # endpoint shows questions based on chosen category
    # --------------------------------------------------

    @app.route('/categories/<int:id>/questions')
    def get_questions_by_category(id):
        # gets category by id
        category = Category.query.filter_by(id=id).one_or_none()

        try:
            # gets  questions that matches the category
            selection = Question.query.filter_by(category=category.id).all()
            current_selection = paginate(request, selection)
            return jsonify({
                'success': True,
                'questions': current_selection,
                'total_questions': len(Question.query.all()),
                'current_category': category.type
            })
        # if a problem occurs give an error    
        except:
            abort(404)

    """

    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    # ------------------------------------------------------------
    # endpoint displays questions used in playing the quiz.It takes 
    # category and previous question parameters and returns random
    # random questions within the given category
    # ------------------------------------------------------------

    @app.route('/quizzes', methods=['POST'])
    def play_quiz():
        try:
            body = request.get_json()
            category = body.get('quiz_category')
            previous_questions = body.get('previous_questions')

            # If 'ALL' categories is selected,filter questions
            if category['type'] == 'click':
                questions = Question.query.filter(Question.id.notin_((previous_questions))).all()
                    
            # filter questions based on category selected
            else:
                questions = Question.query.filter_by(category=category['id']).filter(Question.id.notin_((previous_questions))).all()

            # randomly generate questions
            generate_question = questions[random.randrange(
                0, len(questions))].format() if len(questions) > 0 else None

            return jsonify({
                'success': True,
                'question': generate_question
            })
        except:
            abort(422)
    
    # ----------------------------------
    # Error handlers for expected errors
    # ----------------------------------

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'Error': 400,
            'message': 'Bad request'
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'Error': 404,
            'message': 'Resource Not Found'
        }), 404

    @app.errorhandler(422)
    def uprocessable(error):
        return jsonify({
            'success': False,
            'Error': 422,
            'message': 'Unable to process request'
        }), 422

    @app.errorhandler(405)
    def not_allowed(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': 'Method Not allowed'
        }), 405

    @app.errorhandler(500)
    def not_allowed(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'Internal server error'
        }), 500  

    return app

