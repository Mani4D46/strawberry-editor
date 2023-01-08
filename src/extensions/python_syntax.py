"""Syntax highlightling for python language"""
from pygments import highlight
from pygments.lexers import get_lexer_by_name

TYPE = 'Highlighter'
FILE_TYPES = ['py']


def highlighter(code, formatter):
    """Syntax Highlighter"""
    return highlight(code,
                     lexer=get_lexer_by_name("python"),
                     formatter=formatter)
