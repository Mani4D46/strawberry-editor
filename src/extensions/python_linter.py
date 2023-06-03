"""Linter for python language"""
import ast
from .constants import SYNTAX_ERROR


class Extension():
    """Extension"""
    def __init__(self):
        self.commands = {'editor.linter:py': self.linter}

    def linter(self, code):
        """Python linter"""
        errors = []
        try:
            ast.parse(code)
        except (SyntaxError, IndentationError) as exception:
            errors.append((exception.lineno, *SYNTAX_ERROR,
                           exception.args[0], exception.offset))
        return errors
