.. _examples:

========
Examples
========

On this page you will find a few useful examples (which you can also find in the `GitHub repo`_.) when it comes to using chafa.py. These should cover most of the basics for reading and printing an image and they also include some messing around with :py:class:`chafa.CanvasConfig`.

If you are the sort of person who likes getting their hands dirty right away, take a look at these and read up on the methods and classes used in the api. That should be enough to get you to a pretty good point!

All the examples will be using this image and calling it ``snake.jpg``

.. image:: snake.jpg
    :width: 300
    :align: center

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
    print(canvas.print())


Using `Pillow`_
---------------

When reading pixel data from an image opened with `Pillow`_, we get a 2D array which needs to be reshaped into a 1D array before passing to chafa. This is still pretty fast since both Pillow and NumPy are well optimized.

::

    from chafa import *
    from PIL import Image
    import numpy as np

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
    pixels = np.array(image)
    pixels = np.reshape(pixels, pixels.size)

    # Init the canvas
    canvas = Canvas(config)

    # Draw to canvas
    canvas.draw_all_pixels(
        PixelType.CHAFA_PIXEL_RGB8,
        pixels,
        height,
        width,
        width * bands
    )

    # Write picture
    print(canvas.print())


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
    print(canvas.print())


.. currentmodule:: chafa

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
    print(canvas.print())



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
    print(canvas.print())


.. _`MagickWand`: https://imagemagick.org/script/magick-wand.php
.. _`Pillow`: https://python-pillow.org/
.. _`pyvips`: https://github.com/libvips/pyvips
.. _`GitHub repo`: https://github.com/guardkenzie/chafa.py