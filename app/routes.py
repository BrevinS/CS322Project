from flask import render_template, flash, redirect, url_for, request
from app import app, db
from flask_sqlalchemy import sqlalchemy
from app.forms import StudentForm, ProfessorForm, CourseForm, LoginForm, EmptyForm, ApplyForm
from app.models import Student, Professor, Course, Tag, courseTags, applied, accepted
from flask_login import current_user, login_user, logout_user, login_required

@app.before_first_request
def initDB(*args, **kwargs):
    db.create_all()
    if Tag.query.count() == 0:
        tags = ['Min-GPA 3.0+', 'Min-GPA 3.5+', 'Min-Grade A', 'Min-Grade B', 'Prior-TA-Exper.', 'Senior', 'Graduate', 'Junior+']
        for t in tags:
            db.session.add(Tag(name=t))
        db.session.commit()

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
@login_required
def index():
    courses = Course.query.order_by(Course.coursenum).all()
    return render_template('studentInterface.html', courses=courses)

@app.route('/profregister', methods=['GET', 'POST'])
def profregister():
    if current_user.is_authenticated:
        flash('You must logout to use this feature!')
        return redirect(url_for('index'))
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
    if current_user.is_authenticated:
        flash('You must logout to use this feature!')
        return redirect(url_for('index'))
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

@app.route('/apply/<courseid>', methods=['GET', 'POST'])
@login_required
def apply(courseid):
    form = ApplyForm()
    _course = db.session.query(Course).filter_by(id=courseid).first()
    if form.validate_on_submit() and _course is not None:
        current_user.apply(_course)
        db.session.commit()
        flash('You have successfully applied to TA for the course: {}'.format(_course.title))
        return redirect(url_for('index'))
    return render_template('apply.html', form=form)

@app.route('/createcourse', methods=['GET', 'POST'])
@login_required
def createclass():
    form = CourseForm()
    if form.validate_on_submit():
        newClass = Course(professor_id=current_user.id, coursenum=form.coursenum.data, title=form.title.data, 
            num_ta=form.num_ta.data, min_gpa=form.min_gpa.data, min_grade=form.min_grade.data)
        for pt in form.tag.data:
            newClass.tags.append(pt)
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


@app.route('/unapply/<courseid>', methods=['POST'])
@login_required
def unapply(courseid):
    _course = db.session.query(Course).filter_by(id=courseid).first()
    if _course is not None:
        current_user.unapply(_course)
        db.session.commit()
        flash("You have successfully revoked your application for course : {}".format(_course.title))
        return redirect(url_for('index'))
    else:
        flash('"{}" Was not found!'.format(_courseid))
        return redirect('index')

@app.route('/delete/<courseid>', methods=['POST'])
@login_required
def delete(courseid):
    _post = db.session.query(Course).filter_by(id=courseid).first()
    if _post is not None:
        #Remove course from database in case it gets readded
        for pt in _post.tags:
            _post.tags.remove(pt)
        db.session.commit()
        db.session.delete(_post)
        db.session.commit()
        flash("You have successfully removed your course: {}".format(_post.title))
        return redirect(url_for('index'))
    else:
        return redirect('index')

#Professor clicks button to view apps
@app.route('/viewapps', methods=['GET'])
@login_required
def viewapps():
    courses = Course.query.order_by(Course.coursenum).all()
    return render_template('viewapps.html', courses=courses)

@app.route('/acceptTA/<courseid>/<studentid>', methods=['POST'])
@login_required
def acceptTA(courseid, studentid):
    _course = db.session.query(Course).filter_by(id=courseid).first()
    _student = db.session.query(Student).filter_by(id=studentid).first()
    courses = Course.query.order_by(Course.coursenum).all()
    flag = 0
    if _course is not None and _student is not None:
        for course in courses:
            if _student.is_ta(course):
                flash('Student {}{} is already a TA! Active TA for {}'.format(_student.firstname, _student.lastname, course.title))
                flag = 1
                return redirect(url_for('viewapps'))
        if flag == 0:
            _course.accepted(_student)
            db.session.commit()
            flash('You have successfully made {}{} a TA for {}'.format(_student.firstname, _student.lastname, _course.title))
        return redirect(url_for('viewapps'))
    else:
        flash('Something went wrong')
        return redirect(url_for('index'))

@app.route('/unacceptTA/<courseid>/<studentid>', methods=['POST'])
@login_required
def unacceptTA(courseid, studentid):
    _course = db.session.query(Course).filter_by(id=courseid).first()
    _student = db.session.query(Student).filter_by(id=studentid).first()
    courses = Course.query.order_by(Course.coursenum).all()
    if _course is not None and _student is not None:
        if _student.is_ta(_course):
            _course.unaccept(_student)
            db.session.commit()
            flash('Successfully removed {}{} from being a TA for {}'.format(_student.firstname, _student.lastname, _course.title))
            return redirect(url_for('viewapps'))
        return redirect(url_for('index'))
    else:
        flash('Something went wrong')
        return redirect(url_for('index'))