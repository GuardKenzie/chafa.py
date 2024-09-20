===========
Enumerators
===========

Canvas Mode
___________

An enumerator for canvas modes. This determines how colours (and colour control codes) are used in the output from a canvas.An enumerator for canvas modes. This determines how colours (and colour control codes) are used in the output from a canvas.

.. py:class:: CanvasMode

    :bases: :py:class:`enum.IntEnum`

    .. py:attribute:: CHAFA_CANVAS_MODE_TRUECOLOR

        Truecolor.

    .. py:attribute:: CHAFA_CANVAS_MODE_INDEXED_256

        256 colors.

    .. py:attribute:: CHAFA_CANVAS_MODE_INDEXED_240

        256 colors, but avoid using the lower 16 whose values vary between terminal environments.

    .. py:attribute:: CHAFA_CANVAS_MODE_INDEXED_16

        16 colors using the aixterm ANSI extension.

    .. py:attribute:: CHAFA_CANVAS_MODE_FGBG_BGFG
	
        Default foreground and background colors, plus inversion.

    .. py:attribute:: CHAFA_CANVAS_MODE_FGBG

        Default foreground and background colors. No ANSI codes will be used.

    .. py:attribute:: CHAFA_CANVAS_MODE_INDEXED_8

        8 colors, compatible with original ANSI X3.64.

    .. py:attribute:: CHAFA_CANVAS_MODE_INDEXED_16_8

        16 FG colors (8 of which enabled with bold/bright) and 8 BG colors.

    .. py:attribute:: CHAFA_CANVAS_MODE_MAX

        Last supported canvas mode plus one.


Pixel Mode
__________
An enumerator for pixel modes. This determines how pixel graphics are rendered in the output.

.. py:class:: PixelMode

    :bases: :py:class:`enum.IntEnum`

    .. py:attribute:: CHAFA_PIXEL_MODE_SYMBOLS

        Pixel data is approximated using character symbols ("ANSI art").


    .. py:attribute:: CHAFA_PIXEL_MODE_SIXELS

        Pixel data is encoded as sixels.


    .. py:attribute:: CHAFA_PIXEL_MODE_KITTY

        Pixel data is encoded using the Kitty terminal protocol.


    .. py:attribute:: CHAFA_PIXEL_MODE_ITERM2

        Pixel data is encoded using the iTerm2 terminal protocol.


    .. py:attribute:: CHAFA_PIXEL_MODE_MAX

        Last supported pixel mode plus one.


Pixel Type
__________
An enumerator for pixel types. These represent pixel formats supported by :py:class:`ChafaCanvas` 

.. py:class:: PixelType

    :bases: :py:class:`enum.IntEnum`

    .. py:attribute:: CHAFA_PIXEL_RGBA8_PREMULTIPLIED
        
        Premultiplied RGBA, 8 bits per channel.


    .. py:attribute:: CHAFA_PIXEL_BGRA8_PREMULTIPLIED
        
        Premultiplied BGRA, 8 bits per channel.


    .. py:attribute:: CHAFA_PIXEL_ARGB8_PREMULTIPLIED
        
        Premultiplied ARGB, 8 bits per channel.


    .. py:attribute:: CHAFA_PIXEL_ABGR8_PREMULTIPLIED
        
        Premultiplied ABGR, 8 bits per channel.


    .. py:attribute:: CHAFA_PIXEL_RGBA8_UNASSOCIATED
        
        Unassociated RGBA, 8 bits per channel.


    .. py:attribute:: CHAFA_PIXEL_BGRA8_UNASSOCIATED
        
        Unassociated BGRA, 8 bits per channel.


    .. py:attribute:: CHAFA_PIXEL_ARGB8_UNASSOCIATED
        
        Unassociated ARGB, 8 bits per channel.


    .. py:attribute:: CHAFA_PIXEL_ABGR8_UNASSOCIATED
        
        Unassociated ABGR, 8 bits per channel.


    .. py:attribute:: CHAFA_PIXEL_RGB8
        
        Packed RGB (no alpha), 8 bits per channel.


    .. py:attribute:: CHAFA_PIXEL_BGR8
        
        Packed BGR (no alpha), 8 bits per channel.


    .. py:attribute:: CHAFA_PIXEL_MAX
	
        Last supported pixel type, plus one.

Dither Mode
___________

An enumerator for dither modes. This determines how dithering will be applied to the canvas when drawing.

.. py:class:: DitherMode

    :bases: :py:class:`enum.IntEnum`

    .. py:attribute:: CHAFA_DITHER_MODE_NONE
        
        No dithering.


    .. py:attribute:: CHAFA_DITHER_MODE_ORDERED
        
        Ordered dithering (Bayer or similar).


    .. py:attribute:: CHAFA_DITHER_MODE_DIFFUSION
        
        Error diffusion dithering (Floyd-Steinberg or similar).


    .. py:attribute:: CHAFA_DITHER_MODE_MAX
        
        Last supported dither mode plus one.

Color Extractor
_______________

An enumerator for colour extractors. This determines how colours are approximated in character symbol output.

.. py:class:: ColorExtractor

    :bases: :py:class:`enum.IntEnum`

    .. py:attribute:: CHAFA_COLOR_EXTRACTOR_AVERAGE

        Use the average colors of each symbol's coverage area.

    .. py:attribute:: CHAFA_COLOR_EXTRACTOR_MEDIAN

        Use the median colors of each symbol's coverage area.

    .. py:attribute:: CHAFA_COLOR_EXTRACTOR_MAX

        Last supported color extractor plus one.


Color Space
___________

An enumerator for colour spaces.

.. py:class:: ColorSpace

    :bases: :py:class:`enum.IntEnum`

    .. py:attribute:: CHAFA_COLOR_SPACE_RGB

        RGB color space. Fast but imprecise.

    .. py:attribute:: CHAFA_COLOR_SPACE_DIN99D

        DIN99d color space. Slower, but good perceptual color precision.

    .. py:attribute:: CHAFA_COLOR_SPACE_MAX

        Last supported color space plus one.


Optimizations
_____________

An enumerator for optimizations. When enabled, these may produce more compact output at the cost of reduced compatibility and increased CPU use. Output quality is unaffected.

.. py:class:: Optimizations

    :bases: :py:class:`enum.IntEnum`

    .. py:attribute:: CHAFA_OPTIMIZATION_REUSE_ATTRIBUTES

        Suppress redundant SGR control sequences.

    .. py:attribute:: CHAFA_OPTIMIZATION_SKIP_CELLS

        Reserved for future use.

    .. py:attribute:: CHAFA_OPTIMIZATION_REPEAT_CELLS

        Use REP sequence to compress repeated runs of similar cells.

    .. py:attribute:: CHAFA_OPTIMIZATION_NONE

        All optimizations disabled.

    .. py:attribute:: CHAFA_OPTIMIZATION_ALL

        All optimizations enabled.


Tuck
____
An enumerator for tucking styles. To be used in a :py:class:`Placement` to specify what to do if the image doesn't fit within the :py:class:`Canvas`'s bounds.

.. py:class:: Tuck

    :bases: :py:class:`enum.IntEnum`

    .. py:attribute:: CHAFA_TUCK_STRETCH
	
        Resize element to fit the area exactly, changing its aspect ratio.

    .. py:attribute:: CHAFA_TUCK_FIT  

        Resize element to fit the area, preserving its aspect ratio by adding padding.

    .. py:attribute:: CHAFA_TUCK_SHRINK_TO_FIT   

        Like CHAFA_TUCK_FIT , but prohibit enlargement.

    .. py:attribute:: CHAFA_TUCK_MAX
        
        Last supported tucking policy, plus one.

    .. versionadded:: 1.2.0

Align
_____
An enumerator for :py:class:`Placement`'s available vertical- and horizontal alignments.

.. py:class:: Align

    :bases: :py:class:`enum.IntEnum`

    .. py:attribute:: CHAFA_ALIGN_START
	
        Align flush with beginning of the area (top or left in LTR locales).

    .. py:attribute:: CHAFA_ALIGN_END
	
        Align flush with end of the area (bottom or right in LTR locales).

    .. py:attribute:: CHAFA_ALIGN_CENTER
	
        Align in the middle of the area.

    .. py:attribute:: CHAFA_ALIGN_MAX
	
        Last supported alignment, plus one.
    
    .. versionadded:: 1.2.0


Symbol Tags
___________
An enumerator for symbol tags. This can be used in :py:meth:`SymbolMap.add_by_tags` to specify which symbols to use in the output of a :py:class:`Canvas`.

.. py:class:: SymbolTags

    :bases: :py:class:`enum.IntEnum`

    .. py:attribute:: CHAFA_SYMBOL_TAG_NONE

        Special value meaning no symbols.

    .. py:attribute:: CHAFA_SYMBOL_TAG_SPACE
        
        Space.

    .. py:attribute:: CHAFA_SYMBOL_TAG_SOLID
        
        Solid (inverse of space).

    .. py:attribute:: CHAFA_SYMBOL_TAG_STIPPLE
        
        Stipple symbols.

    .. py:attribute:: CHAFA_SYMBOL_TAG_BLOCK
        
        Block symbols.

    .. py:attribute:: CHAFA_SYMBOL_TAG_BORDER
        
        Border symbols.

    .. py:attribute:: CHAFA_SYMBOL_TAG_DIAGONAL
        
        Diagonal border symbols.

    .. py:attribute:: CHAFA_SYMBOL_TAG_DOT
        
        Symbols that look like isolated dots (excluding Braille).

    .. py:attribute:: CHAFA_SYMBOL_TAG_QUAD
        
        Quadrant block symbols.

    .. py:attribute:: CHAFA_SYMBOL_TAG_HHALF
        
        Horizontal half block symbols.

    .. py:attribute:: CHAFA_SYMBOL_TAG_VHALF
        
        Vertical half block symbols.

    .. py:attribute:: CHAFA_SYMBOL_TAG_HALF
        
        Joint set of horizontal and vertical halves.

    .. py:attribute:: CHAFA_SYMBOL_TAG_INVERTED
        
        Symbols that are the inverse of simpler symbols. When two symbols complement each other, only one will have this tag.
        
    .. py:attribute:: CHAFA_SYMBOL_TAG_BRAILLE
        
        Braille symbols.

    .. py:attribute:: CHAFA_SYMBOL_TAG_TECHNICAL
        
        Miscellaneous technical symbols.

    .. py:attribute:: CHAFA_SYMBOL_TAG_GEOMETRIC
        
        Geometric shapes.

    .. py:attribute:: CHAFA_SYMBOL_TAG_ASCII
        
        Printable ASCII characters.

    .. py:attribute:: CHAFA_SYMBOL_TAG_ALPHA
        
        Letters.

    .. py:attribute:: CHAFA_SYMBOL_TAG_DIGIT
        
        Digits.

    .. py:attribute:: CHAFA_SYMBOL_TAG_ALNUM
        
        Joint set of letters and digits.

    .. py:attribute:: CHAFA_SYMBOL_TAG_NARROW
        
        Characters that are one cell wide.

    .. py:attribute:: CHAFA_SYMBOL_TAG_WIDE
        
        Characters that are two cells wide.

    .. py:attribute:: CHAFA_SYMBOL_TAG_AMBIGUOUS
        
        Characters of uncertain width. Always excluded unless specifically asked for.

    .. py:attribute:: CHAFA_SYMBOL_TAG_UGLY
        
        Characters that are generally undesired or unlikely to render well. Always excluded unless specifically asked for.
        

    .. py:attribute:: CHAFA_SYMBOL_TAG_LEGACY
        
        Legacy computer symbols, including sextants, wedges and more.

    .. py:attribute:: CHAFA_SYMBOL_TAG_SEXTANT
        
        Sextant 2x3 mosaics.

    .. py:attribute:: CHAFA_SYMBOL_TAG_WEDGE
        
        Wedge shapes that align with sextants.

    .. py:attribute:: CHAFA_SYMBOL_TAG_LATIN
        
        Latin and Latin-like symbols (superset of ASCII).

    .. py:attribute:: CHAFA_SYMBOL_TAG_EXTRA
        
        Symbols not in any other category.

    .. py:attribute:: CHAFA_SYMBOL_TAG_BAD
        
        Joint set of ugly and ambiguous characters. Always excluded unless specifically asked for.
        
    .. py:attribute:: CHAFA_SYMBOL_TAG_ALL

        Special value meaning all supported symbols.


Terminal Sequences
__________________

An enumeration of the control sequences supported by :py:class:`TermInfo`.

.. py:class:: TermSeq

    :bases: :py:class:`enum.IntEnum`

    .. py:attribute:: CHAFA_TERM_SEQ_RESET_TERMINAL_SOFT

        Reset the terminal to configured defaults.

    .. py:attribute:: CHAFA_TERM_SEQ_RESET_TERMINAL_HARD

        Reset the terminal to factory defaults.

    .. py:attribute:: CHAFA_TERM_SEQ_RESET_ATTRIBUTES

        Reset active graphics rendition (colors and other attributes) to terminal defaults.

    .. py:attribute:: CHAFA_TERM_SEQ_CLEAR

        Clear the screen.

    .. py:attribute:: CHAFA_TERM_SEQ_INVERT_COLORS

        Invert foreground and background colors (disable with RESET_ATTRIBUTES).

    .. py:attribute:: CHAFA_TERM_SEQ_CURSOR_TO_TOP_LEFT

        Move cursor to top left of screen.

    .. py:attribute:: CHAFA_TERM_SEQ_CURSOR_TO_BOTTOM_LEFT

        Move cursor to bottom left of screen.

    .. py:attribute:: CHAFA_TERM_SEQ_CURSOR_TO_POS

        Move cursor to specific position.

    .. py:attribute:: CHAFA_TERM_SEQ_CURSOR_UP_1

        Move cursor up one cell.

    .. py:attribute:: CHAFA_TERM_SEQ_CURSOR_UP

        Move cursor up N cells.

    .. py:attribute:: CHAFA_TERM_SEQ_CURSOR_DOWN_1

        Move cursor down one cell.

    .. py:attribute:: CHAFA_TERM_SEQ_CURSOR_DOWN

        Move cursor down N cells.

    .. py:attribute:: CHAFA_TERM_SEQ_CURSOR_LEFT_1

        Move cursor left one cell.

    .. py:attribute:: CHAFA_TERM_SEQ_CURSOR_LEFT

        Move cursor left N cells.

    .. py:attribute:: CHAFA_TERM_SEQ_CURSOR_RIGHT_1

        Move cursor right one cell.

    .. py:attribute:: CHAFA_TERM_SEQ_CURSOR_RIGHT

        Move cursor right N cells.

    .. py:attribute:: CHAFA_TERM_SEQ_CURSOR_UP_SCROLL

        Move cursor up one cell. Scroll area contents down when at the edge.

    .. py:attribute:: CHAFA_TERM_SEQ_CURSOR_DOWN_SCROLL

        Move cursor down one cell. Scroll area contents up when at the edge.

    .. py:attribute:: CHAFA_TERM_SEQ_INSERT_CELLS

        Insert blank cells at cursor position.

    .. py:attribute:: CHAFA_TERM_SEQ_DELETE_CELLS

        Delete cells at cursor position.

    .. py:attribute:: CHAFA_TERM_SEQ_INSERT_ROWS

        Insert rows at cursor position.

    .. py:attribute:: CHAFA_TERM_SEQ_DELETE_ROWS

        Delete rows at cursor position.

    .. py:attribute:: CHAFA_TERM_SEQ_SET_SCROLLING_ROWS

        Set scrolling area extents.

    .. py:attribute:: CHAFA_TERM_SEQ_ENABLE_INSERT

        Enable insert mode.

    .. py:attribute:: CHAFA_TERM_SEQ_DISABLE_INSERT

        Disable insert mode.

    .. py:attribute:: CHAFA_TERM_SEQ_ENABLE_CURSOR

        Show the cursor.

    .. py:attribute:: CHAFA_TERM_SEQ_DISABLE_CURSOR

        Hide the cursor.

    .. py:attribute:: CHAFA_TERM_SEQ_ENABLE_ECHO

        Make the terminal echo input locally.

    .. py:attribute:: CHAFA_TERM_SEQ_DISABLE_ECHO

        Don't echo input locally.

    .. py:attribute:: CHAFA_TERM_SEQ_ENABLE_WRAP

        Make cursor wrap around to the next row after output in the final column.

    .. py:attribute:: CHAFA_TERM_SEQ_DISABLE_WRAP

        Make cursor stay in place after output to the final column.

    .. py:attribute:: CHAFA_TERM_SEQ_SET_COLOR_FG_DIRECT

        Set foreground color (directcolor/truecolor).

    .. py:attribute:: CHAFA_TERM_SEQ_SET_COLOR_BG_DIRECT

        Set background color (directcolor/truecolor).

    .. py:attribute:: CHAFA_TERM_SEQ_SET_COLOR_FGBG_DIRECT

        Set foreground and background color (directcolor/truecolor).

    .. py:attribute:: CHAFA_TERM_SEQ_SET_COLOR_FG_256

        Set foreground color (256 colors).

    .. py:attribute:: CHAFA_TERM_SEQ_SET_COLOR_BG_256

        Set background color (256 colors).

    .. py:attribute:: CHAFA_TERM_SEQ_SET_COLOR_FGBG_256

        Set foreground and background colors (256 colors).

    .. py:attribute:: CHAFA_TERM_SEQ_SET_COLOR_FG_16

        Set foreground color (16 colors).

    .. py:attribute:: CHAFA_TERM_SEQ_SET_COLOR_BG_16

        Set background color (16 colors).

    .. py:attribute:: CHAFA_TERM_SEQ_SET_COLOR_FGBG_16

        Set foreground and background colors (16 colors).

    .. py:attribute:: CHAFA_TERM_SEQ_BEGIN_SIXELS

        Begin sixel image data.

    .. py:attribute:: CHAFA_TERM_SEQ_END_SIXELS

        End sixel image data.

    .. py:attribute:: CHAFA_TERM_SEQ_REPEAT_CHAR

        Repeat previous character N times.

    .. py:attribute:: CHAFA_TERM_SEQ_BEGIN_KITTY_IMMEDIATE_IMAGE_V1

        Begin upload of Kitty image for immediate display at cursor.

    .. py:attribute:: CHAFA_TERM_SEQ_END_KITTY_IMAGE

        End of Kitty image upload.

    .. py:attribute:: CHAFA_TERM_SEQ_BEGIN_KITTY_IMAGE_CHUNK

        Begin Kitty image data chunk.

    .. py:attribute:: CHAFA_TERM_SEQ_END_KITTY_IMAGE_CHUNK

        End Kitty image data chunk.

    .. py:attribute:: CHAFA_TERM_SEQ_BEGIN_ITERM2_IMAGE

        Begin iTerm2 image data.

    .. py:attribute:: CHAFA_TERM_SEQ_END_ITERM2_IMAGE

        End of iTerm2 image data.

    .. py:attribute:: CHAFA_TERM_SEQ_ENABLE_SIXEL_SCROLLING

        Enable sixel scrolling.

    .. py:attribute:: CHAFA_TERM_SEQ_DISABLE_SIXEL_SCROLLING

        Disable sixel scrolling.

    .. py:attribute:: CHAFA_TERM_SEQ_ENABLE_BOLD

        Enable boldface (disable with RESET_ATTRIBUTES).

    .. py:attribute:: CHAFA_TERM_SEQ_SET_COLOR_FG_8

        Set foreground color (8 colors).

    .. py:attribute:: CHAFA_TERM_SEQ_SET_COLOR_BG_8

        Set background color (8 colors).

    .. py:attribute:: CHAFA_TERM_SEQ_SET_COLOR_FGBG_8

        Set foreground and background colors (8 colors).

    .. py:attribute:: CHAFA_TERM_SEQ_MAX
        
        Last control sequence plus one.
