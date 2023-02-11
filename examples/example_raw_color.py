from chafa import *

# Create config
config = CanvasConfig()

config.width = 36
config.height = (256 - (16+24))  // 36 + 2


config.canvas_mode = CanvasMode.CHAFA_CANVAS_MODE_INDEXED_256

# Init an empty canvas
pixels = [0, 0, 0, 0]

canvas = Canvas(config)
canvas.draw_all_pixels(
    PixelType.CHAFA_PIXEL_RGBA8_PREMULTIPLIED,
    pixels,
    1, 1, 3
)

# Draw all 256 colors

# Set the characters to half blocks
for row in canvas[:]:
    for pix in row:
        pix.char = "▀"
        pix.remove_foreground()


# Draw the primary 16
for pix in canvas[0,:16]:
    pix.raw_fg_color = pix.x

# Draw the rest of the colors
for row in canvas[1:-1, :]:
    for pix in row:
        pix.raw_fg_color = pix.x + 16 + ((pix.y-1) * 5 * config.width//5)

# Draw the greyscale gradient
for pix in canvas[-1, :24]:
    pix.raw_fg_color = 255 - (23 - pix.x)

print(canvas.print().decode())