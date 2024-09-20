=====================
Accurate aspect ratio
=====================

Here is an example that outputs the image in the correct aspect ratio.

::

    from chafa import *
    from chafa.loader import Loader

    FONT_WIDTH  = 11
    FONT_HEIGHT = 24

    # Init canvas config
    config = CanvasConfig()

    # Set canvas height, width and cell geometry
    config.height = 30
    config.width  = 30

    # Set the canvas cell geometry
    config.cell_height = FONT_HEIGHT
    config.cell_width  = FONT_WIDTH

    # Open image with the loader
    image = Loader("./snake.jpg")

    width      = image.width
    height     = image.height
    rowstride  = image.rowstride

    # Calculate the appropriate geometry for the canvas
    config.calc_canvas_geometry(width, height, FONT_WIDTH/FONT_HEIGHT)

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


.. _`MagickWand`: https://imagemagick.org/script/magick-wand.php
.. _`Pillow`: https://python-pillow.org/
.. _`pyvips`: https://github.com/libvips/pyvips
.. _`GitHub repo`: https://github.com/guardkenzie/chafa.py
.. _`JetBrains Mono`: https://www.jetbrains.com/lp/mono/
.. _`index`: https://chafapy.mage.black
