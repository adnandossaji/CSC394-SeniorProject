from flask_wtf import Form
from wtforms import TextField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, EqualTo, Length
from app.models import *

class RegisterForm(Form):
    name = TextField('Username', validators=[DataRequired(), Length(min=6, max=25)]    )
    email = TextField('Email', validators=[DataRequired(), Length(min=6, max=40)]    )
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=40)]    )
    confirm = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])

    program = SelectField("Program", validators=[DataRequired()], choices=[
            ("Information Systems", "Information Systems"),
            ("Computer Science", "Computer Science")
        ]
    )
    concentration = SelectField("Concentration", validators=[DataRequired()], choices=[
            ("Software and Systems Development", "Software and Systems Development"),
            ("Theory", "Theory"),
            ("Data Science", "Data Science"),
            ("Database Systems", "Database Systems"),
            ("Artificial Intelligence", "Artificial Intelligence"),
            ("Software Engineering","Software Engineering"),
            ("Multimedia", "Multimedia")
        ]
    )
    
    start_term = SelectField("Starting Term", validators=[DataRequired()], choices=[("Autumn", "Autumn"), ("Winter", "Winter"), ("Spring", "Spring")])
    start_year = SelectField("Starting Year", validators=[DataRequired()], choices=[("2017", "2017"), ("2018", "2018")])
    delivery_type = SelectField("Delivery Preference", validators=[DataRequired()], choices=[("In-Class Only", "In-Class Only"), ("Online Only", "Online Only"), ("In-Class or Online", "In-Class or Online")])
    classes_per_term = SelectField("Classes per Term", validators=[DataRequired()], choices=[("1", "1"), ("2", "2"), ("3", "3")])

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

class EditUserForm(Form):
    name = TextField('Username', validators=[DataRequired(), Length(min=6, max=25)]    )
    email = TextField('Email', validators=[DataRequired(), Length(min=6, max=40)]    )

    program = SelectField("Program", validators=[DataRequired()], choices=[
            ("Information Systems", "Information Systems"),
            ("Computer Science", "Computer Science")
        ]
    )
    concentration = SelectField("Concentration", validators=[DataRequired()], choices=[
            ("Software and Systems Development", "Software and Systems Development"),
            ("Theory", "Theory"),
            ("Data Science", "Data Science"),
            ("Database Systems", "Database Systems"),
            ("Artificial Intelligence", "Artificial Intelligence"),
            ("Software Engineering","Software Engineering"),
            ("Multimedia", "Multimedia")
        ]
    )

    role = SelectField("Role", validators=[DataRequired()], choices=[("1", "Admin"), ("2", "Faculty"), ("3", "Student")])
    
    start_term = SelectField("Starting Term", validators=[DataRequired()], choices=[("Autumn", "Autumn"), ("Winter", "Winter"), ("Spring", "Spring")])
    start_year = SelectField("Starting Year", validators=[DataRequired()], choices=[("2017", "2017"), ("2018", "2018")])
    delivery_type = SelectField("Delivery Preference", validators=[DataRequired()], choices=[("In-Class Only", "In-Class Only"), ("Online Only", "Online Only"), ("In-Class or Online", "In-Class or Online")])
    classes_per_term = SelectField("Classes per Term", validators=[DataRequired()], choices=[("1", "1"), ("2", "2"), ("3", "3")])

    submit = SubmitField("Save Changes")

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        # if not Form.validate(self):
        #     return False

        # user = User.query.filter_by(email = self.email.data.lower()).first()

        # if user:
        #     self.email.errors = tuple(list("That email is already taken"))
        #     return False

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
