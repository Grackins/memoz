import json
import sys
from datetime import datetime

from db import session_gen
from models import Card


class CardImporter:
    date_format = '%Y/%m/%d'
    datetime_format = '%Y/%m/%d %H:%M:%S'

    def __init__(self, data):
        self.data = data

    def get(self):
        data = self.data
        card = Card()
        card.question = data['question']
        card.answer = data['answer']
        card.creation_date = datetime.strptime(
            data['creation_date'],
            self.date_format,
        ).date()
        card.ask_date = datetime.strptime(
            data['ask_date'],
            self.datetime_format,
        )
        card.pask_date = datetime.strptime(
            data['pask_date'],
            self.datetime_format,
        )
        card.ppask_date = datetime.strptime(
            data['ppask_date'],
            self.datetime_format,
        )
        card.in_queue = data['in_queue']
        return card


def import_data():
    cards = json.loads(sys.stdin.read())
    session = session_gen()
    for card in cards:
        card = CardImporter(card).get()
        session.add(card)
    session.commit()
    session.close()
