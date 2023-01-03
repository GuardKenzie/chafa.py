from chafa import *
from wand.image import Image

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

# Open image with wand
with Image(filename="./snake.jpg") as image:

    width  = image.width
    height = image.height
    bands  = 4

    pixels = image.export_pixels(storage='char')

# Calculate canvas size
config.calc_canvas_geometry(width, height, FONT_WIDTH/FONT_HEIGHT)

# Init the canvas
canvas = Canvas(config)

# Draw to canvas
canvas.draw_all_pixels(
    PixelType.CHAFA_PIXEL_RGBA8_UNASSOCIATED,
    pixels,
    height,
    width,
    width * bands
)

# Write picture
print(canvas.print().decode())
