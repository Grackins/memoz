import curses
import random
from datetime import date

from db import session_gen
from models import get_date_cards_queryset, get_date_single_card, Card
from utils import interaction_mode

STATE_HOME = 0
STATE_REVIEW_OLD_CARD = 1
STATE_REVIEW_NEW_CARD = 2
STATE_ADD = 3
STATE_STATS = 4
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
        (['o'], STATE_REVIEW_OLD_CARD, 'Review Old Card'),
        (['f'], STATE_REVIEW_NEW_CARD, 'Review Fresh Card'),
        (['a'], STATE_ADD, 'Add'),
        (['s'], STATE_STATS, 'Stats'),
        (['q'], STATE_HALT, 'Quit'),
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        cards_qs, session = get_date_cards_queryset(date.today())
        self.new_cards_cnt = cards_qs.filter(Card.stage == 0).count()
        self.old_cards_cnt = cards_qs.filter(Card.stage > 0).count()
        session.close()

    def get_body(self):
        if self.old_cards_cnt + self.new_cards_cnt == 1:
            return '1 card is waiting 4 you :D\n'
        else:
            return f'{self.old_cards_cnt}+{self.new_cards_cnt} ' \
                    'cards are waiting 4 you :D\n'


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


class CardReviewView(KeyResponsedView):
    transitions = [
        (['y'], None, 'Remember'),  # Should be set in subclasses
        (['n'], None, 'Forget'),    # Should be set in subclasses
        (['s'], None, 'Show/Hide Answer'),
        (['q'], STATE_HOME, 'Go Home'),
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init_data()
        self.show_answer = False

    def init_data():
        self.card, seld.session = None, None

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


class NewCardReviewView(CardReviewView):
    transitions = [
        (['y'], STATE_REVIEW_NEW_CARD, 'Remember'),
        (['n'], STATE_REVIEW_NEW_CARD, 'Forget'),
        (['s'], None, 'Show/Hide Answer'),
        (['q'], STATE_HOME, 'Go Home'),
    ]

    def init_data(self):
        super().init_data()
        cards_qs, self.session = get_date_cards_queryset(date.today())
        cards_qs = cards_qs.filter(Card.stage == 0).all()
        self.card = random.choice(cards_qs) if cards_qs else None


class OldCardReviewView(CardReviewView):
    transitions = [
        (['y'], STATE_REVIEW_OLD_CARD, 'Remember'),
        (['n'], STATE_REVIEW_OLD_CARD, 'Forget'),
        (['s'], None, 'Show/Hide Answer'),
        (['q'], STATE_HOME, 'Go Home'),
    ]

    def init_data(self):
        cards_qs, self.session = get_date_cards_queryset(date.today())
        cards_qs = cards_qs.filter(Card.stage > 0).all()
        self.card = random.choice(cards_qs) if cards_qs else None


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
    STATE_REVIEW_OLD_CARD: OldCardReviewView.as_view(),
    STATE_REVIEW_NEW_CARD: NewCardReviewView.as_view(),
    STATE_ADD: AddCardView.as_view(),
    STATE_STATS: StatsView.as_view(),
}
