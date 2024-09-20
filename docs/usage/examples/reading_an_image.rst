================
Reading an image
================

Here are several different methods of reading images for using them with chafa.py. They perform similarly so just pick the one you like the most!

.. py:currentmodule:: chafa.loader

Using :py:class:`Loader`
------------------------

The :py:class:`Loader` is a class included with chafa.py which aims making it easy to read and draw images to the :py:class:`chafa.Canvas`, however, it does depend on the `MagickWand`_ C-library.

::

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


.. _pillow-example:

Using `Pillow`_
---------------

When reading pixel data from an image opened with `Pillow`_, we get a 2D array which needs to be reshaped into a 1D array before passing to chafa. This is still pretty fast since both Pillow and NumPy are well optimized.

::

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


Using `pyvips`_
---------------

The `pyvips`_ library is another fast image manipulation library which can be used to read images in a pretty straight forward manner.

::

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
    canvas = Canvas(config)

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


.. _`MagickWand`: https://imagemagick.org/script/magick-wand.php
.. _`Pillow`: https://python-pillow.org/
.. _`pyvips`: https://github.com/libvips/pyvips
.. _`GitHub repo`: https://github.com/guardkenzie/chafa.py
.. _`JetBrains Mono`: https://www.jetbrains.com/lp/mono/
.. _`index`: https://chafapy.mage.black
