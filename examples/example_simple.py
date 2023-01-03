from chafa import *
from chafa.loader import Loader

# Init canvas config
config = CanvasConfig()

# Set canvas height, width and cell geometry
config.height = 30
config.width  = 30

# Init the symbol map and add to config
symbols = SymbolMap()
symbols.add_by_tags(SymbolTags.CHAFA_SYMBOL_TAG_ALL)

config.set_symbol_map(symbols)

# Open image with vips
image = Loader("./snake.jpg")

width      = image.width
height     = image.height
rowstride  = image.rowstride

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
