from flask import render_template, flash, redirect, url_for, request
from app import app, db
from flask_sqlalchemy import sqlalchemy
from app.forms import StudentForm, ProfessorForm, CourseForm
from app.models import Student, Professor, Course

@app.before_first_request
def initDB(*args, **kwargs):
    db.create_all()

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    courses = Course.query.order_by(Course.coursenum).all()
    return render_template('studentInterface.html', courses=courses)

@app.route('/profregister', methods=['GET', 'POST'])
def profregister():
    form = ProfessorForm()
    if form.validate_on_submit():
        acc = Professor(username=form.username.data, email=form.email.data, firstname=form.firstname.data,
            lastname=form.lastname.data, wsuid=form.wsuid.data, phone=form.phone.data)
        acc.get_password(form.password2.data)
        db.session.add(acc)
        db.session.commit()
        flash('Congrats you are registered professor')
        ##REDIRECT SO THE TEACHER CAN CREATE COURSES
        return redirect(url_for('createclass'))
    return render_template('prof_reg.html', title='Register', form=form)

@app.route('/studregister', methods=['GET', 'POST'])
def studregister():
    form = StudentForm()
    if form.validate_on_submit():
        acc = Student(username=form.username.data, email=form.email.data, firstname=form.firstname.data,
            lastname=form.lastname.data, wsuid=form.wsuid.data, phone=form.phone.data, 
            c_gpa=form.c_gpa.data, grad_date=form.grad_date.data)
        acc.get_password(form.password2.data)
        db.session.add(acc)
        db.session.commit()
        flash('Congrats you are registered student')
        ##REDIRECT AFTER STUDENT REGISTERS THEY NEED TO SEE COURSES && APPLY
        ##I need to add new page
        return redirect(url_for('index'))
    return render_template('stud_reg.html', title='Register', form=form)

@app.route('/createcourse', methods=['GET', 'POST'])
def createclass():
    form = CourseForm()
    if form.validate_on_submit():
        newClass = Course(coursenum=form.coursenum.data, title=form.title.data, 
            num_ta=form.num_ta.data, min_gpa=form.min_gpa.data, min_grade=form.min_grade.data)
        db.session.add(newClass)
        db.session.commit()
        flash('The Course "' + newClass.coursenum + '-' + newClass.title + '" was created')
        return redirect(url_for('index'))
    return render_template('createcourse.html', form=form)





