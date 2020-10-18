from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class Professor(db.Model):
    role = db.Column(db.Integer, default = 0)
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True)
    password_hash = db.Column(db.String(128))
    firstname = db.Column(db.String(64))
    lastname = db.Column(db.String(64))
    wsuid = db.Column(db.String(8), unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    phone = db.Column(db.String(10), unique=True)

    def __repr__(self):
        return '<Prof {} - {};>'.format(self.id, self.username)

    def get_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    #They must be able to enter courses they are teaching [db relationship?]

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
