#!/usr/bin/env python3
import curses
import argparse

from db import migrate
from views import view_funcs
from views.states import STATE_SINGLE_CARD_REVIEW, STATE_HOME, STATE_HALT


def main(stdscr):
    state = STATE_SINGLE_CARD_REVIEW if args.single_mode else STATE_HOME
    curses.curs_set(0)

    while state != STATE_HALT:
        state = view_funcs[state](stdscr)


parser = argparse.ArgumentParser(
    prog='memoz',
    description='Memoize shits with Memoz',
)
parser.add_argument(
    '--single',
    dest='single_mode',
    action='store_true',
    help='run memoz in single card mode',
)
parser.add_argument(
    '--migrate',
    dest='migrate',
    action='store_true',
    help='migrate models into database',
)
args = parser.parse_args()

if args.migrate:
    migrate()
curses.wrapper(main)
