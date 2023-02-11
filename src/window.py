"""Window"""
import sys
import time
import threading

import yachalk
# from pygments.formatters import Terminal256Formatter

from .settings import STYLES, CONFIGS, KEY_BINDINGS
from .menus import Strawberry, File, Edit
from .edit import TextEditor
from .consts import LEFT, RIGHT
from .terminal import TerminalWindow

BLOCK_CURSOR = yachalk.chalk.bg_white_bright.black
UNDERLINE_CURSOR = yachalk.chalk.underline


class Window(TerminalWindow):
    """Window"""
    def __init__(self):
        self.file_name = 'unnamed.txt'

        self.input_keys = {}

        self.tabs = [TextEditor(self)]
        self.current_tab = 0

        self.menus = [Strawberry(), File(), Edit()]
        self.current_menu = 0

        self.input_mode = True
        self.can_show_cursor = True

    def enter(self):
        """Runs at start of program"""
        self.start_terminal()

    def exit(self):
        """Runs at end of program"""
        self.show_cursor()
        self.clear_terminal()
        sys.exit()

    def toggle_input_mode(self):
        """Toggles between input mode"""
        self.input_mode = not self.input_mode

    def draw(self):
        """
        Draws the window
        """
        self.hide_cursor()
        while True:
            self.clear_terminal()
            self.write(STYLES['menu.bg_color'](' ' * self.terminal_cols))
            self.move_cursor(0, 0)
            for menu_index, menu in enumerate(self.menus):
                if menu_index == 0:
                    self.write(STYLES['menu.start.selected' if
                                      self.current_menu == 0 else
                                      'menu.start.unselected']
                               (CONFIGS['menu.start']))
                if menu_index == self.current_menu:
                    self.write(STYLES['menu.selected'](f' {menu.name} '))
                else:
                    self.write(STYLES['menu.unselected'](f' {menu.name} '))
            self.move_cursor(self.terminal_cols - len(CONFIGS['menu.end']),
                             0)
            self.write(STYLES['menu.end.unselected'](CONFIGS['menu.end']))

            current_tab = self.tabs[self.current_tab]
            editor_draw = current_tab.__draw__()
            cursor_pos = current_tab.__cursor__()['position']
            cursor_is_hidden = current_tab.__cursor__()['is_hidden']
            for line, i in enumerate(editor_draw.split('\n')):
                self.move_cursor(0, line + 1)
                if self.can_show_cursor is True and cursor_is_hidden is False:
                    if line == cursor_pos[1]:
                        if CONFIGS['cursor.shape'] == 'b':
                            i = [*i]
                            try:
                                i.insert(cursor_pos[0], BLOCK_CURSOR(
                                         i[cursor_pos[0]]))
                                i.pop(cursor_pos[0] + 1)
                            except IndexError:
                                i.insert(cursor_pos[0], BLOCK_CURSOR(' '))
                            i = ''.join(i)
                        elif CONFIGS['cursor.shape'] == 'u':
                            i = [*i]
                            try:
                                i.insert(cursor_pos[0], UNDERLINE_CURSOR(
                                         i[cursor_pos[0]]))
                                i.pop(cursor_pos[0] + 1)
                            except IndexError:
                                i.insert(cursor_pos[0], UNDERLINE_CURSOR(' '))
                            i = ''.join(i)
                self.write(i)

            self.flush()

    def execute_command(self, command):
        """Executes commands"""
        for i in command.split('-'):
            if i == 'exit':
                self.exit()
            elif i == 'toggle_input_mode':
                self.toggle_input_mode()

    def key_press(self):
        """Handels keypresses"""
        while True:
            key = self.getch()
            self.can_show_cursor = True
            if key in KEY_BINDINGS:
                self.execute_command(KEY_BINDINGS[key])
            elif (key in self.tabs[self.current_tab].keys and
                  self.input_mode is True):
                self.tabs[self.current_tab].keys[key]()
            elif self.input_mode is True:
                self.tabs[self.current_tab].keys[None](key)
            elif key == LEFT and self.input_mode is False:
                if self.current_menu > 0:
                    self.current_menu -= 1
            elif key == RIGHT and self.input_mode is False:
                if self.current_menu < len(self.menus) - 1:
                    self.current_menu += 1

    def mouse(self):
        """Cursor blink controller"""
        while True:
            self.can_show_cursor = True
            time.sleep(CONFIGS['cursor.blink_time'])
            self.can_show_cursor = False
            time.sleep(CONFIGS['cursor.blink_time'])

    def main_loop(self):
        """
        Starts the loop
        """
        self.enter()
        threading.Thread(target=self.key_press).start()
        threading.Thread(target=self.draw, daemon=True).start()
        threading.Thread(target=self.mouse, daemon=True).start()
