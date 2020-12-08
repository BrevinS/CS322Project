from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

@login.user_loader
def load_user(id):
    return Professor.query.get(int(id))
    #return Student.query.get(int(id))

#Relationships
courseTags = db.Table('courseTags',
    db.Column('course_id', db.Integer, db.ForeignKey('course.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
    )
    
applied = db.Table('applied',
    db.Column('studentid', db.Integer, db.ForeignKey('student.id')),
    db.Column('courseid', db.Integer, db.ForeignKey('course.id'))
    )

accepted = db.Table('accepted',
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
    posts = db.relationship('Course', backref='writer', lazy='dynamic')

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

    accepted = db.relationship('Course', secondary = accepted,
                            primaryjoin=(accepted.c.studentid == id),
                            backref=db.backref('accepted', lazy='dynamic'), lazy='dynamic')

    pendingapps = db.relationship('Course', secondary = applied,
                            primaryjoin=(applied.c.studentid == id),
                            backref=db.backref('applied', lazy='dynamic'), lazy='dynamic')

    def returnrole(self):
        return 0

    def accepted(self, newapp):
        if not self.is_ta(newapp):
            self.accepted.append(newapp)

    def apply(self, newapp):
        if not self.is_applied(newapp):
            self.pendingapps.append(newapp)

    def is_ta(self, newapp):
        return self.accepted.filter(accepted.c.courseid == newapp.id).count() > 0

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

    professor_id = db.Column(db.Integer, db.ForeignKey('professor.id'))

    accepted_tas = db.relationship('Student', secondary = accepted, 
                            primaryjoin=(accepted.c.courseid == id),
                            backref=db.backref('accepted', lazy='dynamic'), lazy='dynamic') 

    ta_apps = db.relationship('Student', secondary = applied, 
                            primaryjoin=(applied.c.courseid == id),
                            backref=db.backref('applied', lazy='dynamic'), lazy='dynamic') 

    tags = db.relationship('Tag', secondary=courseTags,
                            primaryjoin=(courseTags.c.course_id == id),
                            backref=db.backref('courseTags', lazy='dynamic'), lazy='dynamic')

    def accepted(self, studentTA):
        self.accepted_tas.append(studentTA)

#Requirements in the form of tags
class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    courses = db.relationship('Course', secondary=courseTags,
                               primaryjoin=(courseTags.c.tag_id == id),
                               backref=db.backref('courseTags', lazy='dynamic'),
                               lazy='dynamic')

