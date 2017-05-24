#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import Flask, render_template, request, redirect, url_for, session
from flask.ext.sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from forms import *
import os
import sqlite3
from flask import g
from scraper import scraper
from models import *
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
DATABASE = 'database.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Login required decorator.
def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap
#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@app.route('/')
def home():
	user = None
	if 'email' in session:
		user = User.query.filter_by(email = session['email']).first()
	else:
		render_template('errors/404.html')

	# dummy path data
	path = {
	'Fall 2017': ['CSC 402', 'CSC 403'],
	'Winter 2017': ['CSC 406', 'CSC 407'],
	'Spring 2018': ['CSC 421', 'CSC 435'],
	'Summer 2018': ['CSC 447', 'CSC 453'],
	'Fall 2018': ['SE 450', 'CSC 436'],
	'Winter 2018': ['CSC 438', 'CSC 439'],
	'Spring 2019': ['CSC 443', 'CSC 448'],
	'Summer 2019': ['CSC 461', 'CSC 462'],
	'Fall 2019': ['CSC 471']
	}
	
	return render_template(
		'pages/placeholder.home.html',
		user=user,
		path=path
    )


@app.route('/admin')
def admin():
    user = None
    if 'email' in session:
        user = User.query.filter_by(email = session['email']).first()
    else:
        render_template('errors/404.html')


    students = []

    for i in range(0,11):
        students.append(
            {
                "name": "Student %s" % i,
                "email": "student%s@mail.depaul.edu" % i,
                "pending": True if i % 3 else False
            }
        )
    
    return render_template(
        'pages/placeholder.admin.html',
        user=user,
        students=students
    )

@app.route('/updateCourses')
def update_courses(course = None):
    s = scraper()
    scraped = s.results
    course_list = [course] * len(scraped)

    for i, scraped_course in enumerate(scraped):
        print(scraped_course)
        course_list.insert(
            i,
            Course(
                id=scraped_course['course_number'],
                name=scraped_course['subject'],
                prereq=scraped_course['delivery_type'],
                credits=scraped_course['credits'],
                day_of_week=scraped_course['day_of_week'],
                quarter_offered=scraped_course['typically_offered'] ,
                delivery_method=scraped_course['delivery_type']
            )
        )
    [db.session.add(i) for i in course_list]

    db.session.commit()
    return '200'


@app.route('/about')
def about():
    user = None
    if 'email' in session:
        user = User.query.filter_by(email = session['email']).first()
    else: render_template('errors/404.html')

    return render_template(
        'pages/placeholder.about.html',
        user=user,
    )


@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST':
        if form.validate() == False:
          return render_template('forms/login.html', form=form)
        else:
          session['email'] = form.email.data
          user = User.query.filter_by(email = session['email']).first()

          return redirect(url_for('home'))
    elif request.method == 'GET':
        return render_template('forms/login.html', form=form)

@app.route('/logout')
def logout():
    form = LoginForm(request.form)
    session.pop('email', None)
    return redirect(url_for('home'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)

    if request.method == 'POST':
        
        if form.validate() == False:
            return render_template(
                'forms/register.html',
                form=form
            )
        else:
            user = User(form.name.data, form.email.data, form.password.data)
            db.session.add(user)
            db.session.commit()

            session['email'] = user.email

        return render_template('pages/placeholder.home.html', user=user)

    elif request.method == 'GET':

        return render_template(
            'forms/register.html',
            form=form
        )


@app.route('/forgot')
def forgot():
    form = ForgotForm(request.form)
    return render_template('forms/forgot.html', form=form)

# Error handlers.


@app.errorhandler(500)
def internal_error(error):
    #db_session.rollback()
    return render_template('errors/500.html'), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
