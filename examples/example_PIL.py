from chafa import *
from PIL import Image

# Init canvas config
config = CanvasConfig()

# Set canvas height and width
config.height = 30
config.width  = 30

# Open image with PIL
image = Image.open("./snake.jpg")

width  = image.width
height = image.height
bands  = len(image.getbands())

# Put image into correct format
pixels = image.tobytes()

# Init the canvas
canvas = Canvas(config)

# Draw to canvas
canvas.draw_all_pixels(
    PixelType.CHAFA_PIXEL_RGB8,
    pixels,
    width,
    height,
    width * bands
)

# Write picture
print(canvas.print().decode())
