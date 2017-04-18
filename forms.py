from flask_wtf import Form
from wtforms import TextField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Length
from models import *

# Set your classes here.


class RegisterForm(Form):
    name = TextField(
        'Username', validators=[]
    )
    email = TextField(
        'Email', validators=[]
    )
    password = PasswordField(
        'Password', validators=[]
    )
    confirm = PasswordField(
        'Repeat Password',
        [EqualTo('password', message='Passwords must match')]
    )
    submit = SubmitField("Create account")

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        # if not Form.validate(self):
        #     return False

        user = User.query.filter_by(email = self.email.data.lower()).first()

        if user:
            self.email.errors.append("That email is already taken")
            return False

        return



class LoginForm(Form):
    name = TextField('Username', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])


class ForgotForm(Form):
    email = TextField(
        'Email', validators=[DataRequired(), Length(min=6, max=40)]
    )
