from datetime import timedelta

from .states import STATE_HOME
from .key_responsed import KeyResponsedView
from db import session_gen
from models import Card


class StatsView(KeyResponsedView):
    transitions = [
        (['q'], STATE_HOME, 'Quit'),
    ]
    powers = [0, 1, 3, 7, 30, 60, 90, 180, 365, 1000, 10**4]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.session = session_gen()
        self.cards_qs = self.session.query(Card)

    def get_body(self):
        cnt = [0 for _ in self.powers]
        for card in self.cards_qs:
            power = card.get_power()
            if card.in_queue:
                power = 0
            ptr = 0
            while power > timedelta(self.powers[ptr]):
                ptr += 1
            cnt[ptr] += 1
        while cnt[-1] == 0:
            cnt.pop()

        header_line = ' Power '
        sep_line = '       '
        count_line = '   #   '
        field_format = '{:^5d}'

        for i, c in zip(self.powers, cnt):
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
