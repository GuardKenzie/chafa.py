import pyvips
from chafa import *

FONT_WIDTH  = 11
FONT_HEIGHT = 24

# Init canvas config
config = CanvasConfig()

# Set canvas height, width and cell geometry
config.height = 30 
config.width  = 30

config.cell_width  = FONT_WIDTH
config.cell_height = FONT_HEIGHT

# Init the symbol map and add to config
symbols = SymbolMap()
symbols.add_by_tags(SymbolTags.CHAFA_SYMBOL_TAG_ALL)

config.set_symbol_map(symbols)

# Init the terminal info and find out the capabilities
term_db = TermDb()
term_info = term_db.detect()

term_capabilities = term_info.detect_capabilities()

# Set the config to the relevant pixel and canvas mode
config.pixel_mode  = term_capabilities.pixel_mode
config.canvas_mode = term_capabilities.canvas_mode

# Open image with vips
image = pyvips.Image.new_from_file("/tmp/aartminip.png")

width  = image.width
height = image.height
bands  = image.bands

# Calculate the correct geometry based on image size and font ratio
config.calc_canvas_geometry(width, height, FONT_WIDTH/FONT_HEIGHT)

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
