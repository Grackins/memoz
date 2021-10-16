#!/usr/bin/env python3
import curses
import argparse

from db import migrate
from exporter import export_data
from importer import import_data
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
parser.add_argument(
    '--export',
    dest='export_data',
    action='store_true',
    help='export data as json',
)
parser.add_argument(
    '--import',
    dest='import_data',
    action='store_true',
    help='import data as json',
)
args = parser.parse_args()

if args.migrate:
    migrate()
if args.export_data:
    export_data()
    exit(0)
if args.import_data:
    import_data()
    exit(0)
curses.wrapper(main)
