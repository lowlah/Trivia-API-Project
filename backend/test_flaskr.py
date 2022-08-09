import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import true

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format(
            "student", "student", "localhost:5432", self.database_name
        )
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.new_question = {"question": "The movie gray man was distributed by which company?",
         "answer": "Netflix",
         "difficulty": 1,
         "category": 5}    

    
    def tearDown(self):
        """Executed after reach test"""
        pass

    #-----------------------------------------------------------------
    # Test  endpoints for successful behaviors and for expected errors
    # ----------------------------------------------------------------

    # test for successful  display of questions
    def test_get_paginated_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
        self.assertTrue(len(data['categories']))

    
    # test:expected error if a page that does not exist tries to be accessed
    def test_404_requesting_questions_beyond_valid_page(self):
        res = self.client().get('/questions?page=900')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
           
        
    # test success on display of categories
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['categories']))
    
    # test if wrong method is used(should be get) to display categories
    def test_error_post_categories(self):
        res = self.client().post('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['message'], 'Method Not allowed') 

    
    # test : successful deletions happens when the created question is deleted
    def test_delete_question(self):
        # creates a new question
        question = Question(question='The longest river in the world?', 
                            answer='Nile',
                            difficulty=1, 
                            category=3
        
                            )                   
        question.insert()
        # id of the new question
        new_id = question.id

        res = self.client().delete(f'/questions/{new_id}')
        data = json.loads(res.data)
        
        # checks if it has been deleted
        question = Question.query.filter(Question.id == 1).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], (new_id))
        self.assertEqual(question, None)     
    
    
    # test : returns an error if you try to delete a non existent question
    def test_422_question_to_delete_does_not_exist(self):
        res = self.client().delete('/questions/999')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    
    # test: success if a new question was posted
    def create_new_question(self):
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)
        #gets mumber of questions after creating a new questions
        questions = len(Question.query.all())

        self.assertTrue(res.status_code, 200)
        self.assertTrue(data['success'], True)
        self.assertEqual(data['message'], 'Question successfully created!')
        self.assertEqual(data['total_questions'], questions)
    
    # test: returns error if fields(question,sanswer,difficulty,category) are left empty
    def test_400_create_question_with_fields_empty(self):
        res = self.client().post('/questions', json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad request')

    # test: succesful if it returns the search term
    def test_search_question(self):
        res = self.client().post('/questions/search', json={'searchTerm': 'royal'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True) 
    
    # returns error if no search result
    def test_404_search_questions(self):
        response = self.client().post('/questions/search', json={ 'searchTerm': ''})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)

    # test: succesfully get questions based on a category
    def test_get_questions_by_category(self):
        res = self.client().get('/categories/2/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'])


    # test: error if questions based on a category does not exist
    def test_404_get_questions_per_category(self):
        res = self.client().get('/categories/10/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)

    # test: success if parameters present
    def test_play_quiz_1(self):
        res = self.client().post('/quizzes', json={"previous_questions": [], "quiz_category": {"type": "Geography", "id": "3"}})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)         
        self.assertIsNotNone(data['question'])               
        self.assertEqual(data['question']['category'], 3)       
    
    # test: error if category is missing
    def test_422_get_quiz(self):
        res = self.client().post('/quizzes',json={'previous_questions': []})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
            
        
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()