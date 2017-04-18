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

# Create tables.
Base.metadata.create_all(bind=engine)
