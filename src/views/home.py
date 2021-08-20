from datetime import date

from .key_responsed import KeyResponsedView
from .states import STATE_REVIEW_OLD_CARD, STATE_REVIEW_NEW_CARD,\
        STATE_ADD, STATE_STATS, STATE_HALT
from models import get_date_cards_queryset, Card


class HomeView(KeyResponsedView):
    transitions = [
        (['o'], STATE_REVIEW_OLD_CARD, 'Review Old Card'),
        (['f'], STATE_REVIEW_NEW_CARD, 'Review Fresh Card'),
        (['a'], STATE_ADD, 'Add'),
        (['s'], STATE_STATS, 'Stats'),
        (['q'], STATE_HALT, 'Quit'),
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        cards_qs, session = get_date_cards_queryset(date.today())
        self.new_cards_cnt = cards_qs.filter(Card.in_queue == 'true').count()
        self.old_cards_cnt = cards_qs.filter(Card.in_queue == 'false').count()
        session.close()

    def get_body(self):
        total_cards_cnt = self.old_cards_cnt + self.new_cards_cnt
        if total_cards_cnt == 0:
            return f'Congratulations!!! YOU ARE ALL DONE!!!'
        elif total_cards_cnt == 1:
            return f'{self.old_cards_cnt}+{self.new_cards_cnt} ' \
                    'card is waiting 4 you :D\n'
        else:
            return f'{self.old_cards_cnt}+{self.new_cards_cnt} ' \
                    'cards are waiting 4 you :D\n'
