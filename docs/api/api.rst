===
API
===

CanvasConfig
============ 

A :py:class:`CanvasConfig` describes a set of parameters for :py:class:`Canvas`, such as its geometry, color space and other output characteristics.

To create a new :py:class:`CanvasConfig`, simply initialise this class. You can then modify it changing it's properties and via it's setter functions e.g. :py:meth:`CanvasConfig.set_symbol_map` before using it to initialise a :py:class:`Canvas`.

Note that it is not possible to change a canvas' configuration after the canvas is created.

.. py:class:: CanvasConfig


    .. py:property:: height

        :type: int

        Sets the config's height in character cells.

    .. py:property:: width

        :type: int

        Sets the config's width in character cells.

    .. py:property:: pixel_mode

        :type: PixelMode

        Sets config's stored :py:class:`PixelMode`. This determines how pixel graphics are rendered in the output.

    .. py:property:: canvas_mode

        :type: CanvasMode

        Sets config's stored `CanvasMode`. This determines how colours (and colour control codes) are used in the output.
    
    .. py:property:: dither_width

        :type: int

        Sets config's stored dither grain width in pixels. These values can be 1, 2, 4 or 8. 8 corresponds to the size of an entire character cell. The default is 4 pixels.

    .. py:property:: dither_height

        :type: int

        Sets config's stored dither grain width in pixels. These values can be 1, 2, 4 or 8. 8 corresponds to the size of an entire character cell. The default is 4 pixels.

    .. py:property:: cell_height

        :type: int

        Sets config's cell height in pixels.

    .. py:property:: cell_width
 
        :type: int

        Sets config's cell width in pixels.

    .. py:property:: color_extractor

        :type: ColorExtractor

        The config's stored :py:class:`ColorExtractor`. This determines how colours are approximated in character symbol output.

    .. py:property:: color_space

        :type: ColorSpace

        The config's stored :py:class:`ColorSpace`.

    .. py:property:: preprocessing

        :type: bool

        Indicates whether automatic image preprocessing should be enabled. This allows Chafa to boost contrast and saturation in an attempt to improve legibility. 
        
        .. note::

            The type of preprocessing applied (if any) depends on the :py:attr:`canvas_mode`.


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
        :raises ValueError: if src_width or src_height are <= 0

SymbolMap
=========

A :py:class:`SymbolMap` describes a selection of the supported textual symbols that can be used in building a printable output string from a :py:class:`Canvas`.

To create a new :py:class:`SymbolMap`, simply initialise the class. You can then add symbols to it using :py:meth:`SymbolMap.add_by_tags` before copying it into a :py:class:`CanvasConfig` using :py:meth:`CanvasConfig.set_symbol_map`.

Note that some symbols match multiple tags, so it makes sense to e.g. add symbols matching :py:attr:`SymbolTags.CHAFA_SYMBOL_TAG_BORDER` and then removing symbols matching :py:attr:`SymbolTags.CHAFA_SYMBOL_TAG_DIAGONAL`.

.. note:: 
    The number of available symbols is a significant factor in the speed of:py:class:`Canvas`. For the fastest possible operation you could use a single symbol. :py:attr:`SymbolTags.CHAFA_SYMBOL_TAG_VHALF` works well by itself.


.. py:class:: SymbolMap

    .. py:method:: add_by_tags(tags: SymbolTags)

        :param SymbolTags tags: Adds symbols matching the set of tags.


TermDb
======

A :py:class:`TermDb` contains information on terminals, and can be used to obtain a suitable :py:class:`TermInfo` for a terminal environment.

.. py:class:: TermDb(no_defaults: bool=False)

    :param bool no_defaults: If ``True``, the class will be initialised blank instead of with the default global database.

    .. py:method:: detect()

        :rtype: TermInfo

        Builds a new :py:class:`TermInfo` with capabilities implied by the system environment variables (principally the ``TERM`` variable, but also others).


TermInfo
========

A :py:class:`TermInfo` describes the characteristics of one particular kind of display terminal. It stores control sequences that can be used to move the cursor, change text attributes, mark the beginning and end of sixel graphics data, etc.

:py:class:`TermInfo` also implements an efficient low-level API for formatting these sequences with marshaled arguments so they can be sent to the terminal.

.. py:class:: TermInfo

    .. py:method:: have_seq(seq: TermSeq)

        Checks if :py:class:`TermInfo` can emit seq.
        
        :param TermSeq seq: A :py:class:`TermSeq` to query for.

        :rtype: bool

    .. py:method:: detect_capabilities()

        A method that tries to automatically detect the current terminal's capabilities.

        You can use the results for :py:attr:`CanvasConfig.canvas_mode` and :py:attr:`CanvasConfig.pixel_mode` in your :py:class:`CanvasConfig`.

        :rtype: TerminalCapabilities