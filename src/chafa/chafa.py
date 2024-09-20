from __future__ import annotations
import sys
import platform
from io import UnsupportedOperation

if platform.system() == "Linux":
    import termios


def get_device_attributes():
    """
    A functino that returns an array containing the current
    terminal's device attributes, fetched by reading the string
    provided by emitting the ``\\e[c`` control sequence. (See
    `Xterm Control Sequences on invisible-island.net 
    <https://invisible-island.net/xterm/ctlseqs/ctlseqs.html>_`.

    :rtype: Tuple[int]
    """
    
    if platform.system() != "Linux":
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
    sys.stdout.write("\033[c")
    sys.stdout.flush()
    
    termios.tcsetattr(stdin_fileno, termios.TCSANOW, new_term)

    # Read the sequence
    char = sys.stdin.read(1)
    attributes = []

    while char != "c":
        attributes.append(char)
        char = sys.stdin.read(1)

    # Set terminal back to normal
    termios.tcsetattr(stdin_fileno, termios.TCSANOW, old_term)

    # Split attributes by ; and turn them into integers
    if len(attributes) >= 4:
        attributes = "".join(attributes[3:]).split(";")

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

