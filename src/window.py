"""Window"""
import sys
import time
import threading

import yachalk

from .settings import STYLES, CONFIGS, KEY_BINDINGS
from .menus import Strawberry, File, Edit
from .edit import TextEditor
from .extensions import extensions
from .consts import LEFT, RIGHT, UP, DOWN, ENTER
from .terminal import TerminalWindow

BLOCK_CURSOR = yachalk.chalk.bg_white_bright.black
UNDERLINE_CURSOR = yachalk.chalk.underline


class Window(TerminalWindow):
    """Window"""
    def __init__(self):
        self.input_keys = {}

        self.tabs = [TextEditor(self, 'unnamed', '')]
        self.current_tab = 0

        self.menus = [Strawberry(), File(), Edit()]
        self.current_menu = 0
        self.current_menu_item = 0

        self.on_tab = False
        self.is_menu_opened = False

        self.input_mode = True
        self.can_show_cursor = True

        self.extention_commands = {}

        self.t_keypress = None
        self.d_draw = None
        self.d_cursor = None

        self.can_redraw = True

    def enter(self):
        """Runs at start of program"""
        self.start_terminal()

        for i in extensions:
            self.extention_commands.update(i.commands)

    def exit(self):
        """Runs at end of program"""
        self.can_redraw = False
        self.show_cursor()
        self.clear_terminal()
        sys.exit()

    def toggle_input_mode(self):
        """Toggles between input mode"""
        self.input_mode = not self.input_mode

    def open_file(self, name, code):
        """Runs when changed file"""
        self.tabs.append(TextEditor(self, name, code))
        self.current_tab += 1

    def draw(self):
        """
        Draws the window
        """
        self.hide_cursor()
        while True:
            if self.can_redraw is False:
                break

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
            self.move_cursor(self.terminal_cols - len(CONFIGS['tab.end'])
                             - len(CONFIGS['selected_circle' if self.on_tab is
                                   True and self.input_mode is False else
                                   'unselected_circle']), 0)
            self.write(STYLES['tab.bg_color'](CONFIGS['selected_circle' if
                                              self.on_tab is False and
                                              self.input_mode is False else
                                              'unselected_circle']))
            self.write(STYLES['menu.end.unselected'](CONFIGS['menu.end']))

            self.move_cursor(0, self.terminal_lines - 1)
            self.write(STYLES['tab.bg_color'](' ' * self.terminal_cols))
            self.move_cursor(0, self.terminal_lines - 1)
            for tab_index, tabs in enumerate(self.tabs):
                if tab_index == 0:
                    self.write((STYLES['tab.start.selected'] if
                               self.current_tab == 0 else
                               STYLES['tab.start.unselected'])(CONFIGS
                                                               ['tab.start']))
                if tab_index == self.current_tab:
                    self.write(STYLES['tab.selected'](f' {tabs.name} '))
                else:
                    self.write(STYLES['tab.unselected'](f' {tabs.name} '))
            self.move_cursor(self.terminal_cols - len(CONFIGS['tab.end'])
                             - len(CONFIGS['selected_circle' if self.on_tab is
                                   True and self.input_mode is False else
                                   'unselected_circle']),
                             self.terminal_lines - 1)
            self.write(STYLES['tab.bg_color'](CONFIGS['selected_circle' if
                                              self.on_tab is True and
                                              self.input_mode is False else
                                              'unselected_circle']))
            self.write(STYLES['tab.end.unselected'](CONFIGS['tab.end']))

            current_tab = self.tabs[self.current_tab]
            editor_draw = current_tab.__draw__()
            cursor_pos = current_tab.__cursor__()['position']
            cursor_is_hidden = current_tab.__cursor__()['is_hidden']

            for line, i in enumerate(editor_draw.split('\n')):
                self.move_cursor(0, line + 1)
                self.write(i)

            if cursor_is_hidden is False:
                if self.can_show_cursor is True:
                    self.show_cursor()
                else:
                    self.hide_cursor()
                self.move_cursor(cursor_pos[0], cursor_pos[1] + 1)
            else:
                self.hide_cursor()

            if self.is_menu_opened is True:
                left = len(''.join([f' {i.name} ' for i in
                                    self.menus[:self.current_menu]])) + 2
                self.move_cursor(left, 1)
                items = self.menus[self.current_menu].list
                try:
                    max_len_items = len(max(items, key=len))
                    max_len_items = max(max_len_items, 10)
                except ValueError:
                    max_len_items = 0
                for enum, i in enumerate(items):
                    text = ' ' + i.ljust(max_len_items, ' ')
                    self.write(STYLES['menubox.unselected' if enum != self.
                               current_menu_item else 'menubox.selected']
                               (text))
                    self.move_cursor(left, 2 + enum)
                self.hide_cursor()

            self.flush()

    def execute_command(self, command):
        """Executes commands"""
        for i in command.split('-'):
            if i == 'exit':
                self.exit()
            elif i == 'toggle_input_mode':
                self.toggle_input_mode()
            elif i in self.extention_commands:
                self.extention_commands[i]()

    def key_press(self):
        """Handels keypresses"""
        while True:
            key = self.getch()
            self.can_show_cursor = True
            if key in KEY_BINDINGS:
                self.is_menu_opened = False
                self.execute_command(KEY_BINDINGS[key])
            elif (key in self.tabs[self.current_tab].keys and
                  self.input_mode is True):
                self.tabs[self.current_tab].keys[key]()
            elif self.input_mode is True:
                self.tabs[self.current_tab].keys[None](key)
            elif key == LEFT and self.input_mode is False:
                if self.current_tab > 0 and self.on_tab is True:
                    self.current_tab -= 1
                elif self.current_menu > 0 and self.on_tab is False:
                    self.current_menu -= 1
            elif key == RIGHT and self.input_mode is False:
                if self.current_tab < len(self.tabs) - 1 and (self.on_tab
                                                              is True):
                    self.current_tab += 1
                elif self.current_menu < len(self.menus) - 1 and (self.on_tab
                                                                  is False):
                    self.current_menu += 1
            elif (key == UP and self.on_tab is False and self.input_mode is
                  False and self.is_menu_opened is True):
                self.current_menu_item -= 1
            elif (key == DOWN and self.on_tab is False and
                  self.input_mode is False and self.is_menu_opened is True):
                self.current_menu_item += 1
            elif key == UP and self.input_mode is False:
                if self.on_tab is True:
                    self.on_tab = False
            elif key == DOWN and self.input_mode is False:
                if self.on_tab is False:
                    self.on_tab = True
            elif (key == ENTER and self.on_tab is False and self.input_mode is
                  False):
                if self.is_menu_opened is False:
                    self.is_menu_opened = True
                else:
                    (self.menus[self.current_menu].exec[self.current_menu_item]
                     (self))
            else:
                self.is_menu_opened = False

    def cursor(self):
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

        self.t_keypress = threading.Thread(target=self.key_press)
        self.d_draw = threading.Thread(target=self.draw, daemon=True)
        self.d_cursor = threading.Thread(target=self.cursor, daemon=True)

        self.t_keypress.start()
        self.d_draw.start()
        self.d_cursor.start()
