.. currentmodule:: chafa

==========
The Canvas
==========

::

    import chafa

    config = chafa.CanvasConfig()
    canvas = chafa.Canvas(config)

    pixels = [0, 0, 0, 0]

    canvas.draw_all_pixels(
        chafa.PixelType.CHAFA_PIXEL_RGBA8_UNASSOCIATED,
        pixels,
        1, 1, 1
    )

    for row in canvas[5:-5,5:-5]:
        for pix in row:
            pix.bg_color = (0, 255, 0)

    print(canvas.print().decode())

Canvas
------
A :py:class:`Canvas` is a canvas that can render its contents as text strings.

When you want to make a :py:class:`Canvas`, you can specify it's properties like the width, height, output pixel mode etc. by first creating a :py:class:`CanvasConfig` and then initialising :py:class:`Canvas` with that.

You can draw an image to the canvas using :py:meth:`Canvas.draw_all_pixels` and convert it to output bytes for printing with :py:meth:`Canvas.print`. Check out :ref:`pillow-example` for an example on how to load an image using `Pillow`_.

Alternatively, you can assign the :py:class:`Canvas` a :py:class:`Placement` with the :py:attr:`Canvas.placement` property if you want to control the alignment of the image on the :py:class:`Canvas`. If you go this route, you do not need to use :py:meth:`Canvas.draw_all_pixels`, and can go straight to :py:meth:`Canvas.print`.

The :py:class:`Canvas` supports indexing (and slicing) with ``[]``! This will return a :py:class:`CanvasInspector` or a `generator`_ for the relevant :py:class:`CanvasInspector` objects.

.. py:class:: Canvas(config: None|CanvasConfig)

    :param CanvasConfig|None config: The config to initialise the canvas with. If None is passed, the canvas will be initialised with hard-coded defaults.

    :raises TypeError: If config is not None or :py:class:`CanvasConfig`

    .. py:method:: __getitem__(pos)

        You can inspect pixels in the canvas by indexing, similar to if the canvas were a 2d array. When indexing, the first coordinate represents the row (or y coordinate) and the second represents the column (or x coordinate).

        When indexing using a single value, a `generator`_ of relevant :py:class:`CanvasInspector` objects will be returned, representing each pixel in the given row.
        
        ::

            for pixel in canvas[0]:
                pixel.char = "a"

        When indexing using two values, a single :py:class:`CanvasInspector` will be returned representing the given pixel.

        ::

            canvas[1, 4].fg_color = (0, 0, 255)

        Slicing is also supported! You can slice either the row or column coordinates and this will return generators as expected. For example; if you index using ``[:,3]`` you will get a generator for each pixel in the 3rd column of the canvas (0 indexed). 

        ::

            for pixel in canvas[:,3]:
                print(pixel.char)
        
        Slicing using ``[3:6,:5]`` will return generators for rows 3 to 5 inclusive. Each of these rows will be represented by a generator for :py:class:`CanvasInspector` objects representing pixels 0 to 4 inclusive.

        ::

            for row in canvas[3:6,:5]:
                for pixel in row:
                    pixel.remove_background()

        The take-away from this all is that indexing and slicing should work (mostly) the same as you would expect a 2d array to work. Check out the tutorial for more details.

        :param int|slice|tuple pos: The position to index

        :rtype: CanvasInspector
    

    .. py:property:: placement

        :type: Placement

        The :py:class:`Placement` of an :py:class:`Image` containing a :py:class:`Frame` on the canvas. Use this as an alternative to :py:meth:`draw_all_pixels` and for control over the image's alignment with :py:class:`Align` and :py:class:`Tuck`.

        .. versionadded:: 1.2.0


    .. py:method:: new_similar()

        Returns a new :py:class:`Canvas` configured similarly to this one.

        :rtype: Canvas

        .. versionadded:: 1.2.0


    .. py:method:: peek_config()

        Returns a read only version of the :py:class:`CanvasConfig` used to initialise the canvas.

        .. attention:: 
            This :py:class:`ReadOnlyCanvasConfig`'s properties can be inspected but not changed.

        :rtype: ReadOnlyCanvasConfig


    .. py:method:: draw_all_pixels(src_pixel_type: PixelType, src_pixels, src_width: int, src_height: int, src_rowstride: int)

        Draws the given src_pixels to the canvas. Depending on your set :py:class:`PixelMode`, this will be symbols, kitty sequences or sixel sequences. 

        To output the data after drawing, use the :py:meth:`print` method.

        .. note::
            Best performance is achieved by passing a :py:class:`ctypes.Array` for src_pixels. A fast way to do this is to use `Pillow`_; specifically the `` `Image.tobytes <https://pillow.readthedocs.io/en/stable/reference/Image.html#PIL.Image.Image.tobytes>`_ `` method. 

        :param PixelType src_pixel_type: The pixel type of src_pixels. This will determine what order the color channels will be read in and whether there is an alpha channel.
        :param list|tuple|array.array|ctypes.Array src_pixels: The source pixel data. This is a one dimensional array where every block of 3 (or 4 depending on the :py:class:`PixelType`) values represents one pixel of the image. The order of the channels is determined by src_pixel_type.

        :param int src_width:  The width of the source image.
        :param int src_height: The width of the source image.
        :param int src_rowstride: The number of values in src_image that represents one line pixels in the source image. Typically this will be the number of channels in the source image multiplied by src_width, e.g. for an image with no alpha channel and a width of 300 pixels, this will be ``3*300``.

        :raises ValueError: if src_width, src_height or src_rowstride are less than or equal to 0.

    .. py:method:: print(term_info: TermInfo = None, fallback: bool=False)

        Builds a UTF-8 string of terminal control sequences and symbols representing the canvas' current contents. This can e.g. be printed to a terminal. The exact choice of escape sequences and symbols, dimensions, etc. is determined by the configuration assigned to canvas on its creation.

        All output lines except for the last one will end in a newline.

        .. note:: The output of this method will need to be decoded with :py:meth:`bytes.decode`

        :param TermInfo term_info: The :py:class:`TermInfo` that will provide the control sequences used when printing. If None is specified, the term_info will be initialised with :py:meth:`TermDb.detect`.

        :param bool fallback: If True, the term_info (the one provided by :py:meth:`TermDb.detect` or the one provided by the user) will be supplemented with fallback control sequences.

        :raises TypeError: If term_info is not None or :py:class:`TermInfo`

        :rtype: bytes


CanvasInspector
---------------

The :py:class:`CanvasInspector` is an object that can inspect (and edit) individual characters in a :py:class:`Canvas`. It is mainly generated by indexing or slicing a :py:class:`Canvas`, however, you can initialise it yourself if you prefer.

You can think of the :py:class:`CanvasInspector` like a detective with a magnifying glass who's standing on the :py:class:`Canvas`. They can only inspect the current character they are on and have the authority to make changes to that pixel. You can then move the detective to another pixel by changing their coordinates.

.. class:: CanvasInspector(canvas: Canvas, y: int, x: int)

    :param Canvas canvas: The canvas to inspect
    :param int y: The initial y coordinate (starting from 0)
    :param int x: The initial x coordinate (starting from 0)

    :raises ValueError: if x or y are greater than or equal to the canvas's width or height respectively.

    .. py:property:: y

        :type: int

        The y coordinate of the inspector.

        :raises ValueError: if y is not less than the height of the canvas.


    .. py:property:: x

        :type: int

        The x coordinate of the inspector.

        :raises ValueError: if x is not less than the height of the canvas.
    
    .. py:property:: fg_color

        :type: tuple[int, int, int] | None

        The foreground color at the inspector's pixel. The color is represented as None if transparent or a tuple of 3 integers in range [0,255], representing the color in (R, G, B) format.

        For double-width characters, both cells will be set to the same color.

        :raises TypeError:  if fg_color is not an :py:class:`Iterable` other than :py:class:`str`.
        :raises ValueError: if fg_color is not None and does not contain exactly 3 values. 
        :raises ValueError: if fg_color contains a value greater than 255 or less than 0.

    .. py:property:: bg_color

        :type: tuple[int, int, int] | None

        The background color at the inspector's pixel. The color is represented as None if transparent or a tuple of 3 integers in range [0,255], representing the color in (R, G, B) format.

        For double-width characters, both cells will be set to the same color.

        :raises TypeError:  if bg_color is not an :py:class:`Iterable` other than :py:class:`str`.
        :raises ValueError: if bg_color is not None and does not contain exactly 3 values. 
        :raises ValueError: if bg_color contains a value greater than 255 or less than 0.

    .. py:property:: raw_fg_color
        
        :type: int

        The raw foreground color at the inspector's pixel. The colors are -1 for transparency, a packed 8-bit RGB value (``0x00RRGGBB``) in truecolor mode, or the raw pen value (0-255) in indexed modes.
        
        .. versionadded:: 1.1.0

    .. py:property:: raw_bg_color
        
        :type: int

        The raw background color at the inspector's pixel. The colors are -1 for transparency, a packed 8-bit RGB value (``0x00RRGGBB``) in truecolor mode, or the raw pen value (0-255) in indexed modes.

        .. versionadded:: 1.1.0

    .. py:property:: char

        :type: str

        The character at the inspector's pixel. For double-width characters, the leftmost cell must contain the character and the cell to the right of it will automatically be set to 0.

        :raises ValueError: if char is not of length 1.

    .. py:method:: remove_foreground()

        A function that sets the foreground color at the inspectors pixel to be transparent.

    .. py:method:: remove_background()

        A function that sets the background color at the inspectors pixel to be transparent.


.. _`generator`: https://docs.python.org/3/glossary.html#term-generator
.. _`MagickWand`: https://imagemagick.org/script/magick-wand.php
.. _`Pillow`: https://python-pillow.org/
