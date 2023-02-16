"""Setting"""
from yachalk import chalk
from .consts import CTRL_Q, ESC

BOX = '┌┐─│└┘'

ICONS = {'module': '\uea8b ', 'class': '\ueb5b ',
         'instance': '\ueb63 ', 'function': '\uea8c ',
         'param': '\uea92 ', 'path': '\ueb60 ',
         'keyword': '\ueb62 ', 'property': '\ueb65 ',
         'statement': '\uea88 '}

CONFIGS = {'menu.start': ' \ue0ba', 'menu.end': '\ue0b8 ',
           'tab.start': ' \ue0be', 'tab.end': '\ue0bc ',
           'selected_circle': '\uea71 ', 'unselected_circle': '\ueabc ',
           'cursor.shape': 'u', 'editor.style': 'colorful',
           'editor.use_256_colors': False,
           'editor.line_number_rjust_lenth': 4,
           'editor.line_number_rjust_character': ' ',
           'cursor.blink_time': 0.5}
# cursor.shape can be 'b' for box or 'u' for underline
# editor.style can be any pygments style

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
          'completionbox.color': chalk.magenta}

KEY_BINDINGS = {CTRL_Q: 'exit', ESC: 'toggle_input_mode'}
