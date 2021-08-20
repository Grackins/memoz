from .states import STATE_HOME
from .key_responsed import KeyResponsedView


class CardReviewView(KeyResponsedView):
    transitions = [
        (['y'], None, 'Remember'),  # Should be set in subclasses
        (['n'], None, 'Forget'),    # Should be set in subclasses
        (['p'], None, 'Postpone'),  # Should be set in subclasses
        (['s'], None, 'Show/Hide Answer'),
        (['q'], STATE_HOME, 'Go Home'),
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init_data()
        self.show_answer = False

    def init_data(self):
        self.card, self.session = None, None

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
        question_line = 'Q: {}'.format(str(self.card.question))
        if self.show_answer:
            answer_line = 'A: {}'.format(str(self.card.answer))
        else:
            answer_line = 'A: ?'
        return f'{status}\n\n{question_line}\n{answer_line}\n'

    def handle(self):
        if self.card:
            return super().handle()
        return STATE_HOME
