from datetime import date

from .base import BaseView
from .states import STATE_HOME
from models import Card, get_date_cards_queryset


class WordStoreView(BaseView):
    default_state = STATE_HOME

    def init_data(self):
        cards_qs, session = get_date_cards_queryset(date.today())
        cards = cards_qs.filter(Card.in_queue == True)\
                        .order_by(Card.creation_date)\
                        .all()
        self.remaining = (cards, 0, 0)
        self.selected = (list(), 0, 0)
        self.session = session
        # TODO calculate it based on window size
        self.window_size = 10

    def get_body(self, height, width):
        left_len = (width - 1) // 2
        right_len = (width - 1) - left_len

        left_pos = 0
        right_pos = left_len + 1

        body = [[''] * width] * self.window_size
        # TODO I was here

    def render(self):
        scr = self.scr
        scr.clear()

        height, width = scr.getmaxyx()
        scr.addstr(self.get_header(height, width))
        self.addstr('\n')

        scr.addstr(self.get_body(height, width))

    def handle_action(self):
        pass

    def handle(self):
        self.init_data()
        while True:
            self.render()
            if self.handle_action():
                break
        
        self.save_selected_items()
        self.session.close()

        return self.default_state
