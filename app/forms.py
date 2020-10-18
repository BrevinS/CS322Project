from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, PasswordField, SelectField
from wtforms.validators import ValidationError, Length, DataRequired, Email, EqualTo
from app.models import Student, Professor

class ProfessorForm(FlaskForm):
    role = SelectField('Position', choices = [(1,'Professor'), (2, 'Student')])
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('LastName', validators=[DataRequired()])
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
    submit = SubmitField('Submit')