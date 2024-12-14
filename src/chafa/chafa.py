from __future__ import annotations
import sys
import platform
from io import UnsupportedOperation

SYSTEM = platform.system()

if SYSTEM == "Linux" or SYSTEM == "Darwin":
    import termios

def _read_escape_sequence(escape_code, terminator, sep=";"):
    if SYSTEM != "Linux" and SYSTEM != "Darwin":
        return tuple()

    try:
        stdin_fileno = sys.stdin.fileno()

    except UnsupportedOperation:
        return tuple()

    # Set up
    old_term = termios.tcgetattr(stdin_fileno)
    new_term = termios.tcgetattr(stdin_fileno)

    # disable canonical mode and disable echo input
    new_lflags  = ~(termios.ICANON | termios.ECHO) 
    new_term[3] = new_lflags

    # Emit sequence
    sys.stdout.write(escape_code)
    sys.stdout.flush()
    
    termios.tcsetattr(stdin_fileno, termios.TCSANOW, new_term)

    # Read the sequence
    char = sys.stdin.read(1)
    attributes = []

    while char != terminator:
        attributes.append(char)
        char = sys.stdin.read(1)

    # Set terminal back to normal
    termios.tcsetattr(stdin_fileno, termios.TCSANOW, old_term)

    # Split attributes by ; and turn them into integers
    if len(attributes) >= 4:
        attributes = "".join(attributes[3:]).split(sep)

        # Convert all attributes to ints unless we can't, then we skip
        out = []
        for attrib in attributes:
            try:
                out.append(int(attrib))
            except ValueError:
                continue

        out = tuple(out)

    else:
        out = tuple()

    return out

def get_device_attributes():
    """
    A function that returns an array containing the current
    terminal's device attributes, fetched by reading the string
    provided by emitting the ``\\e[c`` control sequence. (See
    `Xterm Control Sequences on invisible-island.net 
    <https://invisible-island.net/xterm/ctlseqs/ctlseqs.html>_`.

    .. note::
        Returns an empty tuple on Windows

    :rtype: Tuple[int]
    """

    return _read_escape_sequence("\033[c", "c")


def get_terminal_geometry():
    """
    A function that returns the size of the terminal text area in character cells. 
    Format: ``(height, width)``.

    .. note::
        Returns an empty tuple on Windows

    :rtype: Tuple[int]
    """
    return _read_escape_sequence("\033[18t", "t")


def get_terminal_pixel_geometry():
    """
    A function that returns the size of the terminal text area in pixels.
    Foramt: ``(height, width)``

    .. note::
        Returns an empty tuple on Windows

    :rtype: Tuple[int]
    """

    return _read_escape_sequence("\033[14t", "t")


def get_cell_geometry():
    """
    A function that returns the cell geometry of the terminal in pixels. This is achieved by simply
    dividing the terminal's reported pixel size by its reported size in characters.
    Format: ``(height, width)``.

    .. note::
        Returns an empty tuple on Windows

    :rtype: Tuple[int]
    """
    pixel_height, pixel_width = get_terminal_pixel_geometry()
    character_height, character_width = get_terminal_geometry()

    return (pixel_height//character_height, pixel_width//character_width)