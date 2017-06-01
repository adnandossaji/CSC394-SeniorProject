from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
from logging import Formatter, FileHandler
from app.forms import *
from flask import g
from app.scraper import scraper

from app.node import *
from app.search import *
from app.dummyCourse import *
from app.models import *

import os
import sqlite3
import json

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#
app = Flask(__name__)
app.config.from_object('config')

from app.models import db

db.init_app(app)
migrate = Migrate(app, db)
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
def home(path=None):
    user = None

    if 'email' in session:
        user = User.query.filter_by(email = session['email']).first()
    else:
        return redirect(url_for('login'))
    
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

@app.route('/getPath')
def getPath():

    user = None

    if 'email' in session:
        user = User.query.filter_by(email = session['email']).first()
    else:
        return redirect(url_for('login'))

   
    # dummy path data
    '''
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
    '''


    # dummy course information 
    # intro
    CS400 = DummyCourse(400, [[]], 4, 0)
    CS401 = DummyCourse(401, [[]], 4, 0)
    CS402 = DummyCourse(402, [[CS401]], 4, 0)
    CS403 = DummyCourse(403, [[CS402]], 4, 0)
    CS406 = DummyCourse(406, [[CS401]], 4, 0)
    CS407 = DummyCourse(407, [[CS406], [CS402]], 4, 0)
    CS408 = DummyCourse(408, [[CS401]], 4, 0)
    CS409 = DummyCourse(409, [[]], 4, 0)
    CS410 = DummyCourse(410, [[]], 4, 0)

    intro = [CS400, CS401, CS402, CS403, CS406, CS407]

    # foundation
    CS421 = DummyCourse(421, [[CS400], [CS403]], 4, 0)
    CS435 = DummyCourse(435, [[CS403], [CS407]], 4, 0)
    CS447 = DummyCourse(447, [[CS403], [CS406]], 4, 0)
    CS453 = DummyCourse(453, [[CS403]], 4, 0)
    SE450 = DummyCourse(450, [[CS403]], 4, 0)
    CS500 = DummyCourse(500, [[CS447, CS435], [CS421]], 4, 0)

    foundation = [CS421, CS435, CS447, CS453, SE450]

    # concentration (software and systems development)
    CS436 = DummyCourse(436, [[CS435], [CS447]], 4, 0)
    CS438 = DummyCourse(438, [[CS407]], 4, 0)
    CS461 = DummyCourse(461, [[CS400], [CS403], [CS406]], 4, 0)
    CS472 = DummyCourse(472, [[CS403], [CS407]], 4, 0)
    CS552 = DummyCourse(552, [[SE450], [CS407]], 4, 0)
    CS595 = DummyCourse(595, [[]], 4, 0)
    SE452 = DummyCourse(452, [[CS403]], 4, 0)
    SE459 = DummyCourse(459, [[SE450]], 4, 0)
    SE491 = DummyCourse(491, [[SE450]], 4, 0)

    concentration = [CS436, CS438, CS461, CS472, CS552, CS595, SE459, SE491]
    everyterm = intro + foundation + concentration

    offered = {"Fall": everyterm, "Winter": everyterm, "Spring": everyterm, "Summer": intro+foundation}

     # create search object
    Path = Search()

    # dummy taken list (empty)
    taken = set()

    # dummy units left
    units = 52

    # dummy root node for path generation (2 quarters per quarter, empty assigned and taken, starting Fall 2017)
    root = Node(0, [], taken, taken, [], units, "Fall", 2017, 2, None)

    path = Search.aStar(root, offered, intro, concentration)

    return render_template(
        'pages/placeholder.home.html', 
        path=path, 
        user=user
    )


@app.route('/updateCourses')
def update_courses():
    s = scraper()
    scraped = s.results

    for i, scraped_course in enumerate(scraped):

        course = Course(
            subject=scraped_course['subject'],
            course_number=scraped_course['course_number'],
            prereq=scraped_course['prereq'],
            day_of_week=scraped_course['day_of_week'],
            credits=scraped_course['credits'],
            description="",
            quarter_offered=scraped_course['typically_offered'],
            delivery_method=scraped_course['delivery_method']
        )

        db.session.add(course)
        db.session.commit()

    return redirect(url_for('home'))

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
            user = User(form.name.data, form.email.data, form.password.data, 3, False, form.program.data, form.concentration.data, form.start_term.data, form.start_year.data, 1, form.classes_per_term.data, "{}")
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
