from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

@login.user_loader
def load_user(id):
    return Student.query.get(int(id))

applied = db.Table('applied',
    db.Column('studentid', db.Integer, db.ForeignKey('student.id')),
    db.Column('courseid', db.Integer, db.ForeignKey('course.id'))
)

class Professor(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(32), unique=True)
    password_hash = db.Column(db.String(128))
    firstname = db.Column(db.String(64))
    lastname = db.Column(db.String(64))
    wsuid = db.Column(db.String(8), unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    phone = db.Column(db.String(10), unique=True)
    def returnrole(self):
        return 1

    def __repr__(self):
        return '<Prof {} - {};>'.format(self.firstname, self.lastname)

    def get_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    #They must be able to enter courses they are teaching [db relationship?]

class Student(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(32), unique=True)
    password_hash = db.Column(db.String(128))
    firstname = db.Column(db.String(64))
    lastname = db.Column(db.String(64))
    wsuid = db.Column(db.String(8), unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    phone = db.Column(db.String(10), unique=True)

    major = db.Column(db.Integer)
    c_gpa = db.Column(db.Float)
    grad_date = db.Column(db.String(32))

    pendingapps = db.relationship ('Course', secondary = applied,
                            primaryjoin=(applied.c.studentid == id),
                            backref=db.backref('applied', lazy='dynamic'), lazy='dynamic')
    def returnrole(self):
        return 0

    def apply(self, newapp):
        if not self.has_applied(newapp):
            self.pendingapps.append(newapp)

    def is_applied(self, newapp):
        return self.pendingapps.filter(applied.c.courseid == newapp.id).count() > 0

    def unapply(self, newapp):
        if self.is_applied(newapp):
            self.pendingapps.remove(newapp)

    def __repr__(self):
        return '<Stud {} - {};>'.format(self.firstname, self.lastname)

    def get_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    coursenum = db.Column(db.String(3))  
    title = db.Column(db.String(150))
    num_ta = db.Column(db.Integer, default = 1)
    min_gpa = db.Column(db.Float)
    min_grade = db.Column(db.Integer)

    ta_apps = db.relationship ('Student', secondary = applied, 
                            primaryjoin=(applied.c.courseid == id),
                            backref=db.backref('applied', lazy='dynamic'), lazy='dynamic') 


    
