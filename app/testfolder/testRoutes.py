import os
import tempfile
import pytest
from config import basedir
from app import app,db,login
from app.models import Professor, Student, Course

@pytest.fixture(scope='module')
def test_client(request):
    #re-configure the app for tests
    app.config.update(
        SECRET_KEY = 'bad-bad-key',
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'test.db'),
        SQLALCHEMY_TRACK_MODIFICATIONS = False,
        WTF_CSRF_ENABLED = False,
        DEBUG = True,
        TESTING = True,
    )
    db.init_app(app)
    testing_client = app.test_client()
 
    ctx = app.app_context()
    ctx.push()
 
    yield  testing_client 
    ctx.pop()

@pytest.fixture
def newuser():
    u = Student(username='BrevinS', email='brevin.simon@wsu.edu', firstname='Brevin', lastname='Simon')
    u.get_password('cat1234')
    return u

@pytest.fixture
def init_database(request,test_client):
    db.create_all()
    if Tag.query.count() == 0:
        tags = ['Min-GPA 3.0+', 'Min-GPA 3.5+', 'Min-Grade A', 'Min-Grade B', 'Prior-TA-Exper.', 'Senior', 'Graduate', 'Junior+']
        for t in tags:
            db.session.add(Tag(name=t))
        db.session.commit()
    #add a user    
    u = Student(username='slash', firstname='Jane', lastname='Doe')
    u.get_password('dog1234')
    db.session.add(u)
    db.session.commit()
    #this does something
    yield 
    db.drop_all()

def test_register(request,test_client,init_database):
    response = test_client.post('/profregister', 
                          data=dict(username='prof1', email='mike.doe@wsu.edu',password="bad-bad-password",password2="bad-bad-password", firstname='Mike',lastname='Doe'),
                          follow_redirects = True)
    assert response.status_code == 200

    p = db.session.query(Professor).filter(Professor.username=='prof1')
    assert s.first().lastname == 'Doe'
    assert s.count() == 1
    assert b"Congrats you are a registered professor" in response.data

def test_invalidlogin(request,test_client,init_database):
    response = test_client.post('/login', 
                          data=dict(username='BrevinS', password='cat12345', remember_me=False),
                          follow_redirects = True)
    assert response.status_code == 200
    assert b"Invalid username or password" in response.data

def test_login_logout(request,test_client,init_database):
    response = test_client.post('/login', 
                          data=dict(username='BrevinS', password='cat1234', remember_me=False),
                          follow_redirects = True)
    assert response.status_code == 200

    response = test_client.get('/logout',                       
                          follow_redirects = True)
    assert response.status_code == 200
    assert b"Sign In" in response.data
    assert b"Please log in to access this page." in response.data   

