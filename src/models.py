import random
from datetime import timedelta, date
from sqlalchemy import Column, Integer, String, Date, Boolean
from sqlalchemy.ext.declarative import declarative_base

from db import Base, session_gen

duration = list()
duration.append(0)
duration.append(1)
for i in range(2, 20):
    duration.append(duration[-1] + duration[-2])


class Card(Base):
    __tablename__ = 'cards'

    id = Column(Integer, primary_key=True)
    question = Column(String)
    answer = Column(String)
    creation_date = Column(Date)
    ask_date = Column(Date)
    stage = Column(Integer)
    in_queue = Column(Boolean, default=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.creation_date = date.today()
        self.ask_date = date.today()
        self.stage = 0

    def __repr__(self):
        return '<Card q="{}">'.format(self.question)

    def apply_solution(self, correct: bool):
        self.stage = self.stage + 1 if correct else 0
        self.ask_date = date.today() + timedelta(days=duration[self.stage])
        self.in_queue = False


def get_date_cards_queryset(today):
    session = session_gen()
    return session.query(Card).filter(Card.ask_date <= today), session
