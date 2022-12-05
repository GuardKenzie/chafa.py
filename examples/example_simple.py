import pyvips
from chafa import *

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
image = pyvips.Image.new_from_file("./snake.jpg")

width  = image.width
height = image.height
bands  = image.bands

# Init the canvas
canvas = Canvas(config, term_info=term_info)

# Draw to canvas
canvas.draw_all_pixels(
    PixelType.CHAFA_PIXEL_RGB8,
    image.write_to_memory(),
    width,
    height,
    width * bands
)

# Write picture
sys.stdout.buffer.write(canvas.print())
sys.stdout.flush()
