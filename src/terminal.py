"""Terminal"""
import sys
import os

try:
    from msvcrt import getch as msvcrt_getch

    def getch():
        """
        Gets a single character from STDIO.
        """
        return msvcrt_getch().decode('utf8')
except ImportError:
    def getch():
        """
        Gets a single character from STDIO.
        """
        import tty
        import termios
        file_no = sys.stdin.fileno()
        old = termios.tcgetattr(file_no)
        try:
            tty.setraw(file_no)
            return sys.stdin.read(1)
        finally:
            termios.tcsetattr(file_no, termios.TCSADRAIN, old)


CSI = '\033['


class TerminalWindow():
    """
    Window class
    """
    def __init_subclass__(cls):
        cls.is_os_windows = sys.platform.startswith("win")

        cls.terminal_lines = os.get_terminal_size().lines
        cls.terminal_cols = os.get_terminal_size().columns

        cls.write = sys.stdout.write
        cls.flush = sys.stdout.flush

    def start_terminal(self):
        """Runs at Start of terminal or when clearing"""
        sys.stdout.write(' ' * self.terminal_cols * self.terminal_lines)

    def getch(self):
        """Gets a key from STDIO"""
        char1 = getch()
        if char1 not in '\x00\xe0' + ('\x1b' if self.is_os_windows is False
                                      else ''):
            return char1
        char2 = getch()
        if char2 not in '\x5b' + ('\x4f' if self.is_os_windows is False
                                  else ''):
            if char1 == '\xe0':
                return '\x00' + char2
            return char1 + char2
        char3 = getch()
        if char3 not in '\x31\x32\x33\x35\x36':
            return char1 + char2 + char3
        char4 = getch()
        if char4 not in '\x30\x31\x33\x34\x35\x37\x38\x39':
            return char1 + char2 + char3 + char4
        char5 = getch()
        return char1 + char2 + char3 + char4 + char5

    def clear_terminal(self):
        """
        Clears Terminal
        """
        self.move_cursor(0, 0)
        self.start_terminal()
        self.move_cursor(0, 0)

    def move_cursor(self, left, top):
        """
        Moves cursor's position
        """
        sys.stdout.write(f'{CSI}{top + 1};{left + 1}H')

    def hide_cursor(self):
        """
        Hides cursor
        """
        sys.stdout.write(f'{CSI}?25l')

    def show_cursor(self):
        """
        Hides cursor
        """
        sys.stdout.write(f'{CSI}?25h')
