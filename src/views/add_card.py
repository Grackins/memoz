from .base import BaseView
from .states import STATE_HOME
from utils import interaction_mode
from models import Card
from db import session_gen


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
        question = scr.getstr(100).decode()

        scr.addstr('A: ')
        scr.refresh()
        answer = scr.getstr(200).decode()

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
