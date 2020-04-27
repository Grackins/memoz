from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Card(Base):
    __tablename__ = 'cards'

    id = Column(Integer, primary_key=True)
    question = Column(String)
    answer = Column(String)
    ask_date = Column(Date)

    def __repr__(self):
        return '<Card q="{}">'.format(self.question)
