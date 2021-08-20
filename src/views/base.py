class BaseView:
    def __init__(self, scr):
        self.scr = scr

    def handle():
        raise Exception('Not implemented error')

    def get_header(self, height, width):
        welcome_msg = 'Welcome to MemoZ'

        bar = '+' + (width - 2) * '-' + '+'

        right_spaces = left_spaces = (width - 2 - len(welcome_msg)) // 2 * ' '
        if (width - len(welcome_msg)) % 2 == 1:
            right_spaces += ' '
        mid_line = '|' + left_spaces + welcome_msg + right_spaces + '|'

        return f'{bar}' \
               f'{mid_line}' \
               f'{bar}'

    @classmethod
    def as_view(cls):
        def view_func(scr):
            return cls(scr).handle()
        return view_func
