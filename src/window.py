"""Window things"""
import os
import sys
import time
import io
import threading

from yachalk import chalk
from readchar import readkey as getch
from readchar.key import (
    ESC,
    END,
    HOME,
    LEFT,
    RIGHT,
    UP,
    DELETE,
    DOWN,
    BACKSPACE,
    CTRL_Q,
    ENTER
)

from .tabs import Lambda, File, Edit

CTRL_BACKSPACE = '\x7f'


class Window(object):
    """Window"""
    def __init__(self):
        self.stdout = sys.stdout
        sys.stdout = io.StringIO("")
        self.terminal_cols = os.get_terminal_size().columns
        self.terminal_lines = os.get_terminal_size().lines
        self.can_draw = True

        self.tabs = [Lambda, File, Edit]
        self.current_tab = 0

        self.input = [[]]
        self.input_index = 0
        self.input_line = 0
        self.is_in_input = True
        self.is_cursor_visible = True

        self.config = {'tabs.start': ' \ue0ba', 'tabs.end': '\ue0bc ',
                       'cursor.shape': 'u'}
        self.style = {'tab.unselected': chalk.bg_gray,
                      'tab.start.selected': chalk.green,
                      'tab.start.unselected': chalk.gray,
                      'tab.end.unselected': chalk.gray,
                      'tab.selected': chalk.bg_green,
                      'tab.bg_color': chalk.bg_gray}

    def start(self):
        """Runs at start of execution"""
        self.stdout.write((' ' * self.terminal_cols) * self.terminal_lines)

    def end(self):
        """Runs at end of execution"""
        self.can_draw = False
        self.clear()
        self.stdout.flush()
        sys.exit()

    def key_right(self):
        """Right key press"""
        if self.is_in_input is True:
            if self.input_index < len(self.input[self.input_line]):
                self.input_index += 1
        else:
            if self.current_tab < len(self.tabs) - 1:
                self.current_tab += 1

    def key_left(self):
        """Left key press"""
        if self.is_in_input is True:
            if self.input_index > 0:
                self.input_index -= 1
        else:
            if self.current_tab > 0:
                self.current_tab -= 1

    def key_up(self):
        """Up key press"""
        if self.input_line > 0:
            self.input_line -= 1
            if self.input_index > len(self.input[self.input_line]):
                self.key_end()

    def key_down(self):
        """Down key press"""
        if self.input_line < len(self.input) - 1:
            self.input_line += 1
            if self.input_index > len(self.input[self.input_line]):
                self.key_end()

    def key_home(self):
        """Home key press"""
        self.input_index = 0

    def key_end(self):
        """End key press"""
        self.input_index = len(self.input[self.input_line])

    def move_cursor(self, left, top):
        """Moves terminal cursor"""
        self.stdout.write(f'\033[{top + 1};{left + 1}H')

    def cursor_hide(self):
        """Hides terminal cursor"""
        self.stdout.write('\033[?25l')

    def cursor_show(self):
        """Shows terminal cursor"""
        self.stdout.write('\033[?25h')

    def set_underline_here(self, character):
        """Sets an under line under `character`"""
        self.stdout.write(f'\033[4m{character}\033[0m')

    def clear(self):
        """Clears terminal"""
        self.move_cursor(0, 0)
        self.stdout.write((' ' * self.terminal_cols) * self.terminal_lines)
        self.move_cursor(0, 0)

    def clear_with_line(self):
        """Clears terminal and adds an line for line numbers"""
        self.move_cursor(0, 0)
        self.stdout.write(('     \u2502' + (' ' * (self.terminal_cols - 6))) *
                          self.terminal_lines)
        self.move_cursor(0, 0)

    def draw(self):
        """Updates the screen"""
        while self.can_draw is True:
            self.cursor_hide()
            self.clear_with_line()
            self.stdout.write(self.style['tab.bg_color'](' ' *
                              self.terminal_cols))
            self.move_cursor(self.terminal_cols - len(self.config['tabs.end']),
                             0)
            self.stdout.write(self.style["tab.end.unselected"](self.
                              config['tabs.end']))

            self.move_cursor(0, 0)
            self.stdout.write(self.style["tab.start.selected"](
                self.config['tabs.start']) if self.current_tab
                == 0 else self.style["tab.start.unselected"]
                (self.config['tabs.start']))
            for tab_index, i in enumerate(self.tabs):
                self.stdout.write(self.style["tab.selected"](
                                  f' {i.name} ')
                                  if tab_index == self.current_tab else
                                  self.style["tab.unselected"](f' {i.name} '))

            for line_index, i in enumerate(self.input):
                self.move_cursor(0, line_index + 2)
                self.stdout.write(str(line_index + 1).ljust(5) + '\u2502 ')
                self.stdout.write(''.join(i))
            self.move_cursor(self.input_index + 7, self.input_line + 2)
            if self.is_in_input is True:
                if self.config['cursor.shape'] == 'u':
                    try:
                        character = (self.input[self.input_line]
                                     [self.input_index])
                    except IndexError:
                        character = ' '
                    if self.is_cursor_visible is True:
                        self.set_underline_here(character)

            self.stdout.write('')
            self.move_cursor(0, 0)
            self.stdout.flush()

    def add_newline(self):
        """Adds an newline to input"""
        self.input[self.input_line + 1:] = ([], *self.input[self.input_line +
                                                            1:])
        self.input_line += 1
        self.input_index = 0

    def remove_line(self):
        """Removes an line from iput"""
        if self.input_line > 0:
            self.input[self.input_line] = []
            self.input_line -= 1
            self.input_index = len(self.input[self.input_line]) - 1

    def add_character(self, character):
        """Adds an character to input"""
        self.input[self.input_line].insert(self.input_index, character)
        self.input_index += 1

    def remove_character(self):
        """Removes an character from input"""
        if self.input_index > 0:
            self.input[self.input_line].pop(self.input_index - 1)
            self.input_index -= 1

    def remove_word(self):
        """Removes an word from input"""
        after_str = ''.join(self.input[self.input_line][self.input_index:])
        lenth = len(self.input[self.input_line])
        index = self.input_index
        input_str = ''.join(self.input[self.input_line][:self.input_index])
        self.input[self.input_line] = [*(input_str.rsplit(' ', 1)[0] +
                                         after_str)]
        self.input_index = index - (lenth - len(self.input[self.input_line]))

    def check_for_keys(self):
        """Checks for key_press in an while True(forever loop)"""
        while True:
            try:
                key = getch()
                if key == ESC:
                    self.is_in_input = not self.is_in_input
                elif key == LEFT:
                    self.key_left()
                elif key == RIGHT:
                    self.key_right()
                elif key == CTRL_Q:
                    self.end()
                elif self.is_in_input is True:
                    if key == ENTER:
                        self.add_newline()
                    elif key == DELETE:
                        self.remove_line()
                    elif key == BACKSPACE:
                        self.remove_character()
                    elif key == UP:
                        self.key_up()
                    elif key == DOWN:
                        self.key_down()
                    elif key == HOME:
                        self.key_home()
                    elif key == END:
                        self.key_end()
                    elif key == CTRL_BACKSPACE:
                        self.remove_word()
                    elif ord(key[0]) in range(32, 127):
                        self.add_character(key[0])
                self.is_cursor_visible = True
            except KeyboardInterrupt:
                self.end()
            except SystemExit:
                self.end()

    def cursor(self):
        """cursor blinking animation"""
        while True:
            if self.is_in_input is True:
                self.is_cursor_visible = True
                time.sleep(1)
                self.is_cursor_visible = False
                time.sleep(1)

    def main_loop(self):
        """Starts main loop"""
        self.start()
        threading.Thread(target=self.check_for_keys).start()
        threading.Thread(target=self.draw, daemon=True).start()
        threading.Thread(target=self.cursor, daemon=True).start()
