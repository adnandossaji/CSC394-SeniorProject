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

    if user.role.name == "Faculty" or user.role.name == "Admin":
        return redirect(url_for('admin'))

    courses_taken = [Course.query.filter_by(id = x).first().title() for x in json.loads(user.taken)]
    degree_credits = len(courses_taken) * 4

    return render_template(
        'pages/placeholder.home.html',
        user=user,
        path=path,
        courses_taken=courses_taken,
        degree_credits=degree_credits,
        last_path=json.loads(user.last_path)
    )

@app.route('/paths')
def paths():
    user = None

    if 'email' in session:
        user = User.query.filter_by(email = session['email']).first()
    else:
        return redirect(url_for('login'))

    if user.taken:
        courses_taken = [Course.query.filter_by(id = x).first().title() for x in json.loads(user.taken)]
    else:
        courses_taken = []
    degree_credits = len(courses_taken) * 4

    paths = [json.loads(x.path) for x in user.paths]

    return render_template(
        'pages/placeholder.paths.html',
        user=user,
        courses_taken=courses_taken,
        degree_credits=degree_credits,
        last_path=json.loads(user.last_path),
        paths=reversed(paths),
        len_paths=len(paths),
        len=len,
        enumerate=enumerate
    )

@app.route('/profile/<user_id>')
def profile(path=None, user_id=None):
    user = None

    if 'email' in session:
        user = User.query.filter_by(email = session['email']).first()
    else:
        return redirect(url_for('login'))

    user = User.query.filter_by(id = user_id).first()

    courses_taken = [Course.query.filter_by(id = x).first().title() for x in json.loads(user.taken)]
    degree_credits = len(courses_taken) * 4

    return render_template(
        'pages/placeholder.home.html',
        user=user,
        path=path,
        courses_taken=courses_taken,
        degree_credits=degree_credits,
        last_path=json.loads(user.last_path)
    )

@app.route('/admin')
def admin():
    user = None
    if 'email' in session:
        user = User.query.filter_by(email = session['email']).first()
    else:
        render_template('errors/404.html')

    if user.role.name == "Faculty":
        users = [user]
        users += User.query.filter_by(role_id = "3").all()
    else:
        users = User.query.all()
    
    return render_template(
        'pages/placeholder.admin.html',
        user=user,
        users=users
    )


@app.route('/editUser/<user_id>', methods=['GET', 'POST'])
def editUser(user_id):
    user = None
    if 'email' in session:
        user = User.query.filter_by(email = session['email']).first()
    else:
        render_template('errors/404.html')

    form = EditUserForm(request.form)

    edit_user = User.query.filter_by(id = user_id).first()

    if request.method == 'POST':
        
        if form.validate() == False:
            return render_template(
                'pages/placeholder.editUser.html',
                user=user,
                form=form
            )
        else:

            edit_user.name = form.name.data
            edit_user.email = form.email.data
            edit_user.role_id = form.role.data
            edit_user.program = form.program.data
            edit_user.concentration = form.concentration.data
            edit_user.start_term = form.start_term.data
            edit_user.start_year = form.start_year.data
            edit_user.delivery_type = form.delivery_type.data
            edit_user.classes_per_term = int(form.classes_per_term.data)
            edit_user.taken = json.dumps(form.taken.data)

            curr_db = db.session.object_session(edit_user)
            curr_db.commit()

            return redirect(url_for('profile', user_id=edit_user.id))

    elif request.method == 'GET':

        courses = Course.query.all()

        form.name.data = edit_user.name
        form.email.data = edit_user.email
        form.program.data = edit_user.program
        form.concentration.data = edit_user.concentration
        form.role.data = str(edit_user.role_id)
        form.start_term.data = edit_user.start_term
        form.start_year.data = edit_user.start_year
        form.classes_per_term.data = str(edit_user.classes_per_term)

        form.taken.choices = [(x.id, "{} {}".format(x.subject, x.course_number)) for x in courses]
        form.taken.data = json.loads(edit_user.taken)

        courses_taken = [Course.query.filter_by(id = x).first().title() for x in json.loads(user.taken)]
        degree_credits = len(courses_taken) * 4
        
        return render_template(
            'pages/placeholder.editUser.html',
            user=user,
            form=form,
            courses_taken=courses_taken,
            degree_credits=degree_credits,
            last_path=json.loads(user.last_path)                  
        )


@app.route('/savePath')
@app.route('/savePath/<user_id>')
def savePath(user_id=None):

    user = None

    if 'email' in session:
        user = User.query.filter_by(email = session['email']).first()
    else:
        return redirect(url_for('login'))

    if user_id:
        user = User.query.filter_by(id = user_id).first()

    save_path = Path(user.id, user.last_path)
    db.session.add(save_path)
    db.session.commit()

    return redirect(url_for('paths'))

@app.route('/getPath')
@app.route('/getPath/<user_id>')
def getPath(user_id=None):

    user = None

    if 'email' in session:
        user = User.query.filter_by(email = session['email']).first()
    else:
        return redirect(url_for('login'))

    if user_id:
        user = User.query.filter_by(id = user_id).first()

    # create search object
    Path = Search()

    # create dictionary of offered courses
    offered = {"Autumn": [], "Winter": [], "Spring": [], "Summer": []}
    
    requirements = [
        ['CSC 400', 'CSC 401', 'CSC 402', 'CSC 403', 'CSC 406'], 
        ['CSC 421', 'CSC 435', 'CSC 447', 'CSC 453', 'SE 450'], 
        ['CSC 436', 'CSC 438', 'CSC 439', 'CSC 443', 'CSC 448', 'CSC 461', 'CSC 462', 'CSC 471', 'CSC 472', 'CSC 475', 'CSC 534', 'CSC 536', 'CSC 540', 'CSC 548', 'CSC 549', 'CSC 551', 'CSC 552', 'CSC 553', 'CSC 595', 'CNS 450', 'GAM 690', 'GAM 691', 'HCI 441', 'SE 441', 'SE 452', 'SE 459', 'SE 525', 'SE 526', 'SE 554', 'SE 560', 'TDC 478', 'TDC 484', 'TDC 568'], 
        ['CSC 431', 'CSC 440', 'CSC 444', 'CSC 489', 'CSC 503', 'CSC 521', 'CSC 525', 'CSC 531', 'CSC 535', 'CSC 547', 'CSC 557', 'CSC 580', 'CSC 591', 'SE 533'], 
        ['CSC 423', 'CSC 424', 'CSC 425', 'CSC 428', 'CSC 433', 'CSC 465', 'CSC 478', 'CSC 481', 'CSC 482', 'CSC 495', 'CSC 529', 'CSC 555', 'CSC 575', 'CSC 578', 'CSC 594', 'CSC 598', 'CSC 672', 'ECT 584', 'IS 467'], 
        ['CSC 433', 'CSC 452', 'CSC 454', 'CSC 478', 'CSC 529', 'CSC 543', 'CSC 549', 'CSC 551', 'CSC 553', 'CSC 554', 'CSC 555', 'CSC 575', 'CSC 589'], 
        ['CSC 457', 'CSC 458', 'CSC 478', 'CSC 480', 'CSC 481', 'CSC 482', 'CSC 495', 'CSC 528', 'CSC 529', 'CSC 538', 'CSC 575', 'CSC 576', 'CSC 577', 'CSC 578', 'CSC 583', 'CSC 587', 'CSC 592', 'CSC 594', 'ECT 584', 'GEO 441', 'GEO 442', 'IS 467'], 
        ['SE 430', 'SE 433', 'SE 441', 'SE 452', 'SE 453', 'SE 456', 'SE 457', 'SE 459', 'SE 475', 'SE 477', 'SE 480', 'SE 482', 'SE 491', 'SE 525', 'SE 526', 'SE 529', 'SE 533', 'SE 546', 'SE 549', 'SE 554', 'SE 556', 'SE 560', 'SE 579', 'SE 581', 'SE 582', 'SE 591'], 
        ['CSC 461', 'CSC 462', 'GAM 450', 'GAM 453', 'GAM 475', 'GAM 476', 'GAM 486', 'GAM 490', 'GAM 575', 'GAM 576', 'GAM 690', 'GAM 691', 'GPH 436', 'GPH 469', 'GPH 570', 'GPH 572', 'GPH 580', 'HCI 440', 'SE 456', 'SE 556']
    ]

    # try and add requirements before other courses
    check = requirements[0] + requirements[1] + requirements[2] + requirements[3]
    for req in check:
        (sub, num) = req.split(" ")
        course = Course.query.filter_by(subject = sub).filter_by(course_number = num).first()

        quarter_offered = json.loads(course.quarter_offered.replace('\'', "\""))

        for off in quarter_offered:
            if (off == "Not Offered"):
                continue
            elif (off == "As Needed"):
                offered["Autumn"].append(course)
                offered["Spring"].append(course)
                offered["Summer"].append(course)
                offered["Winter"].append(course) 
            elif (off == "EO Academic Year"):
                continue
            else:
                offered[off].append(course)

    for course in Course.query.all():
        if "{} {}".format(course.subject, course.course_number) not in check:
            quarter_offered = json.loads(course.quarter_offered.replace('\'', "\""))
            for off in quarter_offered:
                if (off == "As Needed"):
                    offered["Autumn"].append(course)
                    offered["Spring"].append(course)
                    offered["Summer"].append(course)
                    offered["Winter"].append(course)
                if (off == "Autumn"):
                    offered[off].append(course)
                if (off == "Spring"):
                    offered[off].append(course)
                if (off == "Summer"):
                    offered[off].append(course)
                if (off == "Winter"):
                    offered[off].append(course)

    assigned = []
    days = []

    # get user's taken courses
    taken = set(user.taken.split(","))

    # subtract course credits from taken courses to get units left
    units_left = 52
    for course in taken:
        units_left -= 4

    # def __init__(self, num_quarters, assigned, taken, taken_overall, days, units_left, quarter, year, per_quarter, parent):
    root = Node(0, assigned, taken, taken, days, units_left, "Autumn", 2017, user.classes_per_term, None)

    path = Search.aStar(root, offered, requirements[0]+requirements[1], requirements[2],  4)

    courses_taken = [Course.query.filter_by(id = x).first().title() for x in json.loads(user.taken)]
    degree_credits = len(courses_taken) * 4

    user.last_path = json.dumps(path)

    curr_db = db.session.object_session(user)
    curr_db.commit()

    return render_template(
        'pages/placeholder.home.html', 
        path=path, 
        user=user,
        courses_taken=courses_taken,
        degree_credits=degree_credits,
        last_path=json.loads(user.last_path)
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

            user = User(form.name.data, form.email.data, form.password.data, 3, False, form.program.data, form.concentration.data, form.start_term.data, form.start_year.data, form.delivery_type.data, form.classes_per_term.data, "[]")
            db.session.add(user)
            db.session.commit()

            session['email'] = user.email

        return redirect(url_for('home'))

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
