"""Syntax highlightling for python language"""
from pygments import highlight
from pygments.lexers.markup import MarkdownLexer
from pygments.lexers.python import Python3Lexer


class Extension():
    """Extension"""
    def __init__(self):
        self.commands = {'editor.highlight:py': self.highlighter_python,
                         'editor.highlight:md': self.highlighter_markdown}

    def highlighter_python(self, code, formatter):
        """Syntax Highlighter"""
        return highlight(code,
                         lexer=Python3Lexer(),
                         formatter=formatter)[:-1]

    def highlighter_markdown(self, code, formatter):
        """Syntax Highlighter"""
        return highlight(code,
                         lexer=MarkdownLexer(),
                         formatter=formatter)[:-1]
