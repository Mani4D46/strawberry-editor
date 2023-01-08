"""Auto complete for python language"""
import jedi

TYPE = 'AutoComplete'
FILE_TYPES = ['py']


def auto_complete(code, col, line):
    """Python auto complete"""
    if code != '' and code.split('\n')[line] != '':
        script = jedi.Script(code, path='')
        try:
            return script.complete(line + 1, col)
        except AttributeError:
            return []
    return []
