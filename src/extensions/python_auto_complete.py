"""Auto complete for python language"""
import jedi


class Extention():
    """Extention"""
    def __init__(self):
        self.commands = {'editor.auto_complete:py': self.auto_complete}
        self.auto_complete_file_extentions = ['.py']

    def auto_complete(self, code, col, line):
        """Python auto complete"""
        if code != '' and code.split('\n')[line] != '':
            script = jedi.Script(code, path='')
            try:
                return script.complete(line + 1, col)
            except AttributeError:
                return []
        return []
