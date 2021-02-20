import curses


def interaction_mode(func):
    def wrapper(*args, **kwargs):
        curses.echo()
        curses.curs_set(1)
        result = func(*args, **kwargs)
        curses.curs_set(0)
        curses.noecho()
        return result

    return wrapper

