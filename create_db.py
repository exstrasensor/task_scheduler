import sqlite3
import sqlalchemy
from models.base import Base

sqlite3.connect('db')

engine = sqlalchemy.create_engine('sqlite:///db')

Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

