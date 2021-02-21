import curses
from datetime import date

from db import session_gen
from models import get_date_cards_queryset, get_date_single_card, Card
from utils import interaction_mode

STATE_HOME = 0
STATE_CARD = 1
STATE_ADD = 2
STATE_STATS = 3
STATE_HALT = -1


class BaseView:
    def __init__(self, scr):
        self.scr = scr

    def handle():
        raise Exception('Not implemented error')

    def get_header(self, height, width):
        welcome_msg = 'Welcome to MemoZ'

        bar = '+' + (width - 2) * '-' + '+'

        right_spaces = left_spaces = (width - 2 - len(welcome_msg)) // 2 * ' '
        if (width - len(welcome_msg)) % 2 == 1:
            right_spaces += ' '
        mid_line = '|' + left_spaces + welcome_msg + right_spaces + '|'

        return f'{bar}' \
               f'{mid_line}' \
               f'{bar}'

    @classmethod
    def as_view(cls):
        def view_func(scr):
            return cls(scr).handle()
        return view_func


class KeyResponsedView(BaseView):
    default_state = STATE_HOME
    transitions = list()

    def get_body(self):
        return ''

    def get_help(self):
        help_text = ''
        for keys, state, description in self.transitions:
            key = '|'.join(keys)
            help_text += f'{key}) {description}\n'
        return help_text

    def render(self):
        scr = self.scr
        scr.clear()
        scr.addstr(self.get_header(*scr.getmaxyx()))
        scr.addstr('\n')
        scr.addstr(self.get_body())
        scr.addstr('\n')
        scr.addstr(self.get_help())
        scr.refresh()

    def handle_action(self, key):
        for keys, state, _ in self.transitions:
            if key in keys:
                return state
        return self.default_state

    def handle(self):
        self.render()
        key = self.scr.getkey()
        return self.handle_action(key)


class HomeView(KeyResponsedView):
    transitions = [
        (['r'], STATE_CARD, 'Review'),
        (['a'], STATE_ADD, 'Add'),
        (['s'], STATE_STATS, 'Stats'),
        (['q'], STATE_HALT, 'Quit'),
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        cards_qs, session = get_date_cards_queryset(date.today())
        self.cards_cnt = cards_qs.count()
        session.close()

    def get_body(self):
        if self.cards_cnt == 1:
            return '1 card is waiting 4 you :D\n'
        else:
            return f'{self.cards_cnt} cards are waiting 4 you :D\n'


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

        header_line = ''
        sep_line = ''
        count_line = ''
        field_format = '{:^5d}'

        for i, c in enumerate(cnt):
            header_line += '|' + field_format.format(i)
            sep_line += '+' + '-' * 5
            count_line += '|' + field_format.format(c)
        header_line += '|'
        sep_line += '+'
        count_line += '|'
        
        return f'{sep_line}\n' \
                f'{header_line}\n' \
                f'{sep_line}\n' \
                f'{count_line}\n' \
                f'{sep_line}\n'

    def __del__(self):
        self.session.close()


class CardView(KeyResponsedView):
    transitions = [
        (['y'], STATE_CARD, 'Remember'),
        (['n'], STATE_HOME, 'Forget'),
        (['s'], None, 'Show/Hide Answer'),
        (['q'], STATE_HOME, 'Go Home'),
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.card, self.session = get_date_single_card(date.today())
        self.show_answer = False

    def handle_action(self, key):
        if key == 's':
            self.show_answer = not self.show_answer
            return self.handle()
        if key in 'ny':
            correct = key == 'y'
            self.card.apply_solution(correct)
            self.session.commit()
            self.session.close()
        return super().handle_action(key)

    def get_body(self):
        status = f'id:{self.card.id} -- level:{self.card.stage}'
        question_line = 'Q: {}'.format(self.card.question.decode('utf-8'))
        if self.show_answer:
            answer_line = 'A: {}'.format(self.card.answer.decode('utf-8'))
        else:
            answer_line = 'A: ?'
        return f'{status}\n\n{question_line}\n{answer_line}\n'

    def handle(self):
        if self.card:
            return super().handle()
        return STATE_HOME


class AddCardView(BaseView):
    @interaction_mode
    def handle(self):
        scr = self.scr
        scr.clear()

        scr.addstr(self.get_header(*scr.getmaxyx()))
        scr.addstr('\n')

        scr.addstr('Add a new card!\n\n')

        scr.addstr('Q: ')
        scr.refresh()
        question = scr.getstr(100)

        scr.addstr('A: ')
        scr.refresh()
        answer = scr.getstr(200)

        scr.addstr('\nPress <Enter> to keep the card.')
        key = scr.getch()
        scr.refresh()
        if key == ord('\n'):
            card = Card(question=question, answer=answer)
            session = session_gen()
            session.add(card)
            session.commit()
            session.close()

        return STATE_HOME


view_funcs = {
    STATE_HOME: HomeView.as_view(),
    STATE_CARD: CardView.as_view(),
    STATE_ADD: AddCardView.as_view(),
    STATE_STATS: StatsView.as_view(),
}
