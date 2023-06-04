"""Menus"""
import tkinter as tk
from tkinter import filedialog


class Strawberry():
    """Strawberry menu"""
    name = 'Strawberry'
    list = []


class File():
    """File menu"""
    name = 'File'
    list = ['Open     Ctrl + o',
            'New      Ctrl + n',
            'Save     Ctrl + s',
            'Save As  Ctrl + S']

    def __init__(self):
        self.exec = [self.open, self.new, self.save, self.save_as]

    def open(self, window):
        """Opens an file"""
        window.open_file()

    def new(self, window):
        window.new_file()

    def save(self, window):
        """Save an file"""
        with open(window.file_name, 'w', encoding='utf8') as file:
            code = '\n'.join([''.join(i) for i in window.input])
            file.write(code)

    def save_as(self, window):
        """Saves an file as ..."""
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.asksaveasfilename()
        window.open_file(file_path)
        self.save(window)


class Edit():
    """Edit menu"""
    name = 'Edit'
    list = ['Undo     Ctrl + z',
            'Redo     Ctrl + y',
            'Paste    Ctrl + v']
    exec = [lambda _: None for i in range(3)]
