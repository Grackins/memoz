from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

db_dir = f'/home/{os.getenv("USER")}/.memoz'
try:
    os.mkdir(db_dir)
except FileExistsError:
    pass

db_address = os.path.join(db_dir, 'default.sqlite3')
if not os.path.exists(db_address):
    open(db_address, 'w').close()

engine = create_engine(f'sqlite:///{db_address}', echo=False)
Base = declarative_base()
session_gen = sessionmaker(bind=engine)


def migrate():
    Base.metadata.create_all(engine)
