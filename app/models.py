from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

db = SQLAlchemy()

engine = create_engine('sqlite:///database.db', echo=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

class User(Base):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('user_role.id'), nullable=False)
    active = db.Column(db.Integer, nullable=False)
    program = db.Column(db.String(120), nullable=False)
    concentration = db.Column(db.String(120), nullable=False)
    start_term = db.Column(db.String(10), nullable=False)
    start_year = db.Column(db.Integer, nullable=False)
    delivery_type = db.Column(db.Integer, nullable=False)
    classes_per_term = db.Column(db.Integer, nullable=False)
    taken = db.Column(db.String(120), nullable=False)
    last_path = db.Column(db.String(120), nullable=False)

    role = db.relationship("UserRole")

    paths = db.relationship("Path")
    

    def __init__(self, name, email, password, role_id, active, program, concentration, start_term, start_year, delivery_type, classes_per_term, taken, last_path="{}"):
        self.name = name
        self.email = email
        self.password = password
        self.role_id = role_id
        self.active = active
        self.program = program
        self.concentration = concentration
        self.start_term = start_term
        self.start_year = start_year
        self.delivery_type = delivery_type
        self.classes_per_term = classes_per_term
        self.taken = taken
        self.last_path = last_path

class Path(Base):
    __tablename__ = 'path'

    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    path = db.Column(db.String(120), nullable=False)

    def __init__(self, user_id, path):
        self.user_id = user_id
        self.path = path

class UserRole(Base):
    __tablename__ = 'user_role'

    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)

    def __init__(self, name):
        self.name = name

class CourseType(Base):
    __tablename__ = 'course_type'

    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)

    def __init__(self, name):
        self.name = name

class Course(Base):
    __tablename__ = 'course'

    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    course_number = db.Column(db.Integer, nullable=False)
    prereq = db.Column(db.String(400), unique=False, nullable=False)
    credits = db.Column(db.Integer, nullable=False)
    day_of_week = db.Column(db.String(100))
    # syllabus = db.Column(db.String(100))
    description = db.Column(db.String(700))
    quarter_offered = db.Column(db.String(100), nullable=False)

    delivery_method = db.Column(db.Integer, nullable=False)


    def __init__(self, subject, course_number, prereq, credits, day_of_week, description, quarter_offered, delivery_method):
        self.subject = subject
        self.course_number = course_number
        self.prereq = prereq
        self.credits = credits
        self.description = description
        # self.syllabus = syllabus
        self.quarter_offered = quarter_offered
        self.delivery_method = delivery_method
        self.day_of_week     = day_of_week

    def title(self):
        return "{} {}".format(self.subject, self.course_number)

class Term(Base): 
    __tablename__ = 'term'

    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    year = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    offered = db.Column(db.String(120), nullable=False)

    assigned = []

    def __init__(self, name, year, assigned, offered):
        # year of course
        self.year = year
        
        # term name, e.g., summer, winter etc.
        self.name = name
        
        # list of courses (course objects) offered that year
        self.offered = offered
        
        # already assigned courses this term
        self.assigned = assigned


    def next(self):
        if (self.name == "Winter"):
            return Term("Spring", self.year, [], self.off["Spring"][:])
        elif (self.name == "Spring"):
            return Term("Summer", self.year, [], self.off["Winter"][:])
        elif (self.name == "Summer"):
            return Term("Fall", self.year, [], self.off["Fall"][:])
        else:
            return Term("Winter", self.year + 1, [], self.off["Winter"][:])
       
    def __lt__(self, other):
        return id(self) < other(self)
    
    
    def __eq__(self, other):
        return self.year == other.year and self.name == other.name 
    
    def __hash__(self):
        if self.name == "Fall":
            return self.year*10 + 1 
        elif self.name == "Winter":
            return self.year*10 + 2 
        else:
            return self.year*10 + 3 
    
    def __repr__(self):
        return self.name + str(self.year)
    
    def __str__(self):
        return self.name + str(self.year) 

# Create tables.
Base.metadata.create_all(bind=engine)
