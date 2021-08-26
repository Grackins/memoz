from datetime import date
import random

from .card_review import CardReviewView
from .states import STATE_REVIEW_OLD_CARD, STATE_HOME
from models import get_date_cards_queryset, Card


class OldCardReviewView(CardReviewView):
    transitions = [
        (['y'], STATE_REVIEW_OLD_CARD, 'Remember'),
        (['n'], STATE_REVIEW_OLD_CARD, 'Forget'),
        (['p'], STATE_REVIEW_OLD_CARD, 'Postpone'),
        (['s'], None, 'Show/Hide Answer'),
        (['q'], STATE_HOME, 'Go Home'),
    ]

    def init_data(self):
        cards_qs, self.session = get_date_cards_queryset(date.today())
        cards_qs = cards_qs.filter(Card.in_queue == False).all()
        self.card = random.choice(cards_qs) if cards_qs else None
