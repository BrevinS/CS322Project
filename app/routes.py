from flask import render_template, flash, redirect, url_for, request
from app import app, db
from flask_sqlalchemy import sqlalchemy
from app.forms import StudentForm, ProfessorForm, CourseForm, LoginForm, EmptyForm
from app.models import Student, Professor, Course
from flask_login import current_user, login_user, logout_user, login_required

@app.before_first_request
def initDB(*args, **kwargs):
    db.create_all()

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
@login_required
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
        flash('Congrats you are a registered professor')
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
        flash('Congrats you are a registered student')
        ##REDIRECT AFTER STUDENT REGISTERS THEY NEED TO SEE COURSES && APPLY
        ##I need to add new page
        return redirect(url_for('index'))
    return render_template('stud_reg.html', title='Register', form=form)

@app.route('/createcourse', methods=['GET', 'POST'])
@login_required
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

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        print(form.role.data)
        #Student
        if (int(form.role.data) == 1):
            student = Student.query.filter_by(username=form.username.data).first()
            if student is None or not student.check_password(form.password.data):
                flash('Not a username or incorrect password!')
                return redirect(url_for('login'))
            #Valid Student Login
            login_user(student, remember=form.rememberme.data)
            return redirect(url_for('index'))
        #Professor
        elif (int(form.role.data) == 2):
            professor = Professor.query.filter_by(username=form.username.data).first()
            if professor is None or not professor.check_password(form.password.data):
                flash('Not a username or incorrect password!')
                return redirect(url_for('login'))
            #Valid Professor Login 
            login_user(professor, remember=form.rememberme.data)
            return redirect(url_for('index'))
    return render_template('login.html', title='Login Page', form=form)

@login_required
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/apply/<courseid>', methods=['POST'])
@login_required
def enroll(courseid):
    form = EmptyForm()
    if form.validate_on_submit():
        course = Course.query.filter_by(id=courseid).first()
        if couse is None:
            flash('"{}" Was not found!'.format(courseid))
            return redirect('index')
        current_user.apply(course)
        db.session.commit()
        flash('Apply to TA for {}'.format(course.title))
        return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))

@app.route('/unapply/<courseid>', methods=['POST'])
@login_required
def unapply(courseid):
    form = EmptyForm()
    if form.validate_on_submit():
        course = Course.query.filter_by(id=courseid).first()
        if course is None:
            flash('"{}" Was not found!'.format(courseid))
            return redirect(url_for('index'))
        current_user.unapply(course)
        db.session.commit()
        flash('You have unapplied for TA position for course {} {}'.format(course.title, course.coursenum))
        return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))
