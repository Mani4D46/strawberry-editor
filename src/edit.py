"""
Main text editor
"""
import pathlib

from pyperclip import paste
from pygments.formatters import Terminal256Formatter, TerminalFormatter

from .editor import Editor
from .consts import (
    UP, DOWN, LEFT, RIGHT, BACKSPACE, ENTER, LF, CR, END, HOME, CTRL_V
)
from .settings import BOX, CONFIGS


class TextEditor(Editor):
    """
    Text Editor
    """
    def __init__(self, window, file, text):
        self.keys = {None: self.__event_keypress__, UP: self.up_keypress,
                     DOWN: self.down_keypress, LEFT: self.left_keypress,
                     RIGHT: self.right_keypress, HOME: self.move_beginning,
                     END: self.move_end, CTRL_V: self.paste}
        self.file = file
        self.name = pathlib.Path(file).name
        self.file_extention = file.split('.')[-1]
        self.text = [list(i) for i in text.split('\n')]
        self.char_index = 0
        self.line_index = 0
        self.window = window
        self.horizontal_scroll = 0
        self.line_horizontal_scroll = 0
        if CONFIGS['editor.use_256_colors'] is True:
            self.formatter = Terminal256Formatter(style=CONFIGS[
                                                                'editor.style'
                                                               ])
        else:
            self.formatter = TerminalFormatter(style=CONFIGS['editor.style'])

    def __event_keypress__(self, key):
        if key[0] == BACKSPACE:
            if self.char_index > 0:
                self.text[self.line_index].pop(self.char_index - 1)
                self.char_index -= 1
            elif self.line_index > 0:
                line_lenth = len(self.text[self.line_index])
                self.text[self.line_index - 1] += self.text[self.line_index]
                self.text[self.line_index] = []
                self.line_index -= 1
                self.char_index = len(self.text[self.line_index]) - line_lenth
                self.text.pop(self.line_index + 1)
        elif key[0] in {CR, LF, ENTER}:
            before = self.text[self.line_index][:self.char_index]
            after = self.text[self.line_index][self.char_index:]
            self.text[self.line_index] = after
            self.text[self.line_index:] = ([before] + self.text
                                           [self.line_index:])
            self.line_index += 1
            self.char_index = 0
        elif ord(key[0]) > 31:
            self.text[self.line_index].insert(self.char_index, key[0])
            self.char_index += 1

    def paste(self):
        """Pastes a text to terminal"""
        for i in paste():
            self.__event_keypress__(i)

    def move_end(self):
        """Moves to end of line"""
        self.char_index = len(self.text[self.line_index])
        self.horizontal_scroll = len(self.text[self.line_index]) // 2

    def move_beginning(self):
        """Moves to beginning of line"""
        self.char_index = 0
        self.horizontal_scroll = 0

    def up_keypress(self):
        """Runs at up key press"""
        if self.line_index > 0:
            self.line_index -= 1
            if len(self.text[self.line_index]) < self.char_index:
                self.move_end()

    def down_keypress(self):
        """Runs at down key press"""
        if self.line_index < len(self.text) - 1:
            self.line_index += 1
            if len(self.text[self.line_index]) < self.char_index:
                self.move_end()

    def left_keypress(self):
        """Runs at left key press"""
        if self.char_index > 0:
            self.char_index -= 1
        if self.horizontal_scroll > 0:
            self.horizontal_scroll -= 1

    def right_keypress(self):
        """Runs at right key press"""
        if self.char_index <= len(self.text[self.line_index]) - 1:
            self.char_index += 1
            self.horizontal_scroll += 1

    def to_string(self):
        """Returns string version of text"""
        return '\n'.join([''.join(i) for i in self.text])

    def remove_word(self):
        """Returns string version of text"""
        return '\n'.join([''.join(i) for i in self.text])

    def make_line_num(self, line):
        """
        Makes Line Number String
        """
        rjust_len = CONFIGS['editor.line_number_rjust_lenth']
        rjust_char = CONFIGS['editor.line_number_rjust_character']
        return (str(line).rjust(rjust_len, rjust_char)
                + f' {BOX[3]} ')

    def __draw__(self):
        output = []
        output.append(self.make_line_num(''))

        self.line_horizontal_scroll = -(self.window.terminal_cols - 1
                                        - len(self.make_line_num('')))
        self.horizontal_scroll = self.line_horizontal_scroll

        for line, text in enumerate(self.to_string().split('\n')):
            line_num = self.make_line_num(line + 1)
            try:
                text = (self.window.extention_commands[
                            f'editor.highlight:{self.file_extention}'
                        ](text[self.horizontal_scroll:][:(self.window.
                                                          terminal_cols)
                                                        - len(self.
                                                              make_line_num('')
                                                              )],
                          self.formatter))
            except KeyError:
                text = text[self.horizontal_scroll:][:self.window.terminal_cols
                                                     - len(self.make_line_num
                                                           (''))]

            try:
                output.append((line_num + text))
            except IndexError:
                pass

        for _ in range(self.window.terminal_lines - len(output) - 2):
            output.append(self.make_line_num('~'))

        return '\n'.join(output)

    def __cursor__(self):
        return {'is_hidden': False, 'position': [self.char_index
                                                 + len(self.make_line_num('')),
                                                 self.line_index + 1]}
