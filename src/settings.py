"""Setting"""
from yachalk import chalk
from .consts import (
    # Global
    CTRL_Q, ESC,
    # File System
    CTRL_N, CTRL_O,
    # Text Editor
    CTRL_L, F4, END, HOME, LEFT, RIGHT, UP, DOWN, CTRL_V, CTRL_BACKSPACE
)

BOX = '┌┐─│└┘'

FILE_ICONS = {'py': 'python', 'js': 'javascript'}

ICONS = {'module': '\uea8b ', 'class': '\ueb5b ',
         'instance': '\ueb63 ', 'function': '\uea8c ',
         'param': '\uea92 ', 'path': '\ueb60 ',
         'keyword': '\ueb62 ', 'property': '\ueb65 ',
         'statement': '\uea88 ', 'error': '\uea87 ',
         'warning': '\uea6c ', 'info': '\uea74 ',
         'folder': '\uea83 ', 'file': '\uea7b ',
         'python': '\ue235 ', 'javascript': '\ue781 ',
         'home': '\ueb06 '}

CONFIGS = {'menu.start': ' \ue0ba ', 'menu.end': '\ue0b8 ',
           'tab.start': ' \ue0be ', 'tab.end': '\ue0bc ',
           'selected_circle': '\uea71 ', 'unselected_circle': '\ueabc ',
           'cursor.shape': 'u', 'editor.style': 'colorful',
           'editor.use_256_colors': False,
           'editor.line_number_rjust_lenth': 6,
           'editor.line_number_rjust_character': ' ',
           'cursor.blink_time': 0.5,
           'CSI2J_reload_mode': False,
           'default_encoding': 'utf8'}

# CSI2J_reload_mode may make the screen blink

STYLES = {'menu.unselected': chalk.bg_gray,
          'menu.start.selected': chalk.red,
          'menu.start.unselected': chalk.gray,
          'menu.end.unselected': chalk.gray,
          'menu.selected': chalk.bg_red,
          'menu.bg_color': chalk.bg_gray,
          'tab.unselected': chalk.bg_gray,
          'tab.start.selected': chalk.blue,
          'tab.start.unselected': chalk.gray,
          'tab.end.unselected': chalk.gray,
          'tab.selected': chalk.bg_blue.black,
          'tab.bg_color': chalk.bg_gray,
          'menubox.unselected': chalk.red.bg_gray,
          'menubox.selected': chalk.bg_red.gray,
          'completionbox.color': chalk.magenta.bg_black_bright,
          'editor.lines.selected': chalk.blue,
          'editor.lines.error': chalk.red,
          'editor.lines.warning': chalk.yellow,
          'editor.lines.info': chalk.cyan,
          'home_page.selected': chalk.magenta_bright,
          'explorer_page.selected': chalk.magenta_bright,
          'selected_text': chalk.bg_blue}

KEY_BINDINGS = {CTRL_Q: 'exit', ESC: 'toggle_input_mode',
                CTRL_N: 'new_file', CTRL_O: 'open_file'}

EDITOR_KEY_BINDINGS = {'toggle_select_mode': CTRL_L,
                       'toggle_auto_completion': F4,
                       'paste': CTRL_V,
                       'beginning_of_line': HOME,
                       'end_of_line': END,
                       'left': LEFT,
                       'right': RIGHT,
                       'up': UP,
                       'down': DOWN,
                       'remove_word': CTRL_BACKSPACE}
