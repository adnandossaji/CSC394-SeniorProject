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
    perms = db.Column(db.Integer, nullable=False)
    active = db.Column(db.Integer, nullable=False)

    def __init__(self, name, email, password, perms=1, active=1):
        self.name = name
        self.email = email
        self.password = password
        self.perms = perms
        self.active = active

class Course(Base):
    __tablename__ = 'Courses'

    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String(100), unique=True, nullable=False)
    prereq = db.Column(db.String(100), unique=True, nullable=False)
    credits = db.Column(db.Integer, nullable=False)
    day_of_week = db.Column(db.String(100))
    syllabus = db.Column(db.String(100))
    quarter_offered = db.Column(db.String(100), nullable=False)
    delivery_method = db.Column(db.String(100), nullable=False)

    def __init__(self, id, name, prereq, credits, description, syllabus, quarter_offered, delivery_method):
        self.id = id
        self.name = name
        self.prereq = prereq
        self.credits = credits
        self.description = description
        self.syllabus = syllabus
        self.quarter_offered = quarter_offered
        self.delivery_method = delivery_method



# Create tables.
Base.metadata.create_all(bind=engine)
