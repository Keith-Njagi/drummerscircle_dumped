from flask_wtf import FlaskForm
from wtforms import TextField, TextAreaField, SubmitField, StringField, PasswordField, BooleanField, FileField
from wtforms.validators import InputRequired, Email, Length, URL


class LogInForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(),Length(min=4, max=20)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('Remember Me')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=20)])
    email = StringField('Email Address', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
    password_confirm = PasswordField('Retype Password', validators=[InputRequired(), Length(min=8, max=80)])


class ContactForm(FlaskForm):
    name = TextField("Name", validators=[InputRequired(), Length(max=20)])
    email = TextField("Email", validators=[InputRequired(), Email(message='Invalid Email')])
    subject = TextField("Subject", validators=[InputRequired(), Length(max=20)])
    message = TextAreaField("Message", validators=[InputRequired()])
    submit = SubmitField("Send")

class AddPost(FlaskForm):
    title = TextField('Title', validators=[InputRequired(), Length(max=30)])
    subtitle = TextField('Subtitle', validators=[InputRequired(), Length(max=50)])
    content = TextAreaField('Content', validators=[InputRequired()])
    submit = SubmitField('Post')

class UploadTutorialForm(FlaskForm):
    title = TextField('Title', validators=[InputRequired(), Length(max=30)])
    aboutTutorial = TextAreaField('About this tutorial', validators=[InputRequired()])
    tutorialFile = FileField('Would you like to upload your tutorial file?' )
    url = StringField('Or rather post a link to your tutorial...', validators=[URL])
    submit = SubmitField('Upload')
