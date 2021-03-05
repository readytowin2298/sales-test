from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, IntegerField, BooleanField, RadioField
from wtforms import validators
from wtforms.validators import DataRequired, InputRequired, Length


class UserForm(FlaskForm):

    username = StringField("Billmax Username",
                validators=[InputRequired()])
    password = PasswordField("A password of your choosing",
                validators=[Length(min=6, message="Password must be at least six characters long")])