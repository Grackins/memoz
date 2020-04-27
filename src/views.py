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
    return STATE_HALT


view_funcs = dict()
view_funcs[STATE_HOME] = home_view
view_funcs[STATE_CARD] = card_view
