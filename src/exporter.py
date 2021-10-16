import json

from db import session_gen
from models import Card


class CardExporter:
    date_format = '%Y/%m/%d'
    datetime_format = '%Y/%m/%d %H:%M:%S'

    def __init__(self, card):
        self.card = card

    def export(self):
        card = self.card
        return {
            'question': card.question,
            'answer': card.answer,
            'creation_date': self.card.creation_date.strftime(
                self.date_format,
            ),
            'ask_date': self.card.ask_date.strftime(
                self.date_format,
            ),
            'stage': card.stage,
            'in_queue': card.in_queue,
        }


def export_data():
    cards = []
    session = session_gen()
    for card in session.query(Card).all():
        cards.append(CardExporter(card).export())
    print(json.dumps(cards))
