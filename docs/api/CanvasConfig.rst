.. currentmodule:: chafa

====================
Canvas Configuration
====================

::

    import chafa

    config = chafa.CanvasConfig()

    config.height = 10
    config.width  = 10

    config.fg_color = (255, 0, 255)

CanvasConfig
------------

A :py:class:`CanvasConfig` describes a set of parameters for :py:class:`Canvas`, such as its geometry, color space and other output characteristics.

To create a new :py:class:`CanvasConfig`, simply initialise that class. You can then modify it changing it's properties (which are inherited from it's base class :py:class:`ReadOnlyCanvasConfig`) and via it's setter functions e.g. :py:meth:`CanvasConfig.set_symbol_map` before using it to initialise a :py:class:`Canvas`.

Note that it is not possible to change a canvas' configuration after the canvas is created.

.. py:class:: CanvasConfig

    :bases: :py:class:`ReadOnlyCanvasConfig`

    .. py:method:: copy()

        Creates a new :py:class:`CanvasConfig` that's a copy of this one.

        :rtype: CanvasConfig

    
    .. py:method:: set_symbol_map(symbol_map: SymbolMap)

        Assigns a copy of symbol_map to config.

        :param SymbolMap symbol_map: The symbol_map.

    .. py:method:: calc_canvas_geometry(src_width: int, src_height: int, font_ratio: float, zoom: bool=False, stretch: bool=False)

        Calculates an optimal geometry for a :py:class:`Canvas` given the width and height of an input image, font ratio, zoom and stretch preferences. This will then set the config's width and height to the calculated values.

        :param int src_width: Width of the input image in pixels.
        :param int src_height: Height of the input image in pixels.
        :param float font_ratio: The font's width divided by its height.
        :param bool zoom: Upscale the image to fit the canvas.
        :param bool stretch: Ignore the aspect ratio of source.

        :raises ValueError: if src_width src_height or font_ratio are <= 0
        :raises TypeError: if zoom or stretch are None

    .. py:method:: set_fill_symbol_map(fill_symbol_map: SymbolMap)

        Assigns a copy of fill_symbol_map to config.

        Fill symbols are assigned according to their overall 
        foreground to background coverage, disregarding shape.

        :param SymbolMap fill_symbol_map: The fill symbol map.


ReadOnlyCanvasConfig
--------------------
This class describes a read only :py:class:`CanvasConfig`. This is returned from e.g. :py:meth:`Canvas.peek_config`.

The properties of a :py:class:`ReadOnlyCanvasConfig` become editable when inherited by a :py:class:`CanvasConfig`.

    .. attention::
        All properties of :py:class:`ReadOnlyCanvasConfig` can be inspected but not changed!

.. py:class:: ReadOnlyCanvasConfig


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


    .. py:method:: peek_symbol_map()

        Returns a read only version of the :py:class:`SymbolMap` belonging to the config.

        .. note::
            There are currently no implemented attributes or getter functions for :py:class:`ReadOnlySymbolMap`.

        :rtype: ReadOnlySymbolMap