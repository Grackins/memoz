#!/usr/bin/env python3
from curses import wrapper
from views import view_funcs, STATE_HOME, STATE_HALT
import curses

import time


def main(stdscr):
    state = STATE_HOME
    curses.curs_set(0)

    while state != STATE_HALT:
        state = view_funcs[state](stdscr)


wrapper(main)
