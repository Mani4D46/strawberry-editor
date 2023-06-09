"""
Home page
"""
from ..page import Page
from ..consts import (
    UP, DOWN, ENTER, CR, LF
)
from ..settings import STYLES


class Home(Page):
    """
    Home Page
    """
    def __init__(self, window):
        self.keys = {None: self.__event_keypress__, UP: self.up_key_press,
                     DOWN: self.down_key_press, ENTER: self.select,
                     CR: self.select, LF: self.select}
        self.name = 'Home'
        self.icon = 'home'
        self.window = window

        self.options = ['New File       Ctrl + n',
                        'Open File      Ctrl + o',
                        'Open Project   Ctrl + o']
        self.options_executable = [self.new_file, self.open_file,
                                   self.open_file]
        self.selected_option = 0

    def __event_keypress__(self, _):
        pass

    def down_key_press(self):
        """Runs at down key press"""
        if self.selected_option < len(self.options) - 1:
            self.selected_option += 1

    def up_key_press(self):
        """Runs at up key press"""
        if self.selected_option > 0:
            self.selected_option -= 1

    def select(self):
        """Runs at enter key press"""
        self.options_executable[self.selected_option]()

    def __draw__(self):
        with open('_home_page/logo.txt', 'r', encoding='utf8') as file:
            file_text = file.read()
            first_line = file_text.split('\n')[1]
            text_lenth = (first_line.count('▄') + first_line.count('▀')
                          + first_line.count(' '))
            for line, text in enumerate(file_text.split('\n')):
                self.window.move_cursor(round((self.window.terminal_cols
                                               - text_lenth) / 2), 3 + line)
                self.window.write(text)
            max_lenth = len(max(self.options, key=len))
            for line, text in enumerate(self.options):
                self.window.move_cursor(round((self.window.terminal_cols
                                               - max_lenth
                                               - 1) / 2), 13 + line)
                if line == self.selected_option:
                    self.window.write(STYLES['home_page.selected'](text))
                else:
                    self.window.write(text)

    def new_file(self):
        """Opens a new file"""
        self.window.new_file()

    def open_file(self):
        """Opens a file"""
        self.window.open_file()

    def __cursor__(self):
        return {'is_hidden': True, 'position': [0, 0]}


class Extension():
    """Extension"""
    def __init__(self):
        self.commands = {'home_page.page': self.home_page()}

    def home_page(self):
        """Returns the home page"""
        return Home
