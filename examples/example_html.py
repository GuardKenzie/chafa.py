from chafa import *
from chafa.loader import Loader

img_loc     = "snake.jpg"
output_loc  = "out.html"

def format_pixel(char, fg, bg):
    # Formats the pixel to html with color applied through style
    style       = f"color: rgb{fg}; background-color: rgb{bg}"
    opening_tag = f"<span class=\"pixel\" style=\"{style}\">"
    closing_tag = f"</span>"

    return f"{opening_tag}{char}{closing_tag}"

# Font ratio of JetBrains Mono
FONT_RATIO = 11/24

# Init config
config = CanvasConfig()

config.width  = 40
config.height = 40

# Load image
image = Loader(img_loc)

# Set up canvas
config.calc_canvas_geometry(image.width, image.height, FONT_RATIO)

canvas = Canvas(config)
canvas.draw_all_pixels(
    image.pixel_type,
    image.get_pixels(),
    image.width, image.height,
    image.rowstride
)

# Write the file
with open(output_loc, "w") as f:
    f.write("<div class=\"chafa-img\">\n")

    # Iterate over pixels in image
    for row in canvas[:]:
        f.write("    <p class=\"row\">\n")
        f.write("        ")
        for pixel in row:
            f.write(
                format_pixel(
                    pixel.char,
                    pixel.fg_color,
                    pixel.bg_color
                )
            )

        f.write("\n    </p>\n")

    f.write("</div class=\"chafa-img\">")