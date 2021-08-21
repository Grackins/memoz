from datetime import date
import random

from .card_review import CardReviewView
from .states import STATE_HALT
from models import get_date_cards_queryset, Card


class SingleCardReviewView(CardReviewView):
    transitions = [
        (['y'], STATE_HALT, 'Remember'),
        (['n'], STATE_HALT, 'Forget'),
        (['s'], None, 'Show/Hide Answer'),
    ]

    def init_data(self):
        cards_qs, self.session = get_date_cards_queryset(date.today())
        cards_qs = cards_qs.filter(Card.in_queue == 'false').all()
        self.card = random.choice(cards_qs) if cards_qs else None

    def handle(self):
        super().handle()
        return STATE_HALT
