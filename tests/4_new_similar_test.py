from chafa import *
from PIL import Image
from pathlib import Path

def test_PIL():
    # Init canvas config
    config = CanvasConfig()

    # Set canvas height and width
    config.height = 10
    config.width  = 10

    # Open image with PIL
    image = Image.open(Path(__file__).parent / "snake.jpg")

    width  = image.width
    height = image.height
    bands  = len(image.getbands())

    # Put image into correct format
    pixels = image.tobytes()

    # Init the canvas and copy it
    canvas = Canvas(config)

    config.width = 50

    canvas2 = canvas.new_similar()

    # Draw to canvases
    canvas.draw_all_pixels(
        PixelType.CHAFA_PIXEL_RGB8,
        pixels,
        height,
        width,
        width * bands
    )

    canvas2.draw_all_pixels(
        PixelType.CHAFA_PIXEL_RGB8,
        pixels,
        height,
        width,
        width * bands
    )

    for pixel in canvas2[:,0]:
        pixel.bg_color = (255, 0, 0)
        pixel.char     = "ð"

    # Write picture
    print("Original canvas")
    print(canvas.print().decode())
    print("Copied canvas")
    print(canvas2.print().decode())
