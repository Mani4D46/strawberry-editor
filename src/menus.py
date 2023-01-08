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
    list = ['open', 'save', 'save as']

    def __init__(self):
        self.exec = [self.open, self.save, self.save_as]

    def open(self, window):
        """Opens an file"""
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename()
        with open(file_path, 'r', encoding='utf8') as file:
            window.file_open(file_path, file.read())

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
        window.file_open(file_path)
        self.save(window)


class Edit():
    """Edit menu"""
    name = 'Edit'
    list = ['t']
    exec = [lambda window: None]
