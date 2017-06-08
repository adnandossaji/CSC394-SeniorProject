from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
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

@app.route('/seedDB')
def seedDB():
    user = None

    if 'email' in session:
        user = User.query.filter_by(email = session['email']).first()
    else:
        return redirect(url_for('login'))

    courses = [
        Course('CSC',423,'IT 403',4,'Sun','','["Not Offered"]',1),
        Course('CSC',424,'CSC 423 or consent of instructor.',4,'Sun','','["Not Offered"]',1),
        Course('CSC',426,'PhD status or consent of instructor.',4,'Sat','','["EO Spring"]',0),
        Course('CSC',428,'CSC 423.',4,'Fri','','["Not Offered"]',0),
        Course('GPH',436,'CSC 393 and MAT 150.',4,'Fri','','["Not Offered"]',0),
        Course('CSC',444,'CSC 400 and CSC 403',4,'Sat','','["As Needed"]',0),
        Course('CSC',447,'CSC 403 and CSC 406',4,'Sun','','["Autumn", "Winter", "Spring"]',1),
        Course('CSC',448,'CSC 447',4,'Sat','','["As Needed"]',0),
        Course('CSC',451,'None',4,'Sat','','["Autumn", "Winter", "Spring"]',1),
        Course('CSC',452,'(CSC 453 or CSC 451 or CSC 455) and (CSC 401 or IT 411)',4,'Sat','','["Autumn", "Winter", "Spring"]',1),
        Course('CSC',453,'CSC 403',4,'Sun','','["Autumn", "Winter", "Spring"]',1),
        Course('CSC',457,'CSC 403',4,'Thu','','["Not Offered"]',0),
        Course('CSC',458,'CSC 403',4,'Sat','','["EO Academic Year"]',0),
        Course('GPH',469,'CSC 461 and (GAM 425 or GPH 436)',4,'Fri','','["Not Offered"]',0),
        Course('GPH',425,'CSC 212 or CSC 262.',4,'Sat','','["Not Offered"]',0),
        Course('CSC',475,'[]',4,'Fri','','["Not Offered"]',0),
        Course('CSC',480,'CSC 403',4,'Sat','','["Winter"]',0),
        Course('CSC',481,'CSC 412 or consent of instructor',4,'Sat','','["Autumn"]',1),
        Course('CSC',485,'MAT 220 and a programming course.',4,'Sun','','["Not Offered"]',0),
        Course('CSC',421,'CSC 400 and CSC 403',4,'Sun','','["Autumn", "Winter", "Spring"]',1),
        Course('CSC',503,'CSC 421',4,'Sat','','["Winter"]',0),
        Course('CSC',535,'CSC 447.',4,'Sat','','["As Needed"]',0),
        Course('CSC',538,'CSC 528',4,'Fri','','["Not Offered"]',0),
        Course('GPH',539,'GPH 425 or GPH 436 or (ANI 439 and GPH 355)',4,'Mon','','["Not Offered"]',0),
        Course('CSC',489,'CSC 444 or CSC 421.',4,'Sat','','["EO Academic Year"]',0),
        Course('CSC',547,'Instructor consent required.',4,'Thu','','["Not Offered"]',0),
        Course('CSC',548,'CSC 448.',4,'Fri','','["Not Offered"]',0),
        Course('CSC',549,'CSC 453',4,'Sat','','["As Needed"]',0),
        Course('CSC',550,'CSC 453',4,'Sun','','["Not Offered"]',0),
        Course('CSC',551,'CSC 453 and (CSC 435 or TDC 405 or TDC 463)',4,'Fri','','["Not Offered"]',0),
        Course('CSC',554,'[]',4,'Sat','','["Winter"]',0),
        Course('GPH',570,'GPH 469 or GAM 470',4,'Sat','','["Not Offered"]',0),
        Course('GPH',572,'GPH 469.',4,'Mon','','["Not Offered"]',0),
        Course('GPH',575,'GPH 448 and (GPH 469 or GAM 470)',4,'Sat','','["Not Offered"]',0),
        Course('CSC',578,'(CSC 412 and CSC 478) or (CSC 403 and IS 467)',4,'Sat','','["Autumn"]',1),
        Course('CSC',528,'CSC 481',4,'Sat','','["As Needed"]',0),
        Course('CSC',587,'CSC 403 or HCI 460.',4,'Sat','','["Winter"]',0),
        Course('CSC',589,'For specific prerequisites, see syllabus or consult with course instructor. (variable credit)',0,'Fri','','["Not Offered"]',0),
        Course('CSC',590,'For specific prerequisites, see syllabus or consult with course instructor. (variable credit)',0,'Fri','','["Not Offered"]',0),
        Course('CSC',591,'For specific prerequisites, see syllabus or consult course instructor. (variable credit)',0,'Fri','','["Not Offered"]',0),
        Course('CSC',592,'CSC 482 or CSC 528',0,'Fri','','["Not Offered"]',0),
        Course('CSC',594,'For specific prerequisites, see syllabus or consult course instructor. (variable credit)',0,'Tue','','["Autumn", "Spring"]',0),
        Course('GPH',595,'Permission of instructor.',0,'Mon','','["Not Offered"]',0),
        Course('CSC',598,'For specific prerequisites, see syllabus or consult course instructor. (variable credit)',0,'Fri','','["Not Offered"]',0),
        Course('CSC',599,'None',0,'Fri','','["Not Offered"]',0),
        Course('CSC',690,'Consent of the instructor. (variable credit)',0,'Fri','','["Not Offered"]',0),
        Course('CSC',696,'CSC 695 taken twice and approval of report by student''s research supervisor and faculty advisor. (0 credit hours)',0,'Fri','','["Not Offered"]',0),
        Course('CSC',698,'Successful defense of a Master''s Thesis.  (variable credit)',0,'Fri','','["Not Offered"]',0),
        Course('CSC',699,'Research course supervised by an instructor. Independent Study Form required.  Variable credit.  Can be repeated for credit. (variable credit)',0,'Fri','','["Not Offered"]',0),
        Course('CSC',701,'Admission to Candidacy. Independent Study form required.  (0 credit hours)',0,'Fri','','["Not Offered"]',0),
        Course('CSC',702,'Admission to Candidacy.  Independent Study form required.  (0 credit hours)',0,'Fri','','["Not Offered"]',0),
        Course('IS',421,'None',4,'Wed','','["Autumn", "Winter", "Spring"]',1),
        Course('IS',422,'IS 421 and CSC 451',4,'Sun','','["Autumn", "Winter", "Spring"]',1),
        Course('IS',482,'None',4,'Sat','','["Not Offered"]',0),
        Course('IS',483,'Completion of five or more SoC MS level courses is required.',4,'Sat','','["Not Offered"]',0),
        Course('IS',511,'[]',4,'Mon','','["Not Offered"]',1),
        Course('IS',440,'None',4,'Wed','','["Autumn", "Winter", "Spring"]',1),
        Course('IS',540,'Completion of five or more SoC MS level courses is required.',4,'Sat','','["Not Offered"]',0),
        Course('IS',549,'[]',4,'Sun','','["Not Offered"]',1),
        Course('IS',556,'IS 430 or PM 430',4,'Fri','','["Autumn", "Winter", "Spring"]',1),
        Course('IS',560,'Advanced Standing',4,'Mon','','["Not Offered"]',1),
        Course('IS',433,'None',4,'Sun','','["Autumn", "Winter", "Spring"]',0),
        Course('IS',574,'(SE 430 or IS 435 or PM 430 or  MIS 674) and CS C451',4,'Fri','','["Not Offered"]',1),
        Course('IS',577,'Completion of ten or more SoC MS level courses is required.',4,'Wed','','["Not Offered"]',0),
        Course('IS',578,'Completion of foundation or core phase.',4,'Mon','','["Not Offered"]',0),
        Course('IS',596,'[]',4,'Tue','','["Not Offered"]',0),
        Course('IS',690,'[]',0,'Fri','','["Not Offered"]',0),
        Course('IS',696,'[]',0,'Thu','','["Not Offered"]',0),
        Course('IS',698,'[]',0,'Fri','','["Not Offered"]',0),
        Course('CSC',435,'CSC 403 and CSC 407',4,'Sat','','["Autumn", "Winter", "Spring"]',1),
        Course('SE',430,'CSC 403',4,'Thu','','["Autumn", "Winter", "Spring"]',1),
        Course('SE',549,'SE 430 or SE 450',4,'Mon','','["Not Offered"]',0),
        Course('SE',433,'CSC 403',4,'Thu','','["Not Offered"]',0),
        Course('SE',450,'CSC 403',4,'Sun','','["Autumn", "Winter", "Spring"]',1),
        Course('SE',468,'IT 403 and (SE430 or SE450)',4,'Sat','','["Not Offered"]',0),
        Course('SE',477,'Knowledge of the Software development life cycle model, for example through courses such as SE430, ECT455, IS425, MIS555 or through appropriate wor),experience.',4,'Wed','','["Autumn", "Winter", "Spring"]',0),
        Course('SE',480,'SE 450',4,'Fri','','["Not Offered"]',1),
        Course('SE',491,'SE 450.',4,'Fri','','["Not Offered"]',1),
        Course('SE',529,'IT 403 and SE 430 or consent.',4,'Fri','','["Not Offered"]',0),
        Course('SE',533,'SE 450.',4,'Fri','','["Not Offered"]',0),
        Course('SE',690,'Consent of the instructor.',4,'Mon','','["Not Offered"]',0),
        Course('SE',696,'Consent of advisor.',0,'Thu','','["Not Offered"]',0),
        Course('SE',698,'Successful defense of a Master''s Thesis. (0 credit hours)',0,'Fri','','["Not Offered"]',0),
        Course('SE',699,'SE 698. (0 credit hours)',0,'Fri','','["Not Offered"]',0),
        Course('ECT',455,'CSC 401 or IT 411 or ECT 410 or ECT 436 or HCI 430',4,'Sat','','["Not Offered"]',0),
        Course('ECT',480,'ECT 424',4,'Fri','','["Not Offered"]',0),
        Course('ECT',481,'CSC 401 or IT 411 or ECT 410 or ECT 436',4,'Sat','','["Not Offered"]',0),
        Course('ECT',582,'ECT 424 or CSC 435 or TDC 463',4,'Sat','','["Not Offered"]',1),
        Course('ECT',589,'Completion of ten or more School of Computing MS level courses is required.',4,'Fri','','["Not Offered"]',1),
        Course('ECT',596,'Consent of instructor.',4,'Sat','','["Not Offered"]',0),
        Course('ECT',690,'Consent of the instructor.  (variable credit)',0,'Fri','','["Not Offered"]',0),
        Course('ECT',696,'[]',0,'Sat','','["Not Offered"]',0),
        Course('ECT',698,'Consent of advisor.  (2 quarter hours)',0,'Fri','','["Not Offered"]',0),
        Course('TDC',463,'[]',4,'Sun','','["Autumn", "Winter", "Spring"]',1),
        Course('TDC',464,'TDC 413',4,'Sun','','["Winter", "Spring"]',1),
        Course('TDC',511,'TDC 411 and TDC 460 and TDC 463',4,'Fri','','["Autumn", "Spring"]',1),
        Course('TDC',512,'TDC 464',4,'Fri','','["Autumn"]',1),
        Course('TDC',514,'TDC 463 and TDC 464.',4,'Fri','','["Spring"]',0),
        Course('TDC',468,'(TDC 463 or CSC 435) and CSC 404',4,'Fri','','["Winter"]',0),
        Course('TDC',562,'TDC 463',4,'Fri','','["Once Per Year"]',0),
        Course('TDC',563,'TDC 463',4,'Sat','','["Autumn", "Winter", "Spring"]',1),
        Course('TDC',567,'[]',4,'Fri','','["Spring"]',0),
        Course('TDC',568,'TDC 463',4,'Fri','','["Winter"]',0),
        Course('TDC',477,'TDC 463 or CSC 435',4,'Sun','','["Autumn", "Winter", "Spring"]',1),
        Course('TDC',593,'[]',4,'Thu','','["Not Offered"]',0),
        Course('TDC',690,'Consent of the instructor. (variable credit)',0,'Fri','','["Not Offered"]',0),
        Course('TDC',696,'Consent of advisor. Independent study form required.',0,'Thu','','["Not Offered"]',0),
        Course('TDC',698,'Consent of advisor. Independent study form required. (2 quarter hours)',0,'Fri','','["Not Offered"]',0),
        Course('HCI',445,'IT 403 and (HCI 440 or HCI 441)',4,'Sun','','["Not Offered"]',1),
        Course('HCI',422,'HCI 440 or consent of the instructor.',4,'Fri','','["Not Offered"]',0),
        Course('HCI',430,'IT 411.  Students must have completed or be concurrently enrolled in HCI 440 or HCI 441 to register for this course.',4,'Sat','','["Not Offered"]',1),
        Course('HCI',440,'None',0,'Fri','','["Autumn", "Winter", "Spring"]',1),
        Course('HCI',450,'IT 403',4,'Fri','','["Not Offered"]',1),
        Course('HCI',460,'IT 403 and (HCI 440 or HCI 441)',4,'Sun','','["Not Offered"]',1),
        Course('HCI',511,'HCI 445 (HCI 460 recommended)',4,'Sun','','["Not Offered"]',1),
        Course('HCI',512,'IT 403 and HCI 470',4,'Sun','','["Not Offered"]',0),
        Course('HCI',513,'IS 422 or HCI 430',4,'Fri','','["Not Offered"]',0),
        Course('HCI',590,'[]',4,'Tue','','["Not Offered"]',1),
        Course('HCI',594,'Completion of the HCI core courses or consent of the instructor.',4,'Sat','','["Not Offered"]',1),
        Course('HCI',690,'Instructor consent required. (variable credit)',0,'Fri','','["Not Offered"]',0),
        Course('CSC',697,'[]',0,'Sat','','["As Needed"]',0),
        Course('GPH',438,'GPH 425 or GPH 469.',4,'Sat','','["Not Offered"]',0),
        Course('HCI',402,'None',4,'Tue','','["Not Offered"]',1),
        Course('SE',452,'CSC 403',4,'Thu','','["Not Offered"]',1),
        Course('CSC',540,'CSC 471',4,'Thu','','["As Needed"]',0),
        Course('CSC',552,'SE 450 and CSC 407',4,'Sat','','["Autumn"]',1),
        Course('SE',560,'SE 450 OR ((CSC 383 or CSC 301)  and SE 430).',4,'Fri','','["Not Offered"]',0),
        Course('SE',591,'SE 491',4,'Fri','','["Not Offered"]',0),
        Course('HCI',470,'HCI 402 and HCI 406',4,'Sun','','["Not Offered"]',1),
        Course('ECT',583,'[]',4,'Sat','','["Not Offered"]',0),
        Course('ECT',584,'IT 403 AND (CSC 451 or CSC 453 or CSC 455)',4,'Fri','','["Not Offered"]',0),
        Course('ECT',586,'ECT 424',4,'Fri','','["Not Offered"]',0),
        Course('IS',570,'IS 430 or PM 430 or completion of five or more other SoC MS level courses should contact the course instructor or an advisor.',4,'Fri','','["Autumn'', ),Winter", "Spring"]',1),
        Course('CSC',536,'CSC 435',4,'Sat','','["Spring"]',0),
        Course('CSC',575,'CSC 403',4,'Thu','','["Not Offered"]',0),
        Course('ECT',587,'CSC 401 or IT 411 or ECT 410 or ECT 436 or ECT 455',4,'Sat','','["Not Offered"]',0),
        Course('HCI',530,'HCI 454',4,'Sun','','["Not Offered"]',0),
        Course('CSC',534,'SE 450',4,'Fri','','["Not Offered"]',0),
        Course('SE',554,'SE 450 or SE 452.',4,'Fri','','["Not Offered"]',0),
        Course('CSC',580,'SE 450',4,'Fri','','["Not Offered"]',0),
        Course('GPH',448,'GPH 438.',4,'Mon','','["Not Offered"]',0),
        Course('GPH',536,'GPH 469 or GAM 470',4,'Sat','','["Not Offered"]',0),
        Course('GPH',560,'any GPH 400-level course or consent of instructor.',4,'Mon','','["Not Offered"]',0),
        Course('CSC',440,'CSC 403',4,'Sat','','["Winter"]',0),
        Course('IS',467,'IT 403 or CSC 423',4,'Fri','','["Not Offered"]',1),
        Course('CSC',454,'CSC 451 or CSC 453 or CSC 455',4,'Sat','','["Summer"]',0),
        Course('SE',546,'[]',4,'Fri','','["Not Offered"]',0),
        Course('SE',482,'[]',4,'Mon','','["Not Offered"]',0),
        Course('CSC',553,'CSC 453.',4,'Sat','','["Winter"]',0),
        Course('CSC',601,'Completion of required courses. Independent Study form required.  (0 credit hours)',0,'Fri','','["Not Offered"]',0),
        Course('ECT',556,'[]',4,'Sun','','["Not Offered"]',0),
        Course('SE',691,'[]',0,'Sat','','["Not Offered"]',0),
        Course('TDC',460,'TDC 405 and TDC 413',4,'Sun','','["Autumn", "Winter", "Spring"]',1),
        Course('CSC',557,'CSC 439',4,'Fri','','["Not Offered"]',0),
        Course('CNS',594,'TDC 477 or CNS 533',4,'Fri','','["Not Offered"]',0),
        Course('CSC',482,'CSC 481',4,'Sat','','["As Needed"]',0),
        Course('CSC',521,'(CSC 402 or CSC 404) and CSC 423 or  consent of instructor',4,'Sat','','["Spring"]',0),
        Course('GPH',565,'[]',0,'Mon','','["Not Offered"]',0),
        Course('IS',505,'[]',4,'Wed','','["Autumn", "Winter", "Spring"]',1),
        Course('IS',430,'None',4,'Wed','','["Autumn", "Winter", "Spring"]',1),
        Course('ECT',565,'ECT 455',4,'Sat','','["Not Offered"]',0),
        Course('IS',456,'None',4,'Wed','','["Not Offered"]',0),
        Course('CSC',543,'[]',4,'Fri','','["Not Offered"]',0),
        Course('CSC',531,'[]',4,'Sat','','["As Needed"]',0),
        Course('CNS',599,'None',0,'Fri','','["Not Offered"]',0),
        Course('CNS',477,'CNS 440',4,'Sat','','["Not Offered"]',1),
        Course('TDC',532,'TDC 512',4,'Fri','','["Winter"]',0),
        Course('IT',599,'None',0,'Sat','','["Not Offered"]',0),
        Course('TDC',431,'TDC 405',4,'Thu','','["Winter"]',0),
        Course('CSC',425,'CSC 423 or MAT 456 or consent of instructor',4,'Fri','','["Not Offered"]',1),
        Course('GPH',450,'HCI 470',4,'Wed','','["Not Offered"]',0),
        Course('HCI',454,'HCI 406 and (HCI 440 or HCI 441)',4,'Sun','','["Not Offered"]',1),
        Course('TDC',577,'TDC 477',4,'Fri','','["Autumn", "Spring"]',1),
        Course('IS',565,'Completion of five or more SoC MS level courses is required',4,'Sat','','["Not Offered"]',0),
        Course('CSC',431,'(CSC 401 and two quarters of calculus) or instructor permission',4,'Thu','','["Winter"]',0),
        Course('SE',456,'CSC 403',4,'Fri','','["Not Offered"]',0),
        Course('SE',556,'SE 456 and CSC 407',4,'Fri','','["Not Offered"]',0),
        Course('GAM',476,'CSC 461 and (SE 456 or SE 450)',4,'Fri','','["Not Offered"]',1),
        Course('GAM',594,'Completion Of Foundation Courses.',4,'Sat','','["Not Offered"]',0),
        Course('GPH',538,'GPH 438',4,'Mon','','["Not Offered"]',0),
        Course('GPH',540,'GPH 539',4,'Mon','','["Not Offered"]',0),
        Course('GPH',541,'GPH 539',4,'Mon','','["Not Offered"]',0),
        Course('CSC',525,'CSC 421.',4,'Sat','','["EO Academic Year"]',0),
        Course('IS',535,'SE 477 or IS 565 or ACCT 500 or IS 430 or PM 430 or ECT 455',4,'Fri','','["Autumn", "Winter", "Spring"]',1),
        Course('CNS',450,'CSC 407 or CNS 418',4,'Fri','','["Not Offered"]',1),
        Course('CSC',443,'[]',4,'Sun','','["As Needed"]',0),
        Course('IT',698,'Consent of advisor. (2 quarter hours)',0,'Thu','','["Not Offered"]',0),
        Course('CSC',559,'CSC 404 and (CSC 431 or CSC 521 or CSC 425)',4,'Sat','','["Spring"]',1),
        Course('GPH',580,'[]',4,'Sat','','["Not Offered"]',0),
        Course('HCI',599,'[]',0,'Thu','','["Not Offered"]',0),
        Course('SE',453,'[]',4,'Fri','','["Not Offered"]',0),
        Course('SE',457,'[]',4,'Fri','','["Not Offered"]',0),
        Course('CSC',438,'[]',4,'Sat','','["Autumn", "Spring"]',1),
        Course('CSC',695,'Consent of research advisor. Independent study form required. Students must successfully complete the foundation courses prior to their first enrollment i),CSC 695. (variable credit )',0,'Fri','','["Not Offered"]',0),
        Course('GPH',487,'[]',4,'Sat','','["Not Offered"]',0),
        Course('GAM',599,'None',0,'Fri','','["Not Offered"]',0),
        Course('GAM',424,'None',4,'Sat','','["Not Offered"]',0),
        Course('IT',432,'IT 411',4,'Fri','','["Not Offered"]',0),
        Course('IS',590,'[]',4,'Fri','','["Not Offered"]',0),
        Course('IS',599,'[]',0,'Thu','','["Not Offered"]',0),
        Course('GAM',450,'CSC 461 and (SE 456 or SE 450)',4,'Sat','','["Not Offered"]',0),
        Course('IS',435,'IS 421 or SE 430',4,'Fri','','["Not Offered"]',1),
        Course('CSC',439,'[]',4,'Sat','','["As Needed"]',0),
        Course('GAM',475,'CSC 461 and (SE 456 or SE 450)',4,'Sat','','["Not Offered"]',1),
        Course('GAM',575,'GAM 475',4,'Sat','','["Not Offered"]',0),
        Course('CSC',486,'CSC 461 and (SE 456 or SE 450)',4,'Sun','','["Not Offered"]',0),
        Course('GAM',690,'[]',4,'Fri','','["Not Offered"]',0),
        Course('GAM',691,'[]',0,'Fri','','["Not Offered"]',0),
        Course('GAM',453,'CSC 461 and (SE 456 or SE 450)',4,'Sat','','["Not Offered"]',0),
        Course('IS',506,'IS 505',4,'Fri','','["Not Offered"]',0),
        Course('SE',525,'CSC 435 and SE 450',4,'Fri','','["Not Offered"]',0),
        Course('SE',526,'[]',4,'Fri','','["Not Offered"]',0),
        Course('GAM',499,'Permission of instructor  (variable credit)',0,'Tue','','["Not Offered"]',0),
        Course('GAM',598,'For specific prerequisites, see syllabus or consult course instructor.  (variable credit)',0,'Fri','','["Not Offered"]',0),
        Course('HCI',421,'HCI 406',4,'Fri','','["Not Offered"]',0),
        Course('SE',511,'[]',0,'Fri','','["Not Offered"]',0),
        Course('IS',485,'IS 422 or IS 430 or PM 430.',0,'Fri','','["Not Offered"]',0),
        Course('GAM',491,'CSC 400 and CSC 403 and CSC 407',4,'Fri','','["Not Offered"]',0),
        Course('IS',444,'None',4,'Mon','','["Not Offered"]',1),
        Course('CNS',455,'None',4,'Wed','','["Not Offered"]',0),
        Course('CSC',495,'CSC 423 or SOC 412',4,'Wed','','["Autumn", "Spring"]',1),
        Course('IS',455,'None',4,'Tue','','["Not Offered"]',0),
        Course('CSC',465,'IT 403 and (CSC 401 or IT 411)',4,'Fri','','["Not Offered"]',1),
        Course('GAM',486,'CSC 471',4,'Fri','','["Not Offered"]',0),
        Course('SE',459,'SE 450',4,'Fri','','["Not Offered"]',1),
        Course('TDC',560,'TDC 460 AND  TDC 463',4,'Fri','','["Once Per Year"]',0),
        Course('TDC',594,'TDC 477 and TDC 511',4,'Fri','','["As Needed"]',0),
        Course('SE',582,'(SE 477 or PM 430 or IS 430) and (SE 430 or SE 482 or IS 485)',4,'Sat','','["Not Offered"]',0),
        Course('ECT',424,'[]',4,'Wed','','["Autumn", "Winter", "Spring"]',1),
        Course('ECT',436,'None',4,'Thu','','["Autumn", "Winter", "Spring"]',0),
        Course('CSC',500,'None',0,'Fri','','["Autumn", "Winter", "Spring"]',1),
        Course('IT',590,'Instructor consent required',0,'Mon','','["Not Offered"]',0),
        Course('CSC',583,'CSC 480',4,'Fri','','["Not Offered"]',0),
        Course('CNS',466,'CNS 440 or TDC 477',4,'Fri','','["Not Offered"]',0),
        Course('TDC',484,'TDC 413',4,'Sun','','["Spring"]',0),
        Course('HCI',580,'[]',4,'Sat','','["Not Offered"]',0),
        Course('CSC',436,'CSC 435 and CSC 447',4,'Fri','','["Not Offered"]',1),
        Course('CSC',471,'CSC 403 and CSC 407',4,'Sat','','["Winter"]',0),
        Course('TDC',478,'None',4,'Sun','','["Not Offered"]',1),
        Course('IS',500,'IS 430 OR PM 430 OR SE 477',4,'Fri','','["Not Offered"]',0),
        Course('IS',536,'[]',4,'Mon','','["Not Offered"]',0),
        Course('SE',598,'For specific prerequisites, see syllabus or consult course instructor. (variable credit)',0,'Fri','','["Not Offered"]',0),
        Course('TDC',542,'TDC 512',4,'Fri','','["Not Offered"]',0),
        Course('GAM',597,'See syllabus.',4,'Mon','','["Not Offered"]',0),
        Course('CNS',488,'CSC 407 or TDC 477',4,'Sat','','["Not Offered"]',0),
        Course('CSC',595,'For specific prerequisites, see syllabus or consult course instructor. (variable credit)',0,'Mon','','["Winter"]',1),
        Course('IS',580,'Completion of the foundation phase.',4,'Mon','','["Not Offered"]',0),
        Course('IS',579,'PM 430 or IS 430',4,'Fri','','["Not Offered"]',0),
        Course('CSC',555,'CSC 401 and ( CSC 453 or CSC 455) and (IS 467 or CSC 478)',4,'Sat','','["Autumn", "Spring"]',1),
        Course('HCI',520,'IT 403 and (HCI 440 or HCI 441) and HCI 450',4,'Sun','','["Not Offered"]',0),
        Course('HCI',514,'HCI 445 and HCI 460',4,'Sun','','["Not Offered"]',0),
        Course('SE',581,'SE 480',4,'Wed','','["Not Offered"]',0),
        Course('SE',475,'CSC 403',4,'Fri','','["Not Offered"]',1),
        Course('CSC',400,'None',4,'Mon','','["Autumn", "Winter", "Spring"]',1),
        Course('CSC',402,'CSC 401',4,'Wed','','["Autumn", "Winter", "Spring"]',1),
        Course('CSC',401,'None',4,'Tue','','["Autumn", "Winter", "Spring"]',1),
        Course('CSC',403,'CSC 402',4,'Thu','','["Autumn", "Winter", "Spring"]',1),
        Course('CSC',406,'CSC 401',4,'Sat','','["Autumn", "Winter", "Spring"]',1),
        Course('CSC',407,'CSC 406 and CSC 402',4,'Sat','','["Autumn", "Winter", "Spring"]',1),
        Course('CSC',404,'None',4,'Fri','','["Autumn", "Winter", "Spring"]',0),
        Course('TDC',405,'None',4,'Tue','','["Not Offered"]',1),
        Course('TDC',411,'None',4,'Fri','','["Not Offered"]',1),
        Course('TDC',413,'None',4,'Tue','','["Not Offered"]',1),
        Course('IT',403,'None',4,'Mon','','["Not Offered"]',1),
        Course('CNS',418,'TDC 411',4,'Fri','','["Not Offered"]',1),
        Course('ECT',410,'CSC 401 or IT 411',4,'Fri','','["Not Offered"]',1),
        Course('IS',400,'None',4,'Fri','','["Not Offered"]',0),
        Course('IT',411,'None',4,'Mon','','["Not Offered"]',1),
        Course('HCI',406,'None',4,'Tue','','["Not Offered"]',1),
        Course('CSC',412,'None',4,'Sat','','["Autumn", "Winter"]',1),
        Course('CSC',478,'IS 467 and CSC 401',4,'Fri','','["Not Offered"]',1),
        Course('CSC',529,'CSC 424 and  (IS 467 or ECT 584 or CSC 578)',4,'Mon','','["Not Offered"]',1),
        Course('CSC',433,'IT 403 and (CSC 401  or IT 411)',4,'Fri','','["Not Offered"]',0),
        Course('SE',599,'None',0,'Fri','','["Not Offered"]',0),
        Course('IS',431,'None',4,'Fri','','["Not Offered"]',0),
        Course('CNS',440,'None',4,'Fri','','["Not Offered"]',1),
        Course('SE',579,'SE 450',4,'Fri','','["Not Offered"]',0),
        Course('CSC',455,'CSC 401',4,'Sat','','["Autumn", "Winter", "Spring"]',1),
        Course('CNS',533,'CNS 440',4,'Sun','','["Not Offered"]',1),
        Course('CSC',461,'CSC 400 and CSC 403 and CSC 406',4,'Fri','','["Autumn"]',1),
        Course('TDC',599,'[]',0,'Fri','','["Not Offered"]',0),
        Course('CSC',672,'Instructor consent required',4,'Thu','','["Not Offered"]',0),
        Course('CNS',587,'CNS 477 and (IS 444 or CNS 490 or CNS 533 or CSC 439 or TDC 577)',4,'Fri','','["Not Offered"]',0),
        Course('CSC',472,'CSC 403 and CSC 407',4,'Sat','','["Autumn"]',1),
        Course('CNS',597,'For specific prerequisites, see syllabus or consult course instructor. (variable credit)',0,'Fri','','["Not Offered"]',0),
        Course('CSC',462,'GAM 491 or CSC 461',4,'Thu','','["As Needed"]',0),
        Course('HCI',441,'CSC 403',0,'Thu','','["Not Offered"]',0),
        Course('HCI',553,'HCI 454',4,'Sun','','["Not Offered"]',0),
        Course('GAM',695,'GAM 575 and consent of research advisor',0,'Tue','','["Not Offered"]',0),
        Course('SE',695,'Consent of research advisor. Independent study form required. Students must successfully complete the foundation courses prior to their first enrollment i),CSC 695. (variable credit)',0,'Fri','','["Not Offered"]',0),
        Course('CNS',489,'CSC 407 or CNS 418',4,'Sat','','["Not Offered"]',0),
        Course('CNS',490,'CNS 440',4,'Fri','','["Not Offered"]',0),
        Course('HCI',515,'HCI 445 and HCI 454 and HCI 430',4,'Sun','','["Not Offered"]',0),
        Course('IS',452,'None',4,'Tue','','["Not Offered"]',1),
        Course('CSC',576,'[]',4,'Sat','','["EO Winter"]',0),
        Course('GAM',425,'CSC 403',4,'Fri','','["Not Offered"]',1),
        Course('GAM',576,'GAM 575',4,'Fri','','["Not Offered"]',0),
        Course('IS',550,'CSC 451 or CSC 453 or CSC 455',4,'Fri','','["Not Offered"]',1),
        Course('SE',441,'CSC 403',4,'Thu','','["Not Offered"]',0),
        Course('HCI',522,'[]',4,'Fri','','["Not Offered"]',0)
    ]

    # role = UserRole("Admin")
    # db.session.add(role)

    # role_2 = UserRole("Faculty")
    # db.session.add(role_2)

    # role_3 = UserRole("Student")
    # db.session.add(role_3)

    # user = User('admin','admin@mail.depaul.edu','admin',1,0,'Information Systems','Software and Systems Development','Autumn',2017,'In-Class Only',1,'[]','{}')
    # db.session.add(user)

    for course in courses:
        db.session.add(course)

    db.session.commit()


    courses_taken = [Course.query.filter_by(id = x).first().title() for x in json.loads(user.taken)]
    degree_credits = len(courses_taken) * 4

    return redirect(url_for('home'))

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

    # create search object
    Path = Search()

    # TODO: link here to database
    #use database to set up root node () and courses offered by quarter (treated here as a dictionary)
    # offered = {
    #     "Autumn": ['CSC 400', 'CSC 401', 'CSC 402', 'CSC 403', 'CSC 406', 'CSC 407'],
    #     "Winter": ['CSC 400', 'CSC 401', 'CSC 402', 'CSC 403', 'CSC 406', 'CSC 407'],
    #     "Spring": ['CSC 400', 'CSC 401', 'CSC 402', 'CSC 403', 'CSC 406', 'CSC 407'],
    #     "Summer": ['CSC 400', 'CSC 401', 'CSC 402', 'CSC 403', 'CSC 406', 'CSC 407']
    # }
    offered = {"Autumn": [], "Winter": [], "Spring": [], "Summer": []}
    

    requirements = [
        ['CSC 400', 'CSC 401', 'CSC 402', 'CSC 403', 'CSC 406', 'CSC 407'], 
        ['CSC 421 ', 'CSC 435', 'CSC 447', 'CSC 453', 'SE 450'], 
        ['CSC 436', 'CSC 438', 'CSC 439', 'CSC 443', 'CSC 448', 'CSC 461', 'CSC 462', 'CSC 471', 'CSC 472', 'CSC 475', 'CSC 534', 'CSC 536', 'CSC 540', 'CSC 548', 'CSC 549', 'CSC 551', 'CSC 552', 'CSC 553', 'CSC 595', 'CNS 450', 'GAM 690', 'GAM 691', 'HCI 441', 'SE 441', 'SE 452', 'SE 459', 'SE 525', 'SE 526', 'SE 554', 'SE 560', 'TDC 478', 'TDC 484', 'TDC 568'], 
        ['CSC 431', 'CSC 440', 'CSC 444', 'CSC 489', 'CSC 503', 'CSC 521', 'CSC 525', 'CSC 531', 'CSC 535', 'CSC 547', 'CSC 557', 'CSC 580', 'CSC 591', 'SE 533'], 
        ['CSC 423', 'CSC 424', 'CSC 425', 'CSC 428', 'CSC 433', 'CSC 465', 'CSC 478', 'CSC 481', 'CSC 482', 'CSC 495', 'CSC 529', 'CSC 555', 'CSC 575', 'CSC 578', 'CSC 594', 'CSC 598', 'CSC 672', 'ECT 584', 'IS 467'], 
        ['CSC 433', 'CSC 452', 'CSC 454', 'CSC 478', 'CSC 529', 'CSC 543', 'CSC 549', 'CSC 551', 'CSC 553', 'CSC 554', 'CSC 555', 'CSC 575', 'CSC 589'], 
        ['CSC 457', 'CSC 458', 'CSC 478', 'CSC 480', 'CSC 481', 'CSC 482', 'CSC 495', 'CSC 528', 'CSC 529', 'CSC 538', 'CSC 575', 'CSC 576', 'CSC 577', 'CSC 578', 'CSC 583', 'CSC 587', 'CSC 592', 'CSC 594', 'ECT 584', 'GEO 441', 'GEO 442', 'IS 467'], 
        ['SE 430', 'SE 433', 'SE 441', 'SE 452', 'SE 453', 'SE 456', 'SE 457', 'SE 459', 'SE 475', 'SE 477', 'SE 480', 'SE 482', 'SE 491', 'SE 525', 'SE 526', 'SE 529', 'SE 533', 'SE 546', 'SE 549', 'SE 554', 'SE 556', 'SE 560', 'SE 579', 'SE 581', 'SE 582', 'SE 591'], 
        ['CSC 461', 'CSC 462', 'GAM 450', 'GAM 453', 'GAM 475', 'GAM 476', 'GAM 486', 'GAM 490', 'GAM 575', 'GAM 576', 'GAM 690', 'GAM 691', 'GPH 436', 'GPH 469', 'GPH 570', 'GPH 572', 'GPH 580', 'HCI 440', 'SE 456', 'SE 556']
    ]

    for course in Course.query.all():
        quarter_offered = json.loads(course.quarter_offered.replace('\'', "\""))
        for off in quarter_offered:
            if (off == "As Needed"):
                offered["Autumn"].append("{} {}".format(course.subject, course.course_number))
                offered["Spring"].append("{} {}".format(course.subject, course.course_number))
                offered["Summer"].append("{} {}".format(course.subject, course.course_number))
                offered["Winter"].append("{} {}".format(course.subject, course.course_number))
            if (off == "Autumn"):
                offered[off].append("{} {}".format(course.subject, course.course_number))
            if (off == "Spring"):
                offered[off].append("{} {}".format(course.subject, course.course_number))
            if (off == "Summer"):
                offered[off].append("{} {}".format(course.subject, course.course_number))
            if (off == "Winter"):
                offered[off].append("{} {}".format(course.subject, course.course_number))

    # TODO: use hardcoded electives, concentration etc. courses here, and use appropriate one for given major concentration

    assigned = []
    days = []

    taken = set(user.taken.split(","))

    units_left = 24
    # for course in taken:
    #     units_left -= 4

    # def __init__(self, num_quarters, assigned, taken, taken_overall, days, units_left, quarter, year, per_quarter, parent):
    root = Node(0, assigned, set(), set(), days, units_left, "Autumn", 2017, user.classes_per_term, None)

    path = Search.aStar(root, offered, requirements[0]+requirements[1], [],  0)

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
