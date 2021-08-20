from .states import STATE_HOME
from .key_responsed import KeyResponsedView
from db import session_gen
from models import Card


class StatsView(KeyResponsedView):
    transitions = [
        (['q'], STATE_HOME, 'Quit'),
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.session = session_gen()
        self.cards_qs = self.session.query(Card).all()

    def get_body(self):
        cnt = [0] * 20
        for card in self.cards_qs:
            cnt[card.stage] += 1
        while cnt[-1] == 0:
            cnt.pop()

        header_line = ' Stage '
        sep_line = '       '
        count_line = '   #   '
        field_format = '{:^5d}'

        for i, c in enumerate(cnt):
            header_line += '|' + field_format.format(i)
            sep_line += '+' + '-' * 5
            count_line += '|' + field_format.format(c)
        header_line += '|'
        sep_line += '+'
        count_line += '|'

        total_line = f'{sum(cnt)} cards in total'

        return f'{sep_line}\n' \
            f'{header_line}\n' \
            f'{sep_line}\n' \
            f'{count_line}\n' \
            f'{sep_line}\n\n' \
            f'{total_line}\n'

    def __del__(self):
        self.session.close()
