"""
Explorer page
"""
import os

from ..page import Page
from ..edit import TextEditor
from ..consts import (
    UP, DOWN, ENTER, CR, LF
)
from ..settings import STYLES, CONFIGS


class Explorer(Page):
    """
    Explorer Page
    """
    def __init__(self, window):
        self.keys = {None: self.__event_keypress__, UP: self.up_key_press,
                     DOWN: self.down_key_press, ENTER: self.select,
                     CR: self.select, LF: self.select}
        self.name = 'Explorer'
        self.icon = 'home'
        self.window = window

        self.path = os.getcwd()
        self.files = ['..'] + os.listdir(self.path)
        self.selected_file = 0
        self.vertical_scroll = 0
        self.min_vertical_scroll = 0

    def __event_keypress__(self, _):
        pass

    def down_key_press(self):
        """Runs at down key press"""
        if self.selected_file < len(self.files) - 1:
            self.selected_file += 1

    def up_key_press(self):
        """Runs at up key press"""
        if self.selected_file > 0:
            self.selected_file -= 1

    def select(self):
        """Runs at enter key press"""
        file_path = os.path.join(self.path, self.files[self.selected_file])
        if os.path.isfile(file_path):
            with (open(file_path, 'r', encoding=CONFIGS['default_encoding']) as
                  file):
                self.window.tabs.append(TextEditor(
                    self.window, file_path, file.read()
                ))
        else:
            self.path = file_path
            self.files = ['..'] + os.listdir(self.path)
            self.selected_file = 0
            self.vertical_scroll = 0
        self.min_vertical_scroll = 0

    def __draw__(self):
        if self.selected_file >= self.window.terminal_lines // 2:
            self.min_vertical_scroll = (self.selected_file -
                                        self.window.terminal_lines // 2) + 1
        else:
            self.min_vertical_scroll = 1
        self.vertical_scroll = (self.min_vertical_scroll +
                                self.window.terminal_lines - 1)

        for line, text in list(enumerate(self.files))[self.min_vertical_scroll
                                                      - 1: self.
                                                      vertical_scroll - 4]:
            self.window.move_cursor(1, line - self.min_vertical_scroll + 3)
            if line == self.selected_file:
                self.window.write(STYLES['explorer_page.selected'](text))
            else:
                self.window.write(text)

    def __cursor__(self):
        return {'is_hidden': True, 'position': [0, 0]}


class Extension():
    """Extension"""
    def __init__(self):
        self.commands = {'explorer_page.page': self.explorer_page()}

    def explorer_page(self):
        """Returns the explorer page"""
        return Explorer
