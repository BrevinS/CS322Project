from datetime import datetime, timedelta
import unittest
from app import app,db
from app.models import Professor, Student, Course

class ModelTestObject(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    #def test_password_hashing(self):
    #    p = Professor(username)
    #def test_createcourse(self):
    #    m1 =  
