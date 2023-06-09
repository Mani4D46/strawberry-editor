"""
Main text editor
"""
import pathlib
import threading

from pyperclip import paste
from pygments.formatters import Terminal256Formatter, TerminalFormatter

from .page import Page
from .consts import (
    BACKSPACE, ENTER, LF, CR
)
from .settings import (
    BOX, CONFIGS, STYLES,
    ICONS, FILE_ICONS,
    EDITOR_KEY_BINDINGS as KEYB
)


class TextEditor(Page):
    """
    Text Editor Page
    """
    def __init__(self, window, file, text):
        self.keys = {None: self.__event_keypress__,
                     KEYB['up']: self.up_keypress,
                     KEYB['down']: self.down_keypress,
                     KEYB['left']: self.left_keypress,
                     KEYB['right']: self.right_keypress,
                     KEYB['beginning_of_line']: self.move_beginning,
                     KEYB['end_of_line']: self.move_end,
                     KEYB['paste']: self.paste,
                     KEYB['remove_word']: self.remove_word,
                     KEYB['toggle_select_mode']: self.toggle_select_mode,
                     KEYB['toggle_auto_completion']:
                     self.toggle_auto_completion}
        self.file = file
        self.name = pathlib.Path(file).name
        self.icon = 'file'
        self.file_extension = file.split('.')[-1]
        self.text = [list(i) for i in text.split('\n')]

        self.char_index = 0
        self.line_index = 0
        self.is_in_select_mode = False
        self.selected_start_char_index = 0
        self.selected_start_line_index = 0
        self.selected_char_index = 0
        self.selected_line_index = 0

        self.window = window

        try:
            self.syntax_highlighter = self.window.extension_commands[
                f'editor.highlight:{self.file_extension}'
            ]
        except KeyError:
            self.syntax_highlighter = self.default_highlighter

        self.auto_completion_suggestions = []
        self.show_auto_completion = True
        self.selected_completion = 0

        self.horizontal_scroll = 0
        self.line_horizontal_scroll = 0
        self.max_vertical_scroll = 0
        self.min_vertical_scroll = 0
        self.max_horizontal_scroll = 0
        self.min_horizontal_scroll = 0
        if CONFIGS['editor.use_256_colors'] is True:
            self.formatter = Terminal256Formatter(style=CONFIGS[
                                                                'editor.style'
                                                               ])
        else:
            self.formatter = TerminalFormatter(style=CONFIGS['editor.style'])

        auto_completions_daemon = threading.Thread(target=self.
                                                   set_auto_completions,
                                                   daemon=True)
        auto_completions_daemon.start()

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

    def default_highlighter(self, *inputs):
        """
        Just a function to return the first inputs
        """
        return inputs[0]

    def toggle_select_mode(self):
        """Toggles select mode"""
        self.is_in_select_mode = not self.is_in_select_mode
        if self.is_in_select_mode is True:
            self.selected_start_char_index = self.char_index
            self.selected_start_line_index = self.line_index
            self.selected_char_index = self.char_index
            self.selected_line_index = self.line_index

    def toggle_auto_completion(self):
        """Toggles Auto Completion"""
        self.show_auto_completion = not self.show_auto_completion

    def paste(self):
        """Pastes a text to terminal"""
        for i in paste():
            if ord(i) > 31:
                self.__event_keypress__(i)

    def move_end(self):
        """Moves to end of line"""
        self.char_index = len(self.text[self.line_index])
        self.horizontal_scroll = len(self.text[self.line_index]) // 2
        self.selected_char_index = self.char_index
        self.selected_line_index = self.line_index

    def move_beginning(self):
        """Moves to beginning of line"""
        self.char_index = 0
        self.horizontal_scroll = 0
        self.selected_char_index = self.char_index
        self.selected_line_index = self.line_index

    def up_keypress(self):
        """Runs at up key press"""
        if self.line_index > 0:
            self.line_index -= 1
            if len(self.text[self.line_index]) < self.char_index:
                self.move_end()
        self.selected_char_index = self.char_index
        self.selected_line_index = self.line_index

    def down_keypress(self):
        """Runs at down key press"""
        if self.line_index < len(self.text) - 1:
            self.line_index += 1
            if len(self.text[self.line_index]) < self.char_index:
                self.move_end()
        self.selected_char_index = self.char_index
        self.selected_line_index = self.line_index

    def left_keypress(self):
        """Runs at left key press"""
        if self.char_index > 0:
            self.char_index -= 1
        self.selected_char_index = self.char_index
        self.selected_line_index = self.line_index

    def right_keypress(self):
        """Runs at right key press"""
        if self.char_index <= len(self.text[self.line_index]) - 1:
            self.char_index += 1
        self.selected_char_index = self.char_index
        self.selected_line_index = self.line_index

    def to_string(self):
        """Returns string version of text"""
        return '\n'.join([''.join(i) for i in self.text])

    def remove_word(self):
        """Returns string version of text"""
        last_word = ''.join(self.text[self.line_index]).rsplit(' ', 1)[1]
        self.text[self.line_index] = (self.text[self.line_index]
                                      [0: -len(last_word)])
        self.char_index = len(self.text[self.line_index]) - len(last_word)

    def get_icon(self):
        """Returns name of icon by file extension"""
        if self.file_extension in FILE_ICONS:
            return FILE_ICONS[self.file_extension]
        else:
            return 'file'

    def make_line_num(self, line):
        """Makes Line Number String"""
        rjust_len = CONFIGS['editor.line_number_rjust_lenth']
        rjust_char = CONFIGS['editor.line_number_rjust_character']
        line_num = (str(line).rjust(rjust_len, rjust_char)
                    + f' {BOX[3]} ')

        if line == self.line_index + 1:
            line_num = STYLES['editor.lines.selected'](line_num)

        return line_num

    def __draw__(self):
        self.window.move_cursor(0, 1)
        self.window.write(self.make_line_num(''))

        problems = [[] for _ in range(len(self.text) + 1)]

        try:
            linter_output = self.window.extension_commands[
                                f'editor.linter:{self.file_extension}'
                            ](self.to_string())
        except KeyError:
            linter_output = []

        for i in linter_output:
            problems[i[0] - 1].append(f'{ICONS[i[2]]} {i[1]}: {i[3]}')

        max_text_lenth = (self.window.terminal_cols -
                          len(self.make_line_num('')))

        self.min_horizontal_scroll = max(0, self.char_index - max_text_lenth)
        self.max_horizontal_scroll = (self.min_horizontal_scroll +
                                      max_text_lenth)

        self.max_vertical_scroll = (self.min_vertical_scroll +
                                    self.window.terminal_cols - 1)

        if self.line_index >= self.window.terminal_lines // 2:
            self.min_vertical_scroll = (self.line_index -
                                        self.window.terminal_lines // 2) + 1
        else:
            self.min_vertical_scroll = 1
        self.max_vertical_scroll = (self.min_vertical_scroll +
                                    self.window.terminal_lines - 1)

        for line_number in range(2, self.window.terminal_lines
                                 - 1):
            self.window.move_cursor(0, line_number)
            self.window.write(self.make_line_num('~'))

        for line, chars in list(enumerate(self.text))[self.min_vertical_scroll
                                                      - 1:
                                                      self.max_vertical_scroll
                                                      - 4]:
            if problems[line] != []:
                problems_str = ' ' + problems[line][0]
            else:
                problems_str = ''
            self.window.move_cursor(0, 3 + line - self.min_vertical_scroll)
            text = self.syntax_highlighter(''.join(chars)[
                                  self.min_horizontal_scroll:
                                  self.max_horizontal_scroll
                              ], self.formatter)
            self.window.write(self.make_line_num(line))
            self.window.write(text)
            self.window.write(problems_str)

    def set_auto_completions(self):
        """
        Gets auto completion suggestions from extension and then sets
        `self.auto_completion_suggestions` to output of that
        """
        try:
            plugin_output = self.window.extension_commands[
                f'editor.auto_complete:{self.file_extension}'
            ](self.to_string(), self.char_index + 1, self.line_index + 1)
        except KeyError:
            plugin_output = []
        self.auto_completion_suggestions = plugin_output

    def __cursor__(self):
        if self.line_index >= self.window.terminal_lines // 2:
            line = self.window.terminal_lines // 2
        else:
            line = self.line_index
        return {'is_hidden': False, 'position': [self.char_index
                                                 + len(self.make_line_num('')),
                                                 line + 1]}
