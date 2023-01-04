"""Auto complete for python language"""
import jedi

TYPE = 'AutoComplete'
FILE_TYPES = ['py', '<None>']


def auto_complete(code, col, line):
    """Python auto complete"""
    if code != '' and code.split('\n')[line] != '':
        script = jedi.Script(code, path='')
        return script.complete(line + 1, col)
    return []
