import pyvips
from chafa import *

# Init canvas config
config = CanvasConfig()

# Set canvas height and width
config.height = 30
config.width  = 30

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
print(canvas.print().decode())