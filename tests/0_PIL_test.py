from chafa import *
from PIL import Image
import numpy as np
from pathlib import Path

def test_PIL():
    # Init canvas config
    config = CanvasConfig()

    # Set canvas height and width
    config.height = 30
    config.width  = 30

    # Open image with PIL
    image = Image.open(Path(__file__).parent / "snake.jpg")

    width  = image.width
    height = image.height
    bands  = len(image.getbands())

    # Put image into correct format
    pixels = np.array(image)
    pixels = np.reshape(pixels, pixels.size)

    # Init the canvas
    canvas = Canvas(config)

    # Draw to canvas
    canvas.draw_all_pixels(
        PixelType.CHAFA_PIXEL_RGB8,
        pixels,
        height,
        width,
        width * bands
    )

    # Write picture
    print(canvas.print().decode())