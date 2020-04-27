from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base

duration = [0 for _ in range(20)]
duration[0] = duration[1] = 1
for i in range(2, 20):
    duration[i] = duration[i - 1] + duration[i - 2]

Base = declarative_base()


class Card(Base):
    __tablename__ = 'cards'

    id = Column(Integer, primary_key=True)
    question = Column(String)
    answer = Column(String)
    creation_date = Column(Date)
    stage = Column(Integer)

    def __repr__(self):
        return '<Card q="{}">'.format(self.question)
