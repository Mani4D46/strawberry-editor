"""Setting"""
from yachalk import chalk

BOX = '┏┓━┃┗┛'

ICONS = {'module': '\uea8b ', 'class': '\ueb5b ',
         'instance': '\ueb63 ', 'function': '\uea8c ',
         'param': '\uea92 ', 'path': '\ueb60 ',
         'keyword': '\ueb62 ', 'property': '\ueb65 ',
         'statement': '\uea88 '}

CONFIGS = {'menu.start': ' \ue0ba', 'menu.end': '\ue0bc ',
           'cursor.shape': 'b', 'theme': 'monokai'}
# cursor.shape can be 'b' for box or 'u' for underline
# theme can be any pygments style

STYLES = {'menu.unselected': chalk.bg_gray,
          'menu.start.selected': chalk.red,
          'menu.start.unselected': chalk.gray,
          'menu.end.unselected': chalk.gray,
          'menu.selected': chalk.bg_red,
          'menu.bg_color': chalk.bg_gray,
          'completionbox.color': chalk.bg_gray.white}
