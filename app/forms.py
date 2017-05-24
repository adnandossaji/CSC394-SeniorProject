from flask_wtf import Form
from wtforms import TextField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Length
from app.models import User, Role, CourseType, Course, Term

# Set your classes here.


class RegisterForm(Form):
    name = TextField(
        'Username', validators=[DataRequired(), Length(min=6, max=25)]
    )
    email = TextField(
        'Email', validators=[DataRequired(), Length(min=6, max=40)]
    )
    password = PasswordField(
        'Password', validators=[DataRequired(), Length(min=6, max=40)]
    )
    confirm = PasswordField(
        'Repeat Password',
        [DataRequired(),
        EqualTo('password', message='Passwords must match')]
    )
    submit = SubmitField("Create account")

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        # if not Form.validate(self):
        #     return False

        user = User.query.filter_by(email = self.email.data.lower()).first()

        if user:
            self.email.errors = tuple(list("That email is already taken"))
            return False

        return



class LoginForm(Form):
    email = TextField('Email', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])

    submit = SubmitField("Sign in")

    def validate(self):
        # if not Form.validate(self):
        #     return False

        user = User.query.filter_by(email = self.email.data.lower()).first()
        if user and user.password == self.password.data:
            return True
        else:
            self.email.errors = tuple(list("Invalid e-mail or password"))
            return False

class ForgotForm(Form):
    email = TextField(
        'Email', validators=[DataRequired(), Length(min=6, max=40)]
    )
