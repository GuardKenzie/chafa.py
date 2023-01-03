import sys
from chafa import *
from PIL import Image
from array import array
import numpy as np

FONT_WIDTH  = 11
FONT_HEIGHT = 24

# Init canvas config
config = CanvasConfig()

# Set canvas height, width and cell geometry
config.height = 40
config.width  = 40

# Init the symbol map and add to config
symbols = SymbolMap()
symbols.add_by_tags(SymbolTags.CHAFA_SYMBOL_TAG_ALL)

config.set_symbol_map(symbols)

# Open image with PIL
image = Image.open("./snake.jpg")

width  = image.width
height = image.height
bands  = len(image.getbands())

# Put image into correct format
pixels = np.array(image)
pixels = np.reshape(pixels, pixels.size)

# Calculate canvas size
config.calc_canvas_geometry(width, height, FONT_WIDTH/FONT_HEIGHT)

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
