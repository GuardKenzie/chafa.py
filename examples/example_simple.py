from chafa import *
from chafa.loader import Loader

# Init canvas config
config = CanvasConfig()

# Set canvas height and width
config.height = 30
config.width  = 30

# Open image with the loader
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