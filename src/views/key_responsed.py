from .base import BaseView
from .states import STATE_HOME


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
