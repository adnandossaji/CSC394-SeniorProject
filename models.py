from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from app import db

engine = create_engine('sqlite:///database.db', echo=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

# Set your classes here.
class User(Base):
    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=False)
    role = db.Column(db.Integer, nullable=False) # FK
    active = db.Column(db.Integer, nullable=False)

    delivery_type = db.Column(db.Integer, nullable=False)
    program = db.Column(db.String(120), nullable=False)
    concentration = db.Column(db.String(120), nullable=False)
    taken = db.Column(db.String(120), unique=True, nullable=False)


    def __init__(self, name, email, password, role, active, delivery_type, program, concentration, taken):
        self.name = name
        self.email = email
        self.password = password
        self.role = role
        self.active = active
        self.delivery_type = delivery_type
        self.program = program
        self.concentration = concentration
        self.taken = taken		

class Role:
    __tablename__ = 'Role'

    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)

    def __init__(self, name):
        self.name = name

class CourseType:
    '''course objects (domains)'''
    __tablename__ = 'CourseType'

    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)

    def __init__(self, name):
        self.name = name

class Course:
    '''course objects (domains)'''
    __tablename__ = 'Course'

    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    course_id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    prereqs = db.Column(db.String(120), nullable=False)
    units = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    day = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)


    def __init__(self, course_id, prereqs, units, day):
        # TODO: link to database
        
        # course id (are these unique?)
        self.course_id = course_id

        # each course has an associated list of prereqs (a list containing other course objects)
        self.prereqs = prereqs
    
        # int: number of credits the course counts for
        self.units = units
        
        # day that class is held, integer: 1 = Monday, ..., 4 = Thursday, 0 = online; 
        self.day = day

    # when representing coures, give just course_id as integer
    def __repr__(self):
        return str(self.course_id)        
    
    def __str__(self):
        return str(self.course_id)
    
    # when adding courses, give course units value as integer
    def __radd__(self, other):
        return self.units + other
    
    def __add__(self, other):
        return self.units + other

    def __hash__(self):
        return self.course_id

    def __eq__(self, other):
        return self.course_id == other.course_id


class Term: 
    ''' term object, TODO: link to database '''

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
