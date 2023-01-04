from chafa import *
from chafa.loader import Loader
from PIL import Image as pImage
import numpy as np
from wand.image import Image as wImage
import pyvips

FILE = "../examples/snake.jpg"

MAX_RUNS = 1

config = CanvasConfig()

# Init the symbol map and add to config
symbols = SymbolMap()
symbols.add_by_tags(SymbolTags.CHAFA_SYMBOL_TAG_ALL)

config.set_symbol_map(symbols)

canvas_pil = Canvas(config)
canvas_vips = Canvas(config)
canvas_wand = Canvas(config)
canvas_loader = Canvas(config)


@profile
def chafa_pil():
    for _ in range(MAX_RUNS):
        # Open image with PIL
        image = pImage.open(FILE)

        width  = image.width
        height = image.height
        bands  = len(image.getbands())

        # Put image into correct format
        pixels = np.array(image)
        pixels = np.reshape(pixels, pixels.size)

        # Draw to canvas
        canvas_pil.draw_all_pixels(
            PixelType.CHAFA_PIXEL_RGB8,
            pixels,
            height,
            width,
            width * bands
        )


@profile
def chafa_vips():
    for _ in range(MAX_RUNS):
        # Open image with vips
        image = pyvips.Image.new_from_file(FILE)

        width  = image.width
        height = image.height
        bands  = image.bands

        # Draw to canvas
        canvas_vips.draw_all_pixels(
            PixelType.CHAFA_PIXEL_RGB8,
            image.write_to_memory(),
            width,
            height,
            width * bands
        )


@profile
def chafa_loader():
    for _ in range(MAX_RUNS):
        # Open image with vips
        image = Loader(FILE)

        width      = image.width
        height     = image.height
        rowstride  = image.rowstride

        # Draw to canvas
        canvas_loader.draw_all_pixels(
            image.pixel_type,
            image.get_pixels(),
            width, 
            height,
            rowstride
        )


@profile
def chafa_wand():
    for _ in range(MAX_RUNS):
        # Open image with wand
        with wImage(filename=FILE) as image:

            width  = image.width
            height = image.height
            bands  = 4

            pixels = image.export_pixels(storage='char')

        # Draw to canvas
        canvas_wand.draw_all_pixels(
            PixelType.CHAFA_PIXEL_RGBA8_UNASSOCIATED,
            pixels,
            height,
            width,
            width * bands
        )

chafa_loader()
chafa_wand()
chafa_pil()
chafa_vips()
