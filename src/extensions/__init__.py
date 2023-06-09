"""Extensions"""
from . import (
    default_syntaxes,
    python_auto_complete,
    home_page,
    explorer_page,
    python_linter,
)

extensions = [python_auto_complete.Extension(), default_syntaxes.Extension(),
              home_page.Extension(), python_linter.Extension(),
              explorer_page.Extension()]
