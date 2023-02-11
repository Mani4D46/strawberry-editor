"""Main Editor Class"""


class Editor():
    """Editors Base Class"""
    def __init_subclass__(cls):
        cls.keys = {None: cls.__event_keypress__}

    def __event_keypress__(self, key):
        pass

    def __update__(self):
        pass

    def __draw__(self):
        return ''
