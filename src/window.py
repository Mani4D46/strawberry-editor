"""Window"""
import os
import sys
import time
import threading
from pygments.formatters import Terminal256Formatter

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
    ENTER,
    F4
)

from .settings import ICONS, BOX, STYLES, CONFIGS
from .menus import Strawberry, File, Edit
from .extensions import extensions

CTRL_BACKSPACE = '\x7f'


class Window(object):
    """Window"""
    def __init__(self):
        self.stdout = sys.stdout
        self.terminal_cols = os.get_terminal_size().columns
        self.terminal_lines = os.get_terminal_size().lines
        self.can_draw = True

        self.menus = [Strawberry(), File(), Edit()]
        self.current_menu = 0
        self.menu_scroll_bar = 0
        self.is_menu_visible = False

        self.file_name = '<None>'

        self.input = [[]]
        self.input_col = 0
        self.input_line = 0
        self.is_in_input = True
        self.is_cursor_visible = True

        self.highlighter = lambda code, __: code
        self.highlighters = []

        self.completions = []
        self.is_auto_complete_visible = True
        self.auto_complete_scroll_bar = 0
        self.auto_completer = lambda _, __, ___: []
        self.auto_completers = []

        self.box = BOX
        self.icons = ICONS
        self.config = CONFIGS
        self.style = STYLES

    def start(self):
        """Runs at start of execution"""
        self.stdout.write((' ' * self.terminal_cols) * self.terminal_lines)

    def end(self):
        """Runs at end of execution"""
        self.can_draw = False
        self.clear()
        self.stdout.flush()
        sys.exit()

    def highlight(self, code):
        """Syntax highlighter"""
        return self.highlighter(code,
                                (Terminal256Formatter(style=self.config
                                                      ['theme'])))

    def key_right(self):
        """Right key press"""
        if self.is_in_input is True:
            if self.input_col < len(self.input[self.input_line]):
                self.input_col += 1
        else:
            if self.current_menu < len(self.menus) - 1:
                self.current_menu += 1

    def key_left(self):
        """Left key press"""
        if self.is_in_input is True:
            if self.input_col > 0:
                self.input_col -= 1
        else:
            if self.current_menu > 0:
                self.current_menu -= 1

    def key_up(self):
        """Up key press"""
        if self.is_in_input is True:
            if (self.is_auto_complete_visible is True and
               self.auto_complete_scroll_bar > 0):
                self.auto_complete_scroll_bar -= 1
            elif self.input_line > 0:
                self.input_line -= 1
                if self.input_col > len(self.input[self.input_line]):
                    self.key_end()
        elif (self.is_menu_visible is True and
              self.menu_scroll_bar > 0):
            self.menu_scroll_bar -= 1

    def key_down(self):
        """Down key press"""
        if self.is_in_input is True:
            if self.is_auto_complete_visible is True:
                self.auto_complete_scroll_bar += 1
            elif self.input_line < len(self.input) - 1:
                self.input_line += 1
                if self.input_col > len(self.input[self.input_line]):
                    self.key_end()
        elif self.is_menu_visible is True:
            self.menu_scroll_bar += 1

    def key_home(self):
        """Home key press"""
        self.input_col = 0

    def key_end(self):
        """End key press"""
        self.input_col = len(self.input[self.input_line])

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
        self.stdout.write(f'\033[21m\033[4m{character}\033[0m')

    def set_block_here(self, character):
        """Sets an under line under `character`"""
        self.stdout.write(f'\033[107m\033[30m{character}\033[0m')

    def clear(self):
        """Clears terminal"""
        self.move_cursor(0, 0)
        self.stdout.write((' ' * self.terminal_cols) * self.terminal_lines)
        self.move_cursor(0, 0)

    def clear_with_line(self):
        """Clears terminal and adds an line for line numbers"""
        self.move_cursor(0, 0)
        self.stdout.write(('~    \u2502' + (' ' * (self.terminal_cols - 6))) *
                          (self.terminal_lines))
        self.move_cursor(0, 1)
        self.stdout.write('     \u2502')
        self.move_cursor(0, 0)

    def draw_auto_complete(self, left, top, index):
        """Writes auto Completion"""
        if index >= len(self.completions):
            self.auto_complete_scroll_bar = len(self.completions) - 1
        equal_to_ten = len(self.completions[index: 10 + index]) == 10
        completions = (self.completions[index: 10 + index] if equal_to_ten
                       else self.completions)
        if len(completions) == 0:
            lenth = 0
            self.is_auto_complete_visible = False
        else:
            lenth = len(max([i.name for i in completions], key=len))
            self.is_auto_complete_visible = True
        apply_style = self.style['completionbox.color']
        if lenth > 0:
            self.move_cursor(left, top)
            self.stdout.write(apply_style(self.box[0] + (self.box[2] * (lenth
                                          + 6)) + self.box[1]))
        for line_index, i in enumerate(completions):
            self.move_cursor(left, top + line_index + 1)
            text = f'{self.box[3]}   '
            if (equal_to_ten is False and index == line_index) or (
                                                                   equal_to_ten
                                                                   is True and
                                                                   line_index
                                                                   == 0):
                text = f'{self.box[3]} ▎ '
            text += (self.icons[i.type] + (f'{i.name.ljust(lenth)} '
                     + self.box[3]))
            self.stdout.write(apply_style(text))
        self.move_cursor(left, top + len(completions) + 1)
        if lenth > 0:
            self.stdout.write(apply_style(self.box[4] +
                              f'{self.box[2] * (lenth + 6)}{self.box[5]}'))
        if self.is_auto_complete_visible is False:
            self.auto_complete_scroll_bar = 0

    def open_menu(self, left, top, index):
        """Opens an menu"""
        menu = self.menus[self.current_menu]
        if index >= len(menu.list) - 1:
            self.menu_scroll_bar = len(menu.list) - 1
        if len(menu.list) > 0:
            lenth = len(max(menu.list, key=len))
        else:
            lenth = 0
        apply_style = self.style['menubox.color']
        if lenth > 0:
            self.move_cursor(left, top)
            self.stdout.write(apply_style(self.box[0] + (self.box[2] * (lenth
                                                         + 4)) + self.box[1]))
            for line_index, i in enumerate(menu.list):
                self.move_cursor(left, top + line_index + 1)
                if line_index == index:
                    text = f'{self.box[3]} ▎ '
                else:
                    text = f'{self.box[3]}   '
                text += ((f'{i.ljust(lenth)} {self.box[3]}'))
                self.stdout.write(apply_style(text))
            self.move_cursor(left, top + len(menu.list) + 1)
            self.stdout.write(apply_style(self.box[4] + (self.box[2] * (lenth
                                                         + 4)) + self.box[5]))

    def draw(self):
        """Updates the screen"""
        while self.can_draw is True:
            self.cursor_hide()
            self.clear_with_line()
            self.stdout.write(self.style['menu.bg_color'](' ' *
                              self.terminal_cols))
            self.move_cursor(self.terminal_cols - len(self.config['menu.end']),
                             0)
            self.stdout.write(self.style["menu.end.unselected"](self.
                              config['menu.end']))
            self.move_cursor(0, 0)
            self.stdout.write(self.style["menu.start.selected"](
                self.config['menu.start']) if self.current_menu
                == 0 else self.style["menu.start.unselected"]
                (self.config['menu.start']))
            for menu_index, i in enumerate(self.menus):
                self.stdout.write(self.style["menu.selected"](
                                  f' {i.name} ')
                                  if menu_index == self.current_menu else
                                  self.style["menu.unselected"](f' {i.name} '))

            for line_index, i in enumerate(self.input):
                self.move_cursor(0, line_index + 2)
                self.stdout.write(str(line_index + 1).ljust(5) + '\u2502 ')
                self.stdout.write(self.highlight(''.join(i)).replace('\n', ''))
            self.move_cursor(self.input_col + 7, self.input_line + 2)
            if self.is_in_input is True:
                try:
                    character = (self.input[self.input_line]
                                 [self.input_col])
                except IndexError:
                    character = ' '
                if self.is_cursor_visible is True:
                    if self.config['cursor.shape'] == 'u':
                        self.set_underline_here(character)
                    elif self.config['cursor.shape'] == 'b':
                        self.set_block_here(character)
            if (self.input[self.input_line] != [] and
               self.is_auto_complete_visible):
                self.draw_auto_complete(self.input_col + 7, self.input_line
                                        + 3, self.auto_complete_scroll_bar)
            if self.is_menu_visible is True and self.current_menu != 0:
                menu_left = len('  '.join([i.name for i in self.menus[0:
                                          self.current_menu + 1]])) - 2
                self.move_cursor(menu_left, 1)
                self.open_menu(menu_left, 1, self.menu_scroll_bar)

            self.stdout.write('')
            self.move_cursor(0, 0)
            self.stdout.flush()

    def add_newline(self):
        """Adds an newline to input"""
        before = self.input[self.input_line][:self.input_col]
        after = self.input[self.input_line][self.input_col:]
        self.input[self.input_line] = after
        self.input[self.input_line:] = [before] + self.input[self.input_line:]
        self.input_line += 1
        self.input_col = 0

    def remove_line(self):
        """Removes an line from iput"""
        if self.input_line > 0:
            self.input.pop(self.input_line)
            self.input_line -= 1
            self.key_end()

    def add_character(self, character):
        """Adds an character to input"""
        self.input[self.input_line].insert(self.input_col, character)
        self.input_col += 1

    def remove_character(self):
        """Removes an character from input"""
        if self.input_col > 0:
            self.input[self.input_line].pop(self.input_col - 1)
            self.input_col -= 1
        elif self.input_line > 0:
            i = len(self.input[self.input_line])
            self.input[self.input_line - 1] += self.input[self.input_line]
            self.input[self.input_line] = []
            self.input_line -= 1
            self.input_col = len(self.input[self.input_line]) - i
            self.input.pop(self.input_line + 1)

    def remove_word(self):
        """Removes an word from input"""
        after_str = ''.join(self.input[self.input_line][self.input_col:])
        lenth = len(self.input[self.input_line])
        index = self.input_col
        input_str = ''.join(self.input[self.input_line][:self.input_col])
        self.input[self.input_line] = [*(input_str.rsplit(' ', 1)[0] +
                                         after_str)]
        self.input_col = index - (lenth - len(self.input[self.input_line]))

    def check_for_keys(self):
        """Checks for key_press in an while True(forever loop)"""
        while True:
            try:
                key = getch()
                if key == ESC:
                    if self.is_auto_complete_visible is True:
                        self.is_auto_complete_visible = False
                    elif self.is_menu_visible is True:
                        self.is_menu_visible = False
                    else:
                        self.is_in_input = not self.is_in_input
                elif key == LEFT:
                    self.key_left()
                    self.is_cursor_visible = True
                elif key == RIGHT:
                    self.key_right()
                    self.is_cursor_visible = True
                elif key == UP:
                    self.key_up()
                elif key == DOWN:
                    self.key_down()
                elif key == CTRL_Q:
                    self.end()
                elif self.is_in_input is True:
                    if key == ENTER:
                        self.add_newline()
                    elif key == DELETE:
                        self.remove_line()
                    elif key == BACKSPACE:
                        self.remove_character()
                    elif key == HOME:
                        self.key_home()
                    elif key == END:
                        self.key_end()
                    elif key == CTRL_BACKSPACE:
                        self.remove_word()
                    elif key == F4:
                        self.is_auto_complete_visible = True
                    elif ord(key[0]) in range(32, 127):
                        self.add_character(key[0])
                        self.is_auto_complete_visible = True
                    self.is_cursor_visible = True
                elif key == ENTER:
                    if self.is_menu_visible is False:
                        self.is_menu_visible = True
                    else:
                        (self.menus[self.current_menu].exec
                                   [self.menu_scroll_bar])(self)
                        self.key_end()
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

    def file_open(self, name, code=''):
        """Runs at file openning"""
        if code == '':
            code = '\n'.join([''.join(i) for i in self.input])
        self.file_name = name
        self.highlighter = lambda code, __: code
        self.auto_completer = lambda _, __, ___: []
        self.input = [[*i] for i in code.split('\n')]
        self.input_line = 0
        self.input_col = len(self.input[self.input_line])
        for i in self.highlighters:
            if self.file_name.split('.')[-1] in i[0]:
                self.highlighter = i[1]
        for i in self.auto_completers:
            if self.file_name.split('.')[-1] in i[0]:
                self.auto_completer = i[1]

    def extensions(self):
        """Extensions"""
        for i in extensions:
            if i.TYPE == 'Highlighter':
                self.highlighters.append([i.FILE_TYPES, i.highlighter])
            elif i.TYPE == 'AutoComplete':
                self.auto_completers.append([i.FILE_TYPES,
                                            i.auto_complete])
        while True:
            code = '\n'.join(''.join(i) for i in self.input)
            try:
                self.completions = self.auto_completer(code,
                                                       self.input_col,
                                                       self.input_line)
            except Exception:
                self.completions = []

    def main_loop(self):
        """Starts main loop"""
        self.start()
        threading.Thread(target=self.check_for_keys).start()
        threading.Thread(target=self.draw, daemon=True).start()
        threading.Thread(target=self.cursor, daemon=True).start()
        threading.Thread(target=self.extensions, daemon=True).start()
        self.file_open('<None>')
