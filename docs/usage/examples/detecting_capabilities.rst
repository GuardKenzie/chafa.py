===============================
Detecting terminal capabilities
===============================

Here is an example of a program that uses :py:meth:`TermInfo.detect_capabilities()` to figure out what the current terminal is capable of.

::

    from chafa import *
    from chafa.loader import Loader

    # Init canvas config
    config = CanvasConfig()

    # Set canvas height and width
    config.height = 30
    config.width  = 30

    # Init database and get terminal info
    term_db   = TermDb()
    term_info = term_db.detect()

    # Get terminal capabilities
    capabilities = term_info.detect_capabilities()

    # Set config to appropriate modes
    config.canvas_mode = capabilities.canvas_mode
    config.pixel_mode  = capabilities.pixel_mode

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


.. _`MagickWand`: https://imagemagick.org/script/magick-wand.php
.. _`Pillow`: https://python-pillow.org/
.. _`pyvips`: https://github.com/libvips/pyvips
.. _`GitHub repo`: https://github.com/guardkenzie/chafa.py
.. _`JetBrains Mono`: https://www.jetbrains.com/lp/mono/
.. _`index`: https://chafapy.mage.black
