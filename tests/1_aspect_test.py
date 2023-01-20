from chafa import *
from chafa.loader import Loader

from pathlib import Path

FONT_WIDTH  = 11
FONT_HEIGHT = 24

import platform

def test_aspect():
    # Init canvas config
    config = CanvasConfig()

    # Set canvas height, width and cell geometry
    config.height = 30
    config.width  = 30

    # Set the canvas cell geometry
    config.cell_height = FONT_HEIGHT
    config.cell_width  = FONT_WIDTH

    # Open image with the loader
    image = Loader(Path(__file__).parent / "snake.jpg")

    width      = image.width
    height     = image.height
    rowstride  = image.rowstride

    # Calculate the appropriate geometry for the canvas
    config.calc_canvas_geometry(width, height, FONT_WIDTH/FONT_HEIGHT)

    # Init the canvas
    canvas = Canvas(config)

    # Draw to canvas
    canvas.draw_all_pixels(
        image.pixel_type,
        image.get_pixels(),
        width,
        height,
        rowstride
    )

    # Write picture
    print(canvas.print().decode())