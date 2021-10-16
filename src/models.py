from datetime import date, datetime
from sqlalchemy import Column, Integer, String, Date, Boolean, DateTime

from db import Base, session_gen


class Card(Base):
    __tablename__ = 'cards'

    id = Column(Integer, primary_key=True)
    question = Column(String)
    answer = Column(String)
    creation_date = Column(Date)
    ask_date = Column(DateTime)
    pask_date = Column(DateTime)
    ppask_date = Column(DateTime)
    in_queue = Column(Boolean, default=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.creation_date = date.today()
        self.ppask_date = datetime.now()
        self.pask_date = datetime.now()
        self.ask_date = datetime.now()

    def __repr__(self):
        return '<Card q="{}">'.format(self.question)

    def apply_solution(self, correct: bool):
        now = datetime.now()
        if correct:
            saved_ask_date = self.ask_date
            self.ask_date = now + (now - self.ppask_date)
            self.ppask_date = self.pask_date
            self.pask_date = saved_ask_date
        else:
            self.ask_date = now
            self.pask_date += (now - self.pask_date) / 2
            self.ppask_date = self.ppask_date
        self.in_queue = False

    def postpone(self):
        self.ask_date = datetime.now()

    def get_power(self):
        return datetime.now() - self.pask_date


def get_date_cards_queryset(today):
    session = session_gen()
    return session.query(Card).filter(Card.ask_date <= today), session
