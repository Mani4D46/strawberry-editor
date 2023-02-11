"""Setting"""
from yachalk import chalk
from .consts import CTRL_Q, ESC

BOX = '┌┐─│└┘'

ICONS = {'module': '\uea8b ', 'class': '\ueb5b ',
         'instance': '\ueb63 ', 'function': '\uea8c ',
         'param': '\uea92 ', 'path': '\ueb60 ',
         'keyword': '\ueb62 ', 'property': '\ueb65 ',
         'statement': '\uea88 '}

CONFIGS = {'menu.start': ' \ue0ba', 'menu.end': '\ue0bc ',
           'cursor.shape': 'u', 'theme': 'monokai',
           'editor.line_number_rjust_lenth': 4,
           'editor.line_number_rjust_character': ' ',
           'cursor.blink_time': 1}
# cursor.shape can be 'b' for box or 'u' for underline
# theme can be any pygments style

STYLES = {'menu.unselected': chalk.bg_gray,
          'menu.start.selected': chalk.red,
          'menu.start.unselected': chalk.gray,
          'menu.end.unselected': chalk.gray,
          'menu.selected': chalk.bg_red,
          'menu.bg_color': chalk.bg_gray,
          'menubox.color': chalk.magenta,
          'completionbox.color': chalk.magenta}

KEY_BINDINGS = {CTRL_Q: 'exit', ESC: 'toggle_input_mode'}
