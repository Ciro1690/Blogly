from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, IntegerField
from wtforms.validators import InputRequired
from wtforms.fields import html5 as h5fields
from wtforms.widgets import html5 as h5widgets

class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    email = StringField("Email", validators=[InputRequired()])
    first_name = StringField("First Name", validators=[InputRequired()])
    last_name = StringField("Last Name", validators=[InputRequired()])

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])

class UserForm(FlaskForm):
    first_name = StringField("First Name")
    last_name = StringField("Last Name")
    email = StringField("Email")

class PostForm(FlaskForm):
    title = StringField("Title", validators=[InputRequired()])
    content = TextAreaField("Review", validators=[InputRequired()])
    rating = h5fields.IntegerField("Rating", widget=h5widgets.NumberInput(min=0, max=5), validators=[InputRequired()])