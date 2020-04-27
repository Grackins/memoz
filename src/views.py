from _curses import KEY_SRESET
from datetime import date

from db import session_gen
from models import get_date_single_card

STATE_HOME = 0
STATE_CARD = 1
STATE_HALT = -1


def print_header(scr):
    scr.addstr(0, 0, "+--------------------+")
    scr.addstr(1, 0, "|  Welcome to MemoZ  |")
    scr.addstr(2, 0, "+--------------------+")
    return 4


def home_view(scr):
    scr.clear()
    current_line = print_header(scr)
    scr.addstr(current_line, 0, "cards are waiting 4 U")
    current_line += 1
    scr.addstr(current_line, 0, "press any key to start")
    scr.refresh()

    scr.getkey()
    return STATE_CARD


def card_view(scr):
    card, session = get_date_single_card(date.today())
    if card is None:
        return STATE_HALT
    show_answer = False

    while True:
        scr.clear()
        current_line = print_header(scr)

        scr.addstr(current_line, 0, "Q: {}".format(card.question))
        current_line += 1

        scr.addstr(current_line, 0, "A: {}".format(card.answer if show_answer else '?!?!'))
        current_line += 2

        scr.addstr(current_line, 0, "press <s> to show/hide answer")
        current_line += 1

        scr.addstr(current_line, 0, "press <y> if you remember the answer")
        current_line += 1

        scr.addstr(current_line, 0, "press <n> if you don't remember the answer")

        scr.refresh()

        key = scr.getkey()
        if key == 's' or key == 'S':
            show_answer = not show_answer
        elif key == 'y' or key == 'Y':
            correct = True
            break
        elif key == 'n' or key == 'N':
            correct = False
            break

    card.apply_solution(correct)
    session.commit()
    return STATE_HOME


view_funcs = dict()
view_funcs[STATE_HOME] = home_view
view_funcs[STATE_CARD] = card_view
