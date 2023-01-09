from chafa import *
from chafa.loader import Loader

import sys

img_loc     = sys.argv[-2]
output_loc  = sys.argv[-1]

def format_pixel(char, fg, bg):
    style       = f"color: rgb{fg}; background-color: rgb{bg}"
    opening_tag = f"<span class=\"pixel\" style=\"{style}\">"
    closing_tag = f"</span>"

    return f"{opening_tag}{char}{closing_tag}"

FONT_RATIO = 11/24

config = CanvasConfig()

config.width  = 40
config.height = 40

image = Loader("./snake.jpg")

config.calc_canvas_geometry(image.width, image.height, FONT_RATIO)

canvas = Canvas(config)


canvas.draw_all_pixels(
    image.pixel_type,
    image.get_pixels(),
    image.width, image.height,
    image.rowstride
)

with open(output_loc, "w") as f:
    f.write("<div class=\"chafa-img\">\n")

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
