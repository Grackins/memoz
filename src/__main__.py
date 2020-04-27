#!/usr/bin/env python3
import curses

from db import migrate
from views import view_funcs, STATE_HOME, STATE_HALT


def main(stdscr):
    state = STATE_HOME
    curses.curs_set(0)

    while state != STATE_HALT:
        state = view_funcs[state](stdscr)


migrate()
curses.wrapper(main)
