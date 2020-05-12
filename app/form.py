from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,DateTimeField, PasswordField, BooleanField, SubmitField, DateField, TimeField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User, Event

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')
    
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class CreateForm(FlaskForm):
    event_name = StringField('Event', validators=[DataRequired()])
    event_date = DateTimeField('Date', format='%m/%d/%Y', validators=[DataRequired("Format 12/01/2019")])
    event_timeStart = DateTimeField('Time Start', format='%H:%M')
    event_timeEnd =DateTimeField('Time End',  format='%H:%M')
    event_submit = SubmitField('Finish')
    

class SearchForm(FlaskForm):
    eventName = StringField('Event')
    submit = SubmitField('Search')
