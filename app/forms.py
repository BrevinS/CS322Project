from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField, IntegerField, PasswordField, SelectField, BooleanField
from wtforms.validators import ValidationError, Length, DataRequired, Email, EqualTo
from app.models import Student, Professor, Course, Tag
from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField
from wtforms.widgets import ListWidget, CheckboxInput

class ProfessorForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    password1 = PasswordField('Password', validators=[DataRequired()])
    email = StringField('WSU Email', validators=[DataRequired(), Email()])
    wsuid = StringField('WSU ID', validators=[DataRequired(), Length(min=8, max=8)])
    phone = StringField('Phone #', validators=[DataRequired(), Length(min=10, max=10)])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), 
                EqualTo('password1')])
    
    submit = SubmitField('Register')

    def validate_username(self, username):
        prof = Professor.query.filter_by(username=username.data).first()
        if prof is not None:
            raise ValidationError('Username already exists! Try another...')

    def validate_email(self, email):
        prof = Professor.query.filter_by(email=email.data).first()
        if prof is not None:
            raise ValidationError('Email has already been used! Try another...')

class StudentForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    password1 = PasswordField('Password', validators=[DataRequired()])
    email = StringField('WSU Email', validators=[DataRequired(), Email()])
    wsuid = StringField('WSU ID', validators=[DataRequired(), Length(min=8, max=8)])
    phone = StringField('Phone #', validators=[DataRequired(), Length(min=10, max=10)])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), 
                EqualTo('password1')])
    major = SelectField('Major:', choices = [(1, 'Computer Science'), (2, 'Electrical Engineering'), 
            (3, 'Mechanical Engineering'), (4, 'Computer Engineering'), (5, 'Software Engineering'),
            (6, 'Data Analytics'), (7, 'Architectural Studies'), (8, 'Materials Science and Engineering')])
    c_gpa = FloatField('Cumulative GPA', validators=[DataRequired()])
    grad_date = StringField('Graduation Date mm/dd/yyyy', validators=[DataRequired(), Length(min=10, max=10)])
    submit = SubmitField('Register')
    #QUERY OF PREVIOUS TA JOBS

def get_tag():
    return Tag.query

class CourseForm(FlaskForm):
    coursenum = StringField('Course #', [Length(min=3, max=3)])
    title = StringField('Course Title', validators=[DataRequired()])
    num_ta = IntegerField('# of TA\'s', validators=[DataRequired()])
    min_gpa = FloatField('minimum GPA', validators=[DataRequired()])
    min_grade = SelectField('Grade in course', choices = [(1, 'A'), (2, 'B'), (3, 'C'), (4,'D'), (5,'F')])
    
    tag = QuerySelectMultipleField('Tag', query_factory=get_tag, get_label='name',
                                        widget=ListWidget(prefix_label=False),
                                        option_widget=CheckboxInput())
    submit = SubmitField('Create Course')
    #priorxp = 
    #^^^^^^^^^^^^^^^^^QUERY OF PREVIOUS COURSES TA'd
    #list of Students who applied

class LoginForm(FlaskForm):
    role = SelectField('Role', choices = [(1, 'Student'), (2, 'Professor')])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    rememberme = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

#THIS WAS USELESS
class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')
#Enter courses taught by professor, how many TA's needed per course, qualification (min GPA, grade in course, prior TA experience)
#class ProfessorForm(FlaskForm):
    #COURSES TEACHING QUERY

#YEAR/SEMESTER THEY TOOK THE COURSE
#1 INDICATES YEAR/SEMESTER THEY ARE WANTING TO TA FOR THE COURSE
class ApplyForm(FlaskForm):
    semester = SelectField('Semester', choices = [(1, 'Fall'), (2, 'Spring'), (3, 'Summer')])
    year = StringField('Year of enrollment in course', validators=[DataRequired(), Length(min=4, max=4)])
    semester1 = SelectField('Semester you want to TA', choices = [(1, 'Fall'), (2, 'Spring'), (3, 'Summer')])
    year1 = StringField('Year you want to TA', validators=[DataRequired(), Length(min=4, max=4)])
    min_grade = SelectField('Grade in course', choices = [(1, 'A'), (2, 'B'), (3, 'C'), (4,'D'), (5,'F')])
    submit = SubmitField('Send App')


    