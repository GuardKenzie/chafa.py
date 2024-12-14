import chafa
from PIL import Image
from pathlib import Path
import time

DIR = Path(__file__).parent

frames = []

# We extract all the frames from the gif and wrap them in chafa.Frame objects
with Image.open(DIR / "frieren.gif") as animation:
    animation.seek(0)

    total_frames = animation.n_frames
    
    width     = animation.width
    height    = animation.height
    rowstride = width * 3          # We convert each frame to an RGB image so we will have 3 bands

    for k in range(total_frames):
        animation.seek(k)
        duration = animation.info['duration'] / 1000

        chafa_frame = chafa.Frame(
            chafa.PixelType.CHAFA_PIXEL_RGB8,
            animation.convert("RGB").tobytes(),
            width, height, rowstride
        )
        
        frames.append((chafa_frame, duration))

# Init config
config = chafa.CanvasConfig()

config.canvas_mode = chafa.CanvasMode.CHAFA_CANVAS_MODE_TRUECOLOR
config.pixel_mode  = chafa.PixelMode.CHAFA_PIXEL_MODE_SYMBOLS

config.width  = 80
config.height = 80

config.cell_height, config.cell_width = chafa.get_cell_geometry()

config.calc_canvas_geometry(width, height, config.cell_width/config.cell_height)

# Init canvas
canvas = chafa.Canvas(config)

image = chafa.Image()

# Pick out some escape sequences
term_db   = chafa.TermDb()
term_info = term_db.detect()

clear      = term_info.emit(chafa.TermSeq.CHAFA_TERM_SEQ_CLEAR).decode()
no_cursor  = term_info.emit(chafa.TermSeq.CHAFA_TERM_SEQ_DISABLE_CURSOR).decode()
yes_cursor = term_info.emit(chafa.TermSeq.CHAFA_TERM_SEQ_ENABLE_CURSOR).decode()
move       = term_info.emit(chafa.TermSeq.CHAFA_TERM_SEQ_CURSOR_LEFT, config.width).decode() \
           + term_info.emit(chafa.TermSeq.CHAFA_TERM_SEQ_CURSOR_UP, config.height-1).decode()

no_echo    = term_info.emit(chafa.TermSeq.CHAFA_TERM_SEQ_DISABLE_ECHO).decode()
yes_echo   = term_info.emit(chafa.TermSeq.CHAFA_TERM_SEQ_ENABLE_ECHO).decode()

def play():
    print(no_cursor, no_echo, end="")

    k = 0
    first_frame = True
    while True:
        s = time.perf_counter()

        # Update placement
        image.frame, duration = frames[k]
        placement = chafa.Placement(image)
        canvas.placement = placement

        # Move up to overwrite
        if not first_frame:
            print(move, end="")

        print(canvas.print().decode(), end="")

        e = time.perf_counter()

        # Calculate how long it took to draw and wait the appropriate duration
        elapsed = e-s
        time.sleep(max(0, duration - elapsed))

        k = (k + 1) % total_frames
        first_frame = False

def cleanup():
    print(yes_cursor, yes_echo)

try:
    play()
except KeyboardInterrupt:
    cleanup()