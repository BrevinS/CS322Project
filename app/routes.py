from flask import render_template, flash, redirect, url_for, request
from app import app, db
from flask_sqlalchemy import sqlalchemy
from app.forms import StudentForm, ProfessorForm
from app.models import Student, Professor 

@app.before_first_request
def initDB(*args, **kwargs):
    db.create_all()

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    return render_template('base.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = ProfessorForm()
    if form.validate_on_submit():
        prof = Professor(role=form.role.data, username=form.username.data, email=form.email.data, firstname=form.firstname.data,
            lastname=form.lastname.data, wsuid=form.wsuid.data, phone=form.phone.data)
        prof.get_password(form.password2.data)
        db.session.add(prof)
        db.session.commit()
        flash('Congrats you are registered professor')
        return redirect(url_for('index'))
    return render_template('prof_form.html', title='Register', form=form)

