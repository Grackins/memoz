from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

engine = create_engine(f'sqlite:////home/{os.getenv("USER")}/.memoz/default.sqlite3', echo=True)
Base = declarative_base()
session_gen = sessionmaker(bind=engine)


def migrate():
    Base.metadata.create_all(engine)
