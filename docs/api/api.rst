===
API
===

.. module:: chafa

CanvasConfig
============ 

A :py:class:`CanvasConfig` describes a set of parameters for :py:class:`Canvas`, such as its geometry, color space and other output characteristics.

To create a new :py:class:`CanvasConfig`, simply initialise that class. You can then modify it changing it's properties and via it's setter functions e.g. :py:meth:`CanvasConfig.set_symbol_map` before using it to initialise a :py:class:`Canvas`.

Note that it is not possible to change a canvas' configuration after the canvas is created.


.. py:class:: ReadOnlyCanvasConfig

    This class describes a read only :py:class:`CanvasConfig`. This is returned from e.g. :py:meth:`Canvas.peek_config`.

    .. attention::
        All properties of :py:class:`ReadOnlyCanvasConfig` can be inspected but not changed!


    .. py:property:: width

        :type: int

        The config's width in character cells.

    .. py:property:: height

        :type: int

        The config's height in character cells.

    .. py:property:: cell_width
 
        :type: int

        The config's cell width in pixels.

    .. py:property:: cell_height

        :type: int

        The config's cell height in pixels.


    .. py:property:: pixel_mode

        :type: PixelMode

        The config's stored :py:class:`PixelMode`. This determines how pixel graphics are rendered in the output.

    .. py:property:: canvas_mode

        :type: CanvasMode

        The config's stored :py:class:`CanvasMode`. This determines how colours (and colour control codes) are used in the output.

    .. py:property:: color_extractor

        :type: ColorExtractor

        The config's stored :py:class:`ColorExtractor`. This determines how colours are approximated in character symbol output e.g. :py:attr:`PixelMode.CHAFA_PIXEL_MODE_SYMBOLS`.

    .. py:property:: color_space 

        :type: ColorSpace

        The config's stored :py:class:`ColorSpace`.

    .. py:property:: dither_mode

        :type: DitherMode

        The config's stored :py:class:`DitherMode`.

    .. py:property:: dither_intensity

        :type: float

        The relative intensity of the dithering pattern applied during image conversion. 1.0 is the default, corresponding to a moderate intensity.

    .. py:property:: dither_width

        :type: int

        The config's stored dither grain width in pixels. These values can be 1, 2, 4 or 8. 8 corresponds to the size of an entire character cell. The default is 4 pixels.

    .. py:property:: dither_height

        :type: int

        The config's stored dither grain width in pixels. These values can be 1, 2, 4 or 8. 8 corresponds to the size of an entire character cell. The default is 4 pixels.

        .. py:property:: transparency_threshold

        :type: float

        The threshold above which full transparency will be used.

    .. py:property:: fg_only

        :type: bool

        Queries whether to use foreground colors only, leaving the background unmodified in the canvas output.
        When this is set, the canvas will emit escape codes to set the foreground color only.
        
        .. note::

            This is relevant only when the :py:attr:`pixel_mode` is set to :py:attr:`PixelMode.CHAFA_PIXEL_MODE_SYMBOLS`.

    .. py:property:: fg_color

        :type: tuple[int, int, int]

        The assumed foreground color of the output device. This is used to determine how to apply the foreground pen in FGBG modes like :py:attr:`CanvasMode.CHAFA_CANVAS_MODE_FGBG`.

        The color is a tuple containing 3 integers in range [0,255] corresponding to red, green and blue respectively.

    .. py:property:: bg_color

        :type: tuple[int, int, int]

        The assumed background color of the output device. This is used to determine how to apply the background pen in FGBG modes like :py:attr:`CanvasMode.CHAFA_CANVAS_MODE_FGBG`.

        The color is a tuple containing 3 integers in range [0,255] corresponding to red, green and blue respectively.
    

    .. py:property:: preprocessing

        :type: bool

        Indicates whether automatic image preprocessing should be enabled. This allows Chafa to boost contrast and saturation in an attempt to improve legibility. 
        
        .. note::

            The type of preprocessing applied (if any) depends on the :py:attr:`canvas_mode`.

    .. py:property:: work_factor

        :type: float

        Gets the work/quality tradeoff factor. A higher value means more time and memory will be spent towards a higher quality output.

    .. py:property:: optimizations

        :type: tuple[Optimizations, ...]

        The config's optimization flags. When enabled, these may produce more compact output at the cost of reduced compatibility and increased CPU use.

        The config's optimizations are a tuple containing all enabled flags.

        .. note::
            Output quality is unaffected by optimizations.


    .. py:method:: get_geometry()

        Get the config's canvas geometry in character cells. This is the same as inspecting :py:attr:`width` and :py:attr:`height`

        :rtype: tuple[int, int] of width and height.


    .. py:method:: calc_canvas_geometry(src_width: int, src_height: int, font_ratio: float, zoom: bool=False, stretch: bool=False)

        Calculates an optimal geometry for a :py:class:`Canvas` given the width and height of an input image, font ratio, zoom and stretch preferences. This will then set the config's width and height to the calculated values.

        :param int src_width: Width of the input image in pixels.
        :param int src_height: Height of the input image in pixels.
        :param float font_ratio: The font's width divided by its height.
        :param bool zoom: Upscale the image to fit the canvas.
        :param bool stretch: Ignore the aspect ratio of source.

        :raises ValueError: if src_width src_height or font_ratio are <= 0
        :raises TypeError: if zoom or stretch are None

    .. py:method:: peek_symbol_map()

        Returns a read only version of the :py:class:`SymbolMap` belonging to the config.

        .. note::
            There are currently no implemented attributes or getter functions for :py:class:`ReadOnlySymbolMap`.

        :rtype: ReadOnlySymbolMap

.. py:class:: CanvasConfig

    :bases: :py:class:`ReadOnlyCanvasConfig`

    .. py:method:: copy()

        Creates a new :py:class:`CanvasConfig` that's a copy of this one.

        :rtype: CanvasConfig

    
    .. py:method:: set_symbol_map(symbol_map: SymbolMap)

        Assigns a copy of symbol_map to config.

        :param SymbolMap symbol_map: The symbol_map.

    .. py:method:: set_fill_symbol_map(fill_symbol_map: SymbolMap)

        Assigns a copy of fill_symbol_map to config.

        Fill symbols are assigned according to their overall 
        foreground to background coverage, disregarding shape.

        :param SymbolMap fill_symbol_map: The fill symbol map.


Canvas
======

A :py:class:`Canvas` is a canvas that can render its contents as text strings.

When you want to make a :py:class:`Canvas`, you can specify it's properties like the width, height, output pixel mode etc. by first creating a :py:class:`CanvasConfig` and then initialising :py:class:`Canvas` with that.

You can draw an image to the canvas using :py:meth:`Canvas.draw_all_pixels` and convert it to output bytes for printing with :py:meth:`Canvas.print`. *(pssst: check out the :py:class:`loader.Loader` to make drawing images easier)*.

The :py:class:`Canvas` supports indexing (and slicing) with ``[]``! This will return a :py:class:`CanvasInspector` or a `generator`_ for the relevant :py:class:`CanvasInspector` objects.

.. py:class:: Canvas(config: None|CanvasConfig, term_info: TermInfo=None)

    :param CanvasConfig|None config: The config to initialise the canvas with. If None is passed, the canvas will be initialised with hard-coded defaults.

    :param TermInfo term_info: The :py:class:`TermInfo` that will be used when printing. If None is specified, the term_info will be initialised with :py:meth:`TermDb.detect`

    :raises TypeError: If term_info is not None or :py:class:`TermInfo`
    :raises TypeError: If config is not None or :py:class:`CanvasConfig`

    .. py:method:: __getitem__(y)

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
        

    .. py:method:: peek_config()

        Returns a read only version of the :py:class:`CanvasConfig` used to initialise the canvas.

        .. attention:: 
            This :py:class:`ReadOnlyCanvasConfig`'s properties can be inspected but not changed.

        :rtype: ReadOnlyCanvasConfig


    .. py:method:: draw_all_pixels(src_pixel_type: PixelType, src_pixels, src_width: int, src_height: int, src_rowstride: int)

        Draws the given src_pixels to the canvas. Depending on your set :py:class:`PixelMode`, this will be symbols, kitty sequences or sixel sequences. 

        To output the data after drawing, use the :py:meth:`print` method.

        .. note::
            Best performance is achieved by passing a :py:class:`ctypes.Array` for src_pixels. The :py:class:`chafa.loader.Loader` class provides convenient (and reasonably fast) methods for this using the `MagickWand <https://imagemagick.org/script/magick-wand.php>`_ C-library.

        :param PixelType src_pixel_type: The pixel type of src_pixels. This will determine what order the color channels will be read in and whether there is an alpha channel.
        :param list|tuple|array.array|ctypes.Array src_pixels: The source pixel data. This is a one dimensional array where every block of 3 (or 4 depending on the :py:class:`PixelType`) values represents one pixel of the image. The order of the channels is determined by src_pixel_type.

        :param int src_width:  The width of the source image.
        :param int src_height: The width of the source image.
        :param int src_rowstride: The number of values in src_image that represents one line pixels in the source image. Typically this will be the number of channels in the source image multiplied by src_width, e.g. for an image with no alpha channel and a width of 300 pixels, this will be ``3*300``.

        :raises ValueError: if src_width, src_height or src_rowstride are less than or equal to 0.

    .. py:method:: print()

        Builds a UTF-8 string of terminal control sequences and symbols representing the canvas' current contents. This can e.g. be printed to a terminal. The exact choice of escape sequences and symbols, dimensions, etc. is determined by the configuration assigned to canvas on its creation.

        All output lines except for the last one will end in a newline.

        :rtype: str


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

    .. py:property:: char

        :type: str

        The character at the inspector's pixel. For double-width characters, the leftmost cell must contain the character and the cell to the right of it will automatically be set to 0.

        :raises ValueError: if char is not of length 1.

    .. py:method:: remove_foreground()

        A function that sets the foreground color at the inspectors pixel to be transparent.

    .. py:method:: remove_background()

        A function that sets the background color at the inspectors pixel to be transparent.



SymbolMap
=========

A :py:class:`SymbolMap` describes a selection of the supported textual symbols that can be used in building a printable output string from a :py:class:`Canvas`.

To create a new :py:class:`SymbolMap`, simply initialise the class. You can then add symbols to it using :py:meth:`SymbolMap.add_by_tags` before copying it into a :py:class:`CanvasConfig` using :py:meth:`CanvasConfig.set_symbol_map`.

Note that some symbols match multiple tags, so it makes sense to e.g. add symbols matching :py:attr:`SymbolTags.CHAFA_SYMBOL_TAG_BORDER` and then removing symbols matching :py:attr:`SymbolTags.CHAFA_SYMBOL_TAG_DIAGONAL`.

.. note:: 
    The number of available symbols is a significant factor in the speed of:py:class:`Canvas`. For the fastest possible operation you could use a single symbol. :py:attr:`SymbolTags.CHAFA_SYMBOL_TAG_VHALF` works well by itself.

.. py:class:: ReadOnlySymbolMap

    .. py:method:: copy()

        Returns a new :py:class:`SymbolMap` that's a copy of this one.

        :rtype: SymbolMap


.. py:class:: SymbolMap

    :bases: :py:class:`ReadOnlySymbolMap`

    .. py:method:: add_by_tags(tags: SymbolTags)

        Adds symbols matching the set of tags to the symbol map.

        :param SymbolTags tags: The set of tags to add to the map.

    .. py:method:: remove_by_tags(tags: SymbolTags)

        Removes symbols matching the set of tags from the symbol map.

        :param SymbolTags tags: The set of tags to remove from the map.

    .. py:method:: add_by_range(first: str, last: str)

        Adds symbols in the code point range starting with the character first and ending with the character last to the symbol map.

        For example, if first is given as ``a`` and last is given as ``f``, all characters ``a, b, c, d, e, f`` will be added to the map.

        :param str first: First code point to add, inclusive.
        :param str last: Last code point to add, inclusive.

        :raises TypeError: if first or last are not of type str.
        :raises ValueError: if first or last have length other than 1.

    .. py:method:: remove_by_range(first: str, last: str)

        Removes symbols in the code point range starting with the character first and ending with the character last from the symbol map.

        :param str first: First code point to remove, inclusive.
        :param str last: Last code point to remove, inclusive.

        :raises TypeError: if first or last are not of type str.
        :raises ValueError: if first or last have length other than 1.

    .. py:method:: apply_selectors(selectors: str)

        Parses a string consisting of symbol tags separated by ``+-,`` and applies the pattern to the symbol map. If the string begins with ``+`` or ``-``, it's understood to be relative to the current set in the symbol map, otherwise the map is cleared first.

        The symbol tags are string versions of :py:class:`SymbolTags`, i.e.

        ================================================  ===========
        :py:class:`SymbolTags`                            String
        ================================================  ===========
        :py:meth:`SymbolTags.CHAFA_SYMBOL_TAG_ALL`        all
        :py:meth:`SymbolTags.CHAFA_SYMBOL_TAG_NONE`       none
        :py:meth:`SymbolTags.CHAFA_SYMBOL_TAG_SPACE`      space
        :py:meth:`SymbolTags.CHAFA_SYMBOL_TAG_SOLID`      solid
        :py:meth:`SymbolTags.CHAFA_SYMBOL_TAG_STIPPLE`    stipple
        :py:meth:`SymbolTags.CHAFA_SYMBOL_TAG_BLOCK`      block
        :py:meth:`SymbolTags.CHAFA_SYMBOL_TAG_BORDER`     border
        :py:meth:`SymbolTags.CHAFA_SYMBOL_TAG_DIAGONAL`   diagonal
        :py:meth:`SymbolTags.CHAFA_SYMBOL_TAG_DOT`        dot
        :py:meth:`SymbolTags.CHAFA_SYMBOL_TAG_QUAD`       quad
        :py:meth:`SymbolTags.CHAFA_SYMBOL_TAG_HALF`       half
        :py:meth:`SymbolTags.CHAFA_SYMBOL_TAG_EXTRA`      extra
        ================================================  ===========

        other :py:class:`SymbolTags` follow the same format and are supported.

        For example: ``block,border`` sets map to contain symbols matching either of those tags. ``+block,border-dot,stipple`` adds block and border symbols then removes dot and stipple symbols.

        :param str selectors: The string of selectors to apply.

        :raises ValueError: if the selectors string is invalid.

TermDb
======

A :py:class:`TermDb` contains information on terminals, and can be used to obtain a suitable :py:class:`TermInfo` for a terminal environment.

.. py:class:: TermDb(no_defaults: bool=False)

    :param bool no_defaults: If ``True``, the class will be initialised blank instead of with the default global database.

    .. py:method:: copy()

        :rtype: TermDb

        Returns a new :py:class:`TermDb` which is a copy of this one.

    .. py:method:: detect()

        :rtype: TermInfo

        Builds a new :py:class:`TermInfo` with capabilities implied by the system environment variables (principally the ``TERM`` variable, but also others).

    .. py:method:: get_fallback_info()

        :rtype: TermInfo

        Builds a new :py:class:`TermInfo` with fallback control sequences. This can be used with unknown but presumably modern terminals, or to supplement missing capabilities in a detected terminal.


TermInfo
========

A :py:class:`TermInfo` describes the characteristics of one particular kind of display terminal. It stores control sequences that can be used to move the cursor, change text attributes, mark the beginning and end of sixel graphics data, etc.

:py:class:`TermInfo` also implements an efficient low-level API for formatting these sequences with marshaled arguments so they can be sent to the terminal.

.. py:class:: TermInfo

    .. py:method:: copy()

        Returns a new :py:class:`TermInfo` that is a copy of this one.

        :rtype: TermInfo

    .. py:method:: supplement(source: TermInfo)

        Supplements missing sequences in this :py:class:`TermInfo` with ones copied from source.

        :param TermInfo source: The :py:class:`TermInfo` to copy sequences from.

    .. py:method:: have_seq(seq: TermSeq)

        Checks if :py:class:`TermInfo` can emit seq.
        
        :param TermSeq seq: A :py:class:`TermSeq` to query for.

        :rtype: bool

    .. py:method:: detect_capabilities()

        A method that tries to automatically detect the current terminal's capabilities.

        The priority for :py:class:`CanvasMode` is

        #. :py:attr:`CanvasMode.CHAFA_CANVAS_MODE_TRUECOLOR` 
        #. :py:attr:`CanvasMode.CHAFA_CANVAS_MODE_INDEXED_240` 
        #. :py:attr:`CanvasMode.CHAFA_CANVAS_MODE_INDEXED_16` 
        #. :py:attr:`CanvasMode.CHAFA_CANVAS_MODE_FGBG_BGFG` 
        #. :py:attr:`CanvasMode.CHAFA_CANVAS_MODE_FGBG` 

        The priority for :py:class:`PixelMode` is

        #. :py:attr:`PixelMode.CHAFA_PIXEL_MODE_KITTY`
        #. :py:attr:`PixelMode.CHAFA_PIXEL_MODE_SIXELS`
        #. :py:attr:`PixelMode.CHAFA_PIXEL_MODE_SYMBOLS`

        You can use the results for :py:attr:`CanvasConfig.canvas_mode` and :py:attr:`CanvasConfig.pixel_mode` in your :py:class:`CanvasConfig`.

        :rtype: TerminalCapabilities


.. py:class:: TermInfo.TerminalCapabilities

    .. py:attribute:: canvas_mode

        :type: CanvasMode

    .. py:attribute:: pixel_mode

        :type: PixelMode


.. _`generator`: https://docs.python.org/3/glossary.html#term-generator