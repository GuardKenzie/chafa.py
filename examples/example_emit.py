from chafa import *
from time import sleep
import sys

SL=15

def snake(n, step):
    if step < 0: turns = ["┏","┛"]
    else:        turns = ["┓", "┗"]

    if n == 1:
        return turns[0]
    elif n == SL - 1:
        return turns[1]

    return "┃"

def gradient(x, y):
    return (80 + 5*x, 255 - (100 + 10*y), 200)

# Grab our info
db = TermDb()
info = db.detect()

# Clear the terminal
clear     = info.emit(TermSeq.CHAFA_TERM_SEQ_CLEAR)
no_cursor = info.emit(TermSeq.CHAFA_TERM_SEQ_DISABLE_CURSOR)

print(clear.decode())
print(no_cursor.decode())

rows = list(range(1,SL))
cols = list(range(1,32))

for x in cols:
    # We want to step backwards if column is even
    step = 2 * (x%2) - 1

    for y in rows[::step]:
        # Grab char
        char = snake(y, step)

        # Move to position
        out = info.emit(
            TermSeq.CHAFA_TERM_SEQ_CURSOR_TO_POS, 
            x, y
        )

        # Set color
        color = info.emit(
            TermSeq.CHAFA_TERM_SEQ_SET_COLOR_FG_DIRECT,
            *gradient(x,y)
        )

        sys.stdout.buffer.write(out)
        sys.stdout.buffer.write(color)
        sys.stdout.write(char)
        sys.stdout.flush()

        sleep(0.01)

# All back to normal!
reset = info.emit(TermSeq.CHAFA_TERM_SEQ_RESET_TERMINAL_HARD)
print(reset.decode())
