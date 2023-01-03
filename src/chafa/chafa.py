import ctypes
from dataclasses import dataclass
from typing import Tuple, Sequence, Union # PEP 484 
from enum import IntEnum
import sys

#
# === PIXEL MODES ===
#

class PixelMode(IntEnum):
    CHAFA_PIXEL_MODE_SYMBOLS = 0
    CHAFA_PIXEL_MODE_SIXELS  = 1
    CHAFA_PIXEL_MODE_KITTY   = 2
    CHAFA_PIXEL_MODE_ITERM2  = 3
    CHAFA_PIXEL_MODE_MAX     = 4

#
# === DITHER MODE ===
#

class DitherMode(IntEnum):
    CHAFA_DITHER_MODE_NONE       = 0
    CHAFA_DITHER_MODE_ORDERED    = 1
    CHAFA_DITHER_MODE_DIFFUSION  = 2

    CHAFA_DITHER_MODE_MAX        = 3


#
# === CANVAS MODES ===
#

class CanvasMode(IntEnum):
    CHAFA_CANVAS_MODE_TRUECOLOR     = 0
    CHAFA_CANVAS_MODE_INDEXED_256   = 1
    CHAFA_CANVAS_MODE_INDEXED_240   = 2
    CHAFA_CANVAS_MODE_INDEXED_16    = 3
    CHAFA_CANVAS_MODE_FGBG_BGFG     = 4
    CHAFA_CANVAS_MODE_FGBG          = 5
    CHAFA_CANVAS_MODE_INDEXED_8     = 6
    CHAFA_CANVAS_MODE_INDEXED_16_8  = 7

    CHAFA_CANVAS_MODE_MAX           = 8


#
# === DITHER MODES ===
#

class DitherMode(IntEnum):
    CHAFA_DITHER_MODE_NONE      = 0
    CHAFA_DITHER_MODE_ORDERED   = 1
    CHAFA_DITHER_MODE_DIFFUSION = 2

    CHAFA_DITHER_MODE_MAX       = 3


#
# === COLOR SPACE ===
#

class ColorSpace(IntEnum):
    CHAFA_COLOR_SPACE_RGB    = 0
    CHAFA_COLOR_SPACE_DIN99D = 1

    CHAFA_COLOR_SPACE_MAX    = 2


#
# === COLOR EXTRACTOR ===
#

class ColorExtractor(IntEnum):
    CHAFA_COLOR_EXTRACTOR_AVERAGE = 0
    CHAFA_COLOR_EXTRACTOR_MEDIAN  = 1

    CHAFA_COLOR_SPACE_MAX         = 2


#
# === OPTIMIZATIONS ===
#

class Optimizations(IntEnum):
    CHAFA_OPTIMIZATION_REUSE_ATTRIBUTES = (1 << 0),
    CHAFA_OPTIMIZATION_SKIP_CELLS       = (1 << 1),
    CHAFA_OPTIMIZATION_REPEAT_CELLS     = (1 << 2),

    CHAFA_OPTIMIZATION_NONE             = 0,
    CHAFA_OPTIMIZATION_ALL              = 0x7fffffff


#
# === PIXEL TYPE ===
#

class PixelType(IntEnum):
    CHAFA_PIXEL_RGBA8_PREMULTIPLIED = 0
    CHAFA_PIXEL_BGRA8_PREMULTIPLIED = 1
    CHAFA_PIXEL_ARGB8_PREMULTIPLIED = 2
    CHAFA_PIXEL_ABGR8_PREMULTIPLIED = 3

    CHAFA_PIXEL_RGBA8_UNASSOCIATED = 4
    CHAFA_PIXEL_BGRA8_UNASSOCIATED = 5
    CHAFA_PIXEL_ARGB8_UNASSOCIATED = 6
    CHAFA_PIXEL_ABGR8_UNASSOCIATED = 7
    
    CHAFA_PIXEL_RGB8 = 8
    CHAFA_PIXEL_BGR8 = 9
    CHAFA_PIXEL_MAX  = 10


#
# === SYMBOL TAGS ===
#

class SymbolTags(IntEnum):
    CHAFA_SYMBOL_TAG_NONE        = 0

    CHAFA_SYMBOL_TAG_SPACE       = (1 <<  0)
    CHAFA_SYMBOL_TAG_SOLID       = (1 <<  1)
    CHAFA_SYMBOL_TAG_STIPPLE     = (1 <<  2)
    CHAFA_SYMBOL_TAG_BLOCK       = (1 <<  3)
    CHAFA_SYMBOL_TAG_BORDER      = (1 <<  4)
    CHAFA_SYMBOL_TAG_DIAGONAL    = (1 <<  5)
    CHAFA_SYMBOL_TAG_DOT         = (1 <<  6)
    CHAFA_SYMBOL_TAG_QUAD        = (1 <<  7)
    CHAFA_SYMBOL_TAG_HHALF       = (1 <<  8)
    CHAFA_SYMBOL_TAG_VHALF       = (1 <<  9)
    CHAFA_SYMBOL_TAG_HALF        = ((CHAFA_SYMBOL_TAG_HHALF) | (CHAFA_SYMBOL_TAG_VHALF))
    CHAFA_SYMBOL_TAG_INVERTED    = (1 << 10)
    CHAFA_SYMBOL_TAG_BRAILLE     = (1 << 11)
    CHAFA_SYMBOL_TAG_TECHNICAL   = (1 << 12)
    CHAFA_SYMBOL_TAG_GEOMETRIC   = (1 << 13)
    CHAFA_SYMBOL_TAG_ASCII       = (1 << 14)
    CHAFA_SYMBOL_TAG_ALPHA       = (1 << 15)
    CHAFA_SYMBOL_TAG_DIGIT       = (1 << 16)
    CHAFA_SYMBOL_TAG_ALNUM       = CHAFA_SYMBOL_TAG_ALPHA | CHAFA_SYMBOL_TAG_DIGIT
    CHAFA_SYMBOL_TAG_NARROW      = (1 << 17)
    CHAFA_SYMBOL_TAG_WIDE        = (1 << 18)
    CHAFA_SYMBOL_TAG_AMBIGUOUS   = (1 << 19)
    CHAFA_SYMBOL_TAG_UGLY        = (1 << 20)
    CHAFA_SYMBOL_TAG_LEGACY      = (1 << 21)
    CHAFA_SYMBOL_TAG_SEXTANT     = (1 << 22)
    CHAFA_SYMBOL_TAG_WEDGE       = (1 << 23)
    CHAFA_SYMBOL_TAG_LATIN       = (1 << 24)
    CHAFA_SYMBOL_TAG_EXTRA       = (1 << 30)
    CHAFA_SYMBOL_TAG_BAD         = CHAFA_SYMBOL_TAG_AMBIGUOUS | CHAFA_SYMBOL_TAG_UGLY
    CHAFA_SYMBOL_TAG_ALL         = ~(CHAFA_SYMBOL_TAG_EXTRA | CHAFA_SYMBOL_TAG_BAD)


#
# === Term sequences ===
#

class TermSeq(IntEnum):
    CHAFA_TERM_SEQ_RESET_TERMINAL_SOFT = 0
    CHAFA_TERM_SEQ_RESET_TERMINAL_HARD = 1
    CHAFA_TERM_SEQ_RESET_ATTRIBUTES    = 2

    CHAFA_TERM_SEQ_CLEAR         = 3
    CHAFA_TERM_SEQ_INVERT_COLORS = 4

    CHAFA_TERM_SEQ_CURSOR_TO_TOP_LEFT    = 5
    CHAFA_TERM_SEQ_CURSOR_TO_BOTTOM_LEFT = 6
    CHAFA_TERM_SEQ_CURSOR_TO_POS         = 7
    CHAFA_TERM_SEQ_CURSOR_UP_1           = 8
    CHAFA_TERM_SEQ_CURSOR_UP             = 9
    CHAFA_TERM_SEQ_CURSOR_DOWN_1         = 10
    CHAFA_TERM_SEQ_CURSOR_DOWN           = 11
    CHAFA_TERM_SEQ_CURSOR_LEFT_1         = 12
    CHAFA_TERM_SEQ_CURSOR_LEFT           = 13
    CHAFA_TERM_SEQ_CURSOR_RIGHT_1        = 14
    CHAFA_TERM_SEQ_CURSOR_RIGHT          = 15
    CHAFA_TERM_SEQ_CURSOR_UP_SCROLL      = 16
    CHAFA_TERM_SEQ_CURSOR_DOWN_SCROLL    = 17

    CHAFA_TERM_SEQ_INSERT_CELLS = 18
    CHAFA_TERM_SEQ_DELETE_CELLS = 19
    CHAFA_TERM_SEQ_INSERT_ROWS  = 20
    CHAFA_TERM_SEQ_DELETE_ROWS  = 21

    CHAFA_TERM_SEQ_SET_SCROLLING_ROWS = 22

    CHAFA_TERM_SEQ_ENABLE_INSERT  = 23
    CHAFA_TERM_SEQ_DISABLE_INSERT = 24

    CHAFA_TERM_SEQ_ENABLE_CURSOR  = 25
    CHAFA_TERM_SEQ_DISABLE_CURSOR = 26

    CHAFA_TERM_SEQ_ENABLE_ECHO  = 27
    CHAFA_TERM_SEQ_DISABLE_ECHO = 28

    CHAFA_TERM_SEQ_ENABLE_WRAP  = 29
    CHAFA_TERM_SEQ_DISABLE_WRAP = 30

    CHAFA_TERM_SEQ_SET_COLOR_FG_DIRECT   = 31
    CHAFA_TERM_SEQ_SET_COLOR_BG_DIRECT   = 32
    CHAFA_TERM_SEQ_SET_COLOR_FGBG_DIRECT = 33

    CHAFA_TERM_SEQ_SET_COLOR_FG_256   = 34
    CHAFA_TERM_SEQ_SET_COLOR_BG_256   = 35
    CHAFA_TERM_SEQ_SET_COLOR_FGBG_256 = 36

    CHAFA_TERM_SEQ_SET_COLOR_FG_16   = 37
    CHAFA_TERM_SEQ_SET_COLOR_BG_16   = 38
    CHAFA_TERM_SEQ_SET_COLOR_FGBG_16 = 39

    CHAFA_TERM_SEQ_BEGIN_SIXELS = 40
    CHAFA_TERM_SEQ_END_SIXELS   = 41
    CHAFA_TERM_SEQ_REPEAT_CHAR  = 42

    CHAFA_TERM_SEQ_BEGIN_KITTY_IMMEDIATE_IMAGE_V1 = 43
    CHAFA_TERM_SEQ_END_KITTY_IMAGE                = 44
    CHAFA_TERM_SEQ_BEGIN_KITTY_IMAGE_CHUNK        = 45
    CHAFA_TERM_SEQ_END_KITTY_IMAGE_CHUNK          = 46

    CHAFA_TERM_SEQ_BEGIN_ITERM2_IMAGE = 47
    CHAFA_TERM_SEQ_END_ITERM2_IMAGE   = 48

    CHAFA_TERM_SEQ_ENABLE_SIXEL_SCROLLING  = 49
    CHAFA_TERM_SEQ_DISABLE_SIXEL_SCROLLING = 50

    CHAFA_TERM_SEQ_ENABLE_BOLD = 51

    CHAFA_TERM_SEQ_SET_COLOR_FG_8   = 52
    CHAFA_TERM_SEQ_SET_COLOR_BG_8   = 53
    CHAFA_TERM_SEQ_SET_COLOR_FGBG_8 = 54

    CHAFA_TERM_SEQ_MAX = 55


class ReadOnlySymbolMap():
    def __init__(self):
        # Init chafa
        self._chafa = ctypes.CDLL("libchafa.so")

        # Init map
        self._chafa.chafa_symbol_map_new.restype = ctypes.c_void_p
        self._symbol_map = self._chafa.chafa_symbol_map_new()

    
    def copy(self) -> 'SymbolMap':
        """
        Wrapper for chafa_symbol_map_copy
        """

        # Argtypes
        self._chafa.chafa_symbol_map_copy.argtypes = [
            ctypes.c_void_p
        ]

        self._chafa.chafa_symbol_map_copy.restype = ctypes.c_void_p

        # Get new pointer
        new_pointer = self._chafa.chafa_symbol_map_copy(self._symbol_map)

        # Init symbol map
        symbol_map = SymbolMap()
        symbol_map._symbol_map = new_pointer

        return symbol_map



class SymbolMap(ReadOnlySymbolMap):
    def add_by_tags(self, tags: SymbolTags):
        """
            wrapper for chafa_symbol_map_add_by_tags
        """

        # Set types
        self._chafa.chafa_symbol_map_add_by_tags.argtypes = [
            ctypes.c_void_p, 
            ctypes.c_uint
        ]

        self._chafa.chafa_symbol_map_add_by_tags(self._symbol_map, tags)

    
    def remove_by_tags(self, tags: SymbolTags):
        """
        wrapper for chafa_symbol_map_remove_by_tags
        """

        # Set types
        self._chafa.chafa_symbol_map_remove_by_tags.argtypes = [
            ctypes.c_void_p, 
            ctypes.c_uint
        ]

        self._chafa.chafa_symbol_map_remove_by_tags(self._symbol_map, tags)

    
    def add_by_range(self, first: str, last: str):
        """
        Wrapper for chafa_symbol_map_add_by_range
        """

        # check for chars
        if len(first) != 1:
            raise ValueError("code point 'first' must be of length 1")

        if len(last) != 1:
            raise ValueError("code point 'last' must be of length 1")

        # Set types
        self._chafa.chafa_symbol_map_add_by_range.argtypes = [
            ctypes.c_void_p,
            ctypes.c_wchar,
            ctypes.c_wchar
        ]

        # add tags
        self._chafa.chafa_symbol_map_add_by_range(
            self._symbol_map,
            first,
            last
        )


    def remove_by_range(self, first: str, last: str):
        """
        Wrapper for chafa_symbol_map_remove_by_range
        """

        # check for chars
        if len(first) != 1:
            raise ValueError("code point 'first' must be of length 1")

        if len(last) != 1:
            raise ValueError("code point 'last' must be of length 1")

        # Set types
        self._chafa.chafa_symbol_map_remove_by_range.argtypes = [
            ctypes.c_void_p,
            ctypes.c_wchar,
            ctypes.c_wchar
        ]

        # remove tags
        self._chafa.chafa_symbol_map_remove_by_range(
            self._symbol_map,
            first,
            last
        )

    
    def apply_selectors(self, selectors: str):
        """
        Wrapper for chafa_symbol_map_apply_selectors
        """

        class GError(ctypes.Structure):
            _fields_ = [('domain',   ctypes.c_uint32),
                        ('code',     ctypes.c_int),
                        ('message',  ctypes.c_char_p)]

        # Set types

        self._chafa.chafa_symbol_map_apply_selectors.argtypes = [
            ctypes.c_void_p,
            ctypes.c_char_p,
            ctypes.POINTER(ctypes.POINTER(GError))
        ]

        self._chafa.chafa_symbol_map_apply_selectors.restype = ctypes.c_bool

        selectors = ctypes.c_char_p(bytes(selectors, "utf8"))

        # Init error
        error = ctypes.POINTER(GError)()

        success = self._chafa.chafa_symbol_map_apply_selectors(
            self._symbol_map,
            selectors,
            ctypes.byref(error)
        )
        
        if not success:
            error = error.contents.message.decode()
            raise ValueError(error)

        return success


class CanvasConfig():
    def __init__(self):
        # Init chafa
        self._chafa = ctypes.CDLL("libchafa.so")

        # Init config
        self._chafa.chafa_canvas_config_new.restype = ctypes.c_void_p
        self._canvas_config = self._chafa.chafa_canvas_config_new()

    # === Width & Height property ===

    @property
    def height(self) -> int:
        """
        :type: int

        Sets the config's height in character cells.
        """

        _, height = self.get_geometry()

        return height

    @height.setter
    def height(self, value: int):
        self._set_geometry(self.width, value)


    @property
    def width(self) -> int:
        """
        :type: int

        Sets the config's width in character cells.
        """
        width, _ = self.get_geometry()

        return width

    @width.setter
    def width(self, value: int):
        self._set_geometry(value, self.height)


    # === pixel mode property ===

    @property
    def pixel_mode(self) -> PixelMode:
        """
        :type: PixelMode

        Sets config's stored :py:class:`PixelMode`. 
        This determines how pixel graphics are rendered 
        in the output.
        """

        return self._get_pixel_mode()

    @pixel_mode.setter
    def pixel_mode(self, mode: PixelMode):
        self._set_pixel_mode(mode)


    # === color extractor property ===

    @property
    def color_extractor(self) -> ColorExtractor:
        """
        :type: ColorExtractor

        The config's stored :py:class:`ColorExtractor`. 
        This determines how colours are approximated in 
        character symbol output.
        """
        return self._get_color_extractor()

    @color_extractor.setter
    def color_extractor(self, extractor: ColorExtractor):
        self._set_color_extractor(extractor)


    # === color space property ===

    @property
    def color_space(self) -> ColorSpace:
        """
        :type: ColorSpace

        The config's stored :py:class:`ColorSpace`.
        """
        return self._get_color_space()

    @color_space.setter
    def color_space(self, space: ColorSpace):
        self._set_color_space(space)


    # === canvas mode property ===

    @property
    def canvas_mode(self) -> CanvasMode:
        """
        :type: CanvasMode

        Sets config's stored `CanvasMode`. 
        This determines how colours (and colour control codes) 
        are used in the output.
        """
        return self._get_canvas_mode()

    @canvas_mode.setter
    def canvas_mode(self, mode: CanvasMode):
        self._set_canvas_mode(mode)


    # === preprocessing property ===

    @property
    def preprocessing(self) -> bool:
        """
        :type: bool

        Indicates whether automatic image preprocessing should 
        be enabled. This allows Chafa to boost contrast and 
        saturation in an attempt to improve legibility. 
        """
        return self._get_preprocessing_enabled()

    @preprocessing.setter
    def preprocessing(self, preproc: bool):
        self._set_preprocessing_enabled(preproc)

    
    # === dither grain width & height ===

    @property
    def dither_width(self) -> int:
        """
        :type: int

        Sets config's stored dither grain width in pixels. These 
        values can be 1, 2, 4 or 8. 8 corresponds to the size of 
        an entire character cell. 

        The default is 4 pixels.
        """
        width, _, = self._get_dither_grain_size()
        return width
    
    @dither_width.setter
    def dither_width(self, width: int):
        self._set_dither_grain_size(width, self.dither_height)

    @property
    def dither_height(self) -> int:
        """
        :type: int

        Sets config's stored dither grain width in pixels. These 
        values can be 1, 2, 4 or 8. 8 corresponds to the size of 
        an entire character cell. 

        The default is 4 pixels.

        """
        _, height, = self._get_dither_grain_size()
        return height 
    
    @dither_height.setter
    def dither_height(self, height: int):
        self._set_dither_grain_size(self.dither_width, height)


    # === dither mode property ===

    @property
    def dither_mode(self) -> DitherMode:
        return self._get_dither_mode()

    @dither_mode.setter
    def dither_mode(self, mode: DitherMode):
        self._set_dither_mode(mode)


    # === dither intensity ===

    @property
    def dither_intensity(self) -> float:
        return self._get_dither_intensity()

    @dither_intensity.setter
    def dither_intensity(self, intensity: float):
        if intensity < 0:
            raise ValueError("Dither intensity must be positive.")

        self._set_dither_intensity(intensity)
    

    # === optimizations ===

    @property
    def optimizations(self) -> Tuple:
        """
        :type: Tuple 

        Returns config's optimization flags.
        When enabled, these may produce more 
        compact output at the cost of reduced 
        compatibility and increased CPU use. 

        The flags will be returned as a tuple
        containing all enabled flags.

        Output quality is unaffected.
        """

        out = []

        flags = self._get_optimizations()

        # Check if all optimizations are being used
        if flags == Optimizations.CHAFA_OPTIMIZATION_ALL:
            return (Optimizations.CHAFA_OPTIMIZATION_ALL, )
        
        # Loop to decipher which optimizations are in use
        for optimization in Optimizations:
            # Check if we have reached the end
            if optimization == Optimizations.CHAFA_OPTIMIZATION_NONE:
                break

            # Check if flag is set
            if flags & optimization == optimization:
                out.append(optimization)

        return tuple(map(Optimizations, out))

    @optimizations.setter
    def optimizations(self, optimizations: Tuple):
        # Or all optimizations together

        compounded = 0
        for flag in optimizations:
            compounded |= flag

        self._set_optimizations(compounded)


    # === cell width & height ===

    @property
    def cell_width(self) -> int:
        """
        :type: int

        Sets config's cell width in pixels.
        """

        width, _ = self._get_cell_geometry()
        return width
    
    @cell_width.setter
    def cell_width(self, width: int):
        self._set_cell_geometry(width, self.cell_height)

    @property
    def cell_height(self) -> int:
        """
        :type: int

        Sets config's cell height in pixels.
        """
        _, height = self._get_cell_geometry()
        return height 
    
    @cell_height.setter
    def cell_height(self, height: int):
        self._set_cell_geometry(self.cell_width, height)


    # === Transparency threshold ===

    @property
    def transparency_threshold(self) -> float:
        return self._get_transparency_threshold()

    @transparency_threshold.setter
    def transparency_threshold(self, threshold: float):
        if 1 < threshold or threshold < 0:
            raise ValueError("Transparency threshold must be in range [0,1]")

        self._set_transparency_threshold(threshold)


    # === Work factor ===

    @property
    def work_factor(self) -> float:
        return self._get_work_factor()

    @work_factor.setter
    def work_factor(self, factor: float):
        if 1 < factor or factor < 0:
            raise ValueError("Work factor must be in range [0,1]")

        self._set_work_factor(factor)
        

    # === fg only ===

    @property
    def fg_only(self) -> bool:
        return self._get_fg_only_enabled()

    @fg_only.setter
    def fg_only(self, fg_only: bool):
        self._set_fg_only_enabled(fg_only)
        

    # === fg and bg colors ===

    @property
    def fg_color(self) -> Tuple[int, int, int]:
        # Get the color
        color = self._get_fg_color()

        # Convert to bytes
        bit_length = 3 
        order      = "big"
        
        color = color.to_bytes(bit_length, order)

        return (color[0], color[1], color[2])

    @fg_color.setter
    def fg_color(self, fg_color: Tuple[int, int, int]):

        if len(fg_color) != 3:
            raise ValueError("fg_color must have exactly 3 values")

        if any([255 < col or col < 0 for col in fg_color]):
            raise ValueError("Each value of fg_color must in the range [0,255]")

        # Calculate packed color
        color = fg_color[0] * 16**4 + fg_color[1] * 16 ** 2 + fg_color[2]

        self._set_fg_color(color)


    @property
    def bg_color(self) -> Tuple[int, int, int]:
        # Get the color
        color = self._get_bg_color()

        # Convert to bytes
        bit_length = 3
        order      = "big"
        
        color = color.to_bytes(bit_length, order)

        return (color[0], color[1], color[2])

    @bg_color.setter
    def bg_color(self, bg_color: Tuple[int, int, int]):

        if len(bg_color) != 3:
            raise ValueError("bg_color must have exactly 3 values")

        if any([255 < col or col < 0 for col in bg_color]):
            raise ValueError("Each value of bg_color must in the range [0,255]")

        # Calculate packed color
        color = bg_color[0] * 16**4 + bg_color[1] * 16 ** 2 + bg_color[2]

        self._set_bg_color(color)

    def _set_geometry(self, width: int, height: int):
        """
            Wrapper for chafa_canvas_config_set_geometry
        """

        self._chafa.chafa_canvas_config_set_geometry.argtypes = [
            ctypes.c_void_p, 
            ctypes.c_uint, 
            ctypes.c_uint
        ]

        self._chafa.chafa_canvas_config_set_geometry(
            self._canvas_config, 
            width, 
            height
        )


    def set_geometry(self, width: int, height: int):
        """
            Set the canvas geometry.
        """

        self._set_geometry(width, height)


    def get_geometry(self) -> Tuple[int, int]:
        """
        Get the config's canvas geometry.

        :rtype: Tuple[int, int] of width and height.
        """

        # Init pointers
        width  = ctypes.pointer(ctypes.c_int(-1))
        height = ctypes.pointer(ctypes.c_int(-1))

        # get geometry
        self._chafa.chafa_canvas_config_get_geometry.argtypes = [
            ctypes.c_void_p,
            ctypes.POINTER(ctypes.c_int),
            ctypes.POINTER(ctypes.c_int)
        ]

        self._chafa.chafa_canvas_config_get_geometry(
            self._canvas_config,
            width,
            height
        )

        return width.contents.value, height.contents.value

    def _get_fg_only_enabled(self) -> bool:
        """
            Wrapper for chafa_canvas_config_get_fg_only_enabled
        """

        # Set types
        self._chafa.chafa_canvas_config_get_fg_only_enabled.argtypes = [
            ctypes.c_void_p
        ]

        self._chafa.chafa_canvas_config_get_fg_only_enabled.restype = ctypes.c_bool

        # Get fg_only 
        fg_only = self._chafa.chafa_canvas_config_get_fg_only_enabled(self._canvas_config)

        return fg_only


    def _set_fg_only_enabled(self, fg_only: bool):
        """
            Wrapper for chafa_canvas_config_set_fg_only_enabled
        """

        # Set types
        self._chafa.chafa_canvas_config_set_fg_only_enabled.argtypes = [
            ctypes.c_void_p,
            ctypes.c_bool
        ]

        # Set threshold
        self._chafa.chafa_canvas_config_set_fg_only_enabled(
            self._canvas_config,
            fg_only
        )


    def _get_fg_color(self) -> int:
        """
            Wrapper for chafa_canvas_config_get_fg_color
        """

        # Set types
        self._chafa.chafa_canvas_config_get_fg_color.argtypes = [
            ctypes.c_void_p
        ]

        self._chafa.chafa_canvas_config_get_fg_color.restype = ctypes.c_uint32

        # Get fg_color
        color = self._chafa.chafa_canvas_config_get_fg_color(
            self._canvas_config 
        )

        return color


    def _set_fg_color(self, fg_color: int):
        """
            Wrapper for chafa_canvas_config_set_fg_color
        """

        # Set types
        self._chafa.chafa_canvas_config_set_fg_color.argtypes = [
            ctypes.c_void_p,
            ctypes.c_uint32
        ]

        # Set fg_color
        color = self._chafa.chafa_canvas_config_set_fg_color(
            self._canvas_config,
            fg_color
        )


    def _get_bg_color(self) -> int:
        """
            Wrapper for chafa_canvas_config_get_bg_color
        """

        # Set types
        self._chafa.chafa_canvas_config_get_bg_color.argtypes = [
            ctypes.c_void_p
        ]

        self._chafa.chafa_canvas_config_get_bg_color.restype = ctypes.c_uint32

        # Get bg_color
        color = self._chafa.chafa_canvas_config_get_bg_color(
            self._canvas_config 
        )

        return color


    def _set_bg_color(self, bg_color: int):
        """
            Wrapper for chafa_canvas_config_set_bg_color
        """

        # Set types
        self._chafa.chafa_canvas_config_set_bg_color.argtypes = [
            ctypes.c_void_p,
            ctypes.c_uint32
        ]

        # Set bg_color
        color = self._chafa.chafa_canvas_config_set_bg_color(
            self._canvas_config,
            bg_color
        )


    def _get_transparency_threshold(self) -> float:
        """
            Wrapper for chafa_canvas_config_get_transparency_threshold
        """

        # Set types
        self._chafa.chafa_canvas_config_get_transparency_threshold.argtypes = [
            ctypes.c_void_p
        ]

        self._chafa.chafa_canvas_config_get_transparency_threshold.restype = ctypes.c_float

        # Get threshold
        threshold = self._chafa.chafa_canvas_config_get_transparency_threshold(self._canvas_config)

        return threshold


    def _set_transparency_threshold(self, threshold: float):
        """
            Wrapper for chafa_canvas_config_set_transparency_threshold
        """

        # Set types
        self._chafa.chafa_canvas_config_set_transparency_threshold.argtypes = [
            ctypes.c_void_p,
            ctypes.c_float
        ]

        # Set threshold
        self._chafa.chafa_canvas_config_set_transparency_threshold(
            self._canvas_config,
            threshold
        )


    def _get_work_factor(self) -> float:
        """
            Wrapper for chafa_canvas_config_get_work_factor
        """

        # Set types
        self._chafa.chafa_canvas_config_get_work_factor.argtypes = [
            ctypes.c_void_p
        ]

        self._chafa.chafa_canvas_config_get_work_factor.restype = ctypes.c_float

        # Get factor
        factor = self._chafa.chafa_canvas_config_get_work_factor(self._canvas_config)

        return factor


    def _set_work_factor(self, factor: float):
        """
            Wrapper for chafa_canvas_config_set_work_factor
        """

        # Set types
        self._chafa.chafa_canvas_config_set_work_factor.argtypes = [
            ctypes.c_void_p,
            ctypes.c_float
        ]

        # Set factor
        self._chafa.chafa_canvas_config_set_work_factor(
            self._canvas_config,
            factor
        )


    def _get_pixel_mode(self) -> PixelMode:
        """
            Wrapper for chafa_canvas_config_get_pixel_mode
        """

        # Set types
        self._chafa.chafa_canvas_config_get_pixel_mode.argtypes = [ctypes.c_void_p]
        self._chafa.chafa_canvas_config_get_pixel_mode.restype  = ctypes.c_uint

        # Get mode
        pixel_mode = self._chafa.chafa_canvas_config_get_pixel_mode(self._canvas_config)

        return PixelMode(pixel_mode)

    
    def _set_pixel_mode(self, mode: PixelMode):
        """
            Wrapper for chafa_canvas_config_set_pixel_mode
        """

        # Specify types
        self._chafa.chafa_canvas_config_set_pixel_mode.argtypes = [
            ctypes.c_void_p,
            ctypes.c_uint
        ]

        self._chafa.chafa_canvas_config_set_pixel_mode(self._canvas_config, mode)


    def _set_dither_grain_size(self, width: int, height: int):
        """
            Wrapper for chafa_canvas_config_set_dither_grain_size
        """

        # Specify types
        self._chafa.chafa_canvas_config_set_dither_grain_size.argtypes = [
            ctypes.c_void_p,
            ctypes.c_int,
            ctypes.c_int
        ]

        # Set grain size
        self._chafa.chafa_canvas_config_set_dither_grain_size(self._canvas_config, width, height)
        

    def _get_dither_grain_size(self) -> Tuple[int, int]:
        """
            Wrapper for chafa_canvas_config_get_dither_grain_size
        """

        # Specify types
        self._chafa.chafa_canvas_config_get_dither_grain_size.argtypes = [
            ctypes.c_void_p,
            ctypes.POINTER(ctypes.c_int),
            ctypes.POINTER(ctypes.c_int)
        ]

        width_out  = ctypes.pointer(ctypes.c_int(0))
        height_out = ctypes.pointer(ctypes.c_int(0))

        # Set grain size
        self._chafa.chafa_canvas_config_get_dither_grain_size(self._canvas_config, width_out, height_out)

        return (width_out.contents.value, height_out.contents.value)



    def _set_cell_geometry(self, width: int, height: int):
        """
            Wrapper for chafa_canvas_config_set_cell_geometry
        """

        # Specify types
        self._chafa.chafa_canvas_config_set_cell_geometry.argtypes = [
            ctypes.c_void_p,
            ctypes.c_int,
            ctypes.c_int
        ]

        # Set grain size
        self._chafa.chafa_canvas_config_set_cell_geometry(self._canvas_config, width, height)
        

    def _get_cell_geometry(self) -> Tuple[int, int]:
        """
            Wrapper for chafa_canvas_config_get_dither_grain_size
        """

        # Specify types
        self._chafa.chafa_canvas_config_get_cell_geometry.argtypes = [
            ctypes.c_void_p,
            ctypes.POINTER(ctypes.c_int),
            ctypes.POINTER(ctypes.c_int)
        ]

        width_out  = ctypes.pointer(ctypes.c_int(0))
        height_out = ctypes.pointer(ctypes.c_int(0))

        # Set grain size
        self._chafa.chafa_canvas_config_get_cell_geometry(self._canvas_config, width_out, height_out)

        return (width_out.contents.value, height_out.contents.value)


    def _get_dither_mode(self) -> DitherMode:
        """
            Wrapper for chafa_canvas_config_get_cnavas_mode
        """

        # Specify types
        self._chafa.chafa_canvas_config_get_dither_mode.argtypes = [ctypes.c_void_p]
        self._chafa.chafa_canvas_config_get_dither_mode.restype  = ctypes.c_uint

        # Get mode
        mode = self._chafa.chafa_canvas_config_get_dither_mode(self._canvas_config)

        return DitherMode(mode)

    
    def _set_dither_mode(self, mode: DitherMode):
        """
            wrapper for chafa_canvas_config_set_dither_mode
        """

        # Specify types
        self._chafa.chafa_canvas_config_set_dither_mode.argtypes = [
            ctypes.c_void_p,
            ctypes.c_uint
        ]

        self._chafa.chafa_canvas_config_set_dither_mode(self._canvas_config, mode)
        

    def _get_dither_intensity(self) -> float:
        """
            Wrapper for chafa_canvas_config_get_dither_intensity
        """

        # Specify types
        self._chafa.chafa_canvas_config_get_dither_intensity.argtypes = [
            ctypes.c_void_p
        ]

        self._chafa.chafa_canvas_config_get_dither_intensity.restype = ctypes.c_float

        # Get intensity
        intensity = self._chafa.chafa_canvas_config_get_dither_intensity(self._canvas_config)

        return intensity


    def _set_dither_intensity(self, intensity: float):
        """
        Wrapper for chafa_canvas_config_set_dither_intensity
        """

        # Specify types
        self._chafa.chafa_canvas_config_set_dither_intensity.argtypes = [
            ctypes.c_void_p,
            ctypes.c_float
        ]

        # Set intensity
        self._chafa.chafa_canvas_config_set_dither_intensity(
            self._canvas_config,
            intensity
        )


    def _get_canvas_mode(self) -> CanvasMode:
        """
            Wrapper for chafa_canvas_config_get_cnavas_mode
        """

        # Specify types
        self._chafa.chafa_canvas_config_get_canvas_mode.argtypes = [ctypes.c_void_p]
        self._chafa.chafa_canvas_config_get_canvas_mode.restype  = ctypes.c_uint

        # Get mode
        mode = self._chafa.chafa_canvas_config_get_canvas_mode(self._canvas_config)

        return CanvasMode(mode)

    
    def _set_canvas_mode(self, mode: CanvasMode):
        """
            wrapper for chafa_canvas_config_set_canvas_mode
        """

        # Specify types
        self._chafa.chafa_canvas_config_set_canvas_mode.argtypes = [
            ctypes.c_void_p,
            ctypes.c_uint
        ]

        self._chafa.chafa_canvas_config_set_canvas_mode(self._canvas_config, mode)


    def _get_color_extractor(self) -> ColorExtractor:
        """
            Wrapper for chafa_canvas_config_get_color_extractor
        """

        # Set types
        self._chafa.chafa_canvas_config_get_color_extractor.argtypes = [ctypes.c_void_p]
        self._chafa.chafa_canvas_config_get_color_extractor.restype  = ctypes.c_uint

        # Get extractor
        extractor = self._chafa.chafa_canvas_config_get_color_extractor(self._canvas_config)

        return ColorExtractor(extractor)

    
    def _set_color_extractor(self, extractor: ColorExtractor):
        """
            Wrapper for chafa_canvas_config_set_color_extractor
        """

        # Specify types
        self._chafa.chafa_canvas_config_set_color_extractor.argtypes = [
            ctypes.c_void_p,
            ctypes.c_uint
        ]

        self._chafa.chafa_canvas_config_set_color_extractor(self._canvas_config, extractor)


    def _get_color_space(self) -> ColorSpace:
        """
            Wrapper for chafa_canvas_config_get_color_space
        """

        # Set types
        self._chafa.chafa_canvas_config_get_color_space.argtypes = [ctypes.c_void_p]
        self._chafa.chafa_canvas_config_get_color_space.restype  = ctypes.c_uint

        # Get space
        space = self._chafa.chafa_canvas_config_get_color_space(self._canvas_config)

        return ColorSpace(space)

    
    def _set_color_space(self, space: ColorSpace):
        """
            Wrapper for chafa_canvas_config_set_color_space
        """

        # Specify types
        self._chafa.chafa_canvas_config_set_color_space.argtypes = [
            ctypes.c_void_p,
            ctypes.c_uint
        ]

        self._chafa.chafa_canvas_config_set_color_space(self._canvas_config, space)


    def _get_preprocessing_enabled(self) -> bool:
        """
            Wrapper for chafa_canvas_config_get_preprocessing_enabled
        """

        # Set types
        self._chafa.chafa_canvas_config_get_preprocessing_enabled.argtypes = [ctypes.c_void_p]
        self._chafa.chafa_canvas_config_get_preprocessing_enabled.restype  = ctypes.c_bool

        # Get preprocessing value 
        preprocessing = self._chafa.chafa_canvas_config_get_preprocessing_enabled(self._canvas_config)

        return preprocessing 

    
    def _set_preprocessing_enabled(self, preproc: bool):
        """
            Wrapper for chafa_canvas_config_set_preprocessing_enabled
        """

        # Specify types
        self._chafa.chafa_canvas_config_set_preprocessing_enabled.argtypes = [
            ctypes.c_void_p,
            ctypes.c_bool
        ]

        self._chafa.chafa_canvas_config_set_preprocessing_enabled(self._canvas_config, preproc)


    def _get_optimizations(self) -> int:
        """
            Wrapper for chafa_canvas_config_get_optimizations
        """

        # Specify types
        self._chafa.chafa_canvas_config_get_optimizations.argtypes = [
            ctypes.c_void_p
        ]

        self._chafa.chafa_canvas_config_get_optimizations.restype = ctypes.c_uint

        return self._chafa.chafa_canvas_config_get_optimizations(self._canvas_config)

    def _set_optimizations(self, optimizations: int):
        """
            Wrapper for chafa_canvas_config_set_optimizations
        """

        # Specify types
        self._chafa.chafa_canvas_config_set_optimizations.argtypes = [
            ctypes.c_void_p,
            ctypes.c_uint
        ]

        # Set optimizations
        self._chafa.chafa_canvas_config_set_optimizations(
            self._canvas_config,
            optimizations
        )


    def set_symbol_map(self, symbol_map: SymbolMap):
        """
            Assigns a copy of symbol_map to config.

            :param SymbolMap symbol_map: The symbol_map.
        """

        # Specify types
        self._chafa.chafa_canvas_config_set_symbol_map.argtypes = [
            ctypes.c_void_p,
            ctypes.c_void_p
        ]

        self._chafa.chafa_canvas_config_set_symbol_map(self._canvas_config, symbol_map._symbol_map)


    def set_fill_symbol_map(self, fill_symbol_map: SymbolMap):
        """
            Assigns a copy of fill_symbol_map to config.

            Fill symbols are assigned according to their overall foreground to background coverage, disregarding shape. ???

            :param SymbolMap fill_symbol_map: The fill symbol map.
        """

        # Specify types
        self._chafa.chafa_canvas_config_set_fill_symbol_map.argtypes = [
            ctypes.c_void_p,
            ctypes.c_void_p
        ]

        self._chafa.chafa_canvas_config_set_fill_symbol_map(self._canvas_config, fill_symbol_map._symbol_map)


    def calc_canvas_geometry(self, src_width: int, src_height: int, font_ratio: float, zoom: bool=False, stretch: bool=False):
        """
        Calculates an optimal geometry for a :py:class:`Canvas` given 
        the width and height of an input image, font ratio, zoom and 
        stretch preferences. This will then set the config's width and 
        height to the calculated values.

        :param int src_width: Width of the input image in pixels.
        :param int src_height: Height of the input image in pixels.
        :param float font_ratio: The font's width divided by its height.
        :param bool zoom: Upscale the image to fit the canvas.
        :param bool stretch: Ignore the aspect ratio of source.

        :raises ValueError: if src_width or src_height are <= 0
        """

        if src_width <= 0:
            raise ValueError("src_width must be greater than 0")

        if src_height <= 0:
            raise ValueError("src_height must be greater than 0")

        self._chafa.chafa_calc_canvas_geometry.argtypes = [
            ctypes.c_uint,
            ctypes.c_uint,
            ctypes.POINTER(ctypes.c_uint),
            ctypes.POINTER(ctypes.c_uint),
            ctypes.c_float,
            ctypes.c_bool,
            ctypes.c_bool
        ]

        new_width  = ctypes.pointer(ctypes.c_uint(self.width))
        new_height = ctypes.pointer(ctypes.c_uint(self.height))
        
        self._chafa.chafa_calc_canvas_geometry(
            src_width, src_height,
            new_width, new_height,
            font_ratio,
            zoom,
            stretch
        )

        self.width  = new_width. contents.value
        self.height = new_height.contents.value

    def copy(self) -> 'CanvasConfig':
        """
        Creates a new :py:class:`CanvasConfig` that is a copy of this config.

        :rtype: CanvasConfig
        """

        # define types
        self._chafa.chafa_canvas_config_copy.argtypes = [
            ctypes.c_void_p
        ]

        self._chafa.chafa_canvas_config_copy.restype = ctypes.c_void_p

        # Init new config
        new_config = CanvasConfig()

        # Get new pointer
        config_copy = self._chafa.chafa_canvas_config_copy(self._canvas_config)

        new_config._canvas_config = config_copy

        return new_config


class TermDb():
    def __init__(self, no_defaults: bool=False):
        # Init chafa
        self._chafa = ctypes.CDLL("libchafa.so")

        # Init term db
        if no_defaults:
            self._chafa.chafa_term_db_new.restype = ctypes.c_void_p
            self._term_db = self._chafa.chafa_term_db_new()
        else:
            self._chafa.chafa_term_db_get_default.restype = ctypes.c_void_p
            self._term_db = self._chafa.chafa_term_db_get_default()

    def detect(self):
        # Init glib
        glib = ctypes.CDLL("libglib-2.0.so")
        glib.g_get_environ.restype = ctypes.c_void_p

        # Get environment
        environment = glib.g_get_environ()

        self._chafa.chafa_term_db_detect.restype  = ctypes.c_void_p
        self._chafa.chafa_term_db_detect.argtypes = [
            ctypes.c_void_p,
            ctypes.c_void_p
        ]

        new_term_info = self._chafa.chafa_term_db_detect(
            self._term_db,
            environment
        )

        term_info = TermInfo()
        term_info._term_info = new_term_info

        return term_info




class TermInfo():
    def __init__(self):
        # Init chafa
        self._chafa = ctypes.CDLL("libchafa.so")

        # Init term_info
        self._chafa.chafa_term_info_new.restype = ctypes.c_void_p

        self._term_info = self._chafa.chafa_term_info_new()


    @dataclass
    class TerminalCapabilities:
        canvas_mode: CanvasMode
        pixel_mode: PixelMode


    def _supplement(self, source: ctypes.c_void_p):
        """
            Wrapper for chafa_term_info_supplement
        """

        self._chafa.chafa_term_info_supplement.argtypes = [
            ctypes.c_void_p,
            ctypes.c_void_p
        ]

        self._chafa.chafa_term_info_supplement(self._term_info, source)


    def have_seq(self, seq: TermSeq) -> bool:
        """
            Wrapper for chafa_term_info_have_seq
        """

        # Set types
        self._chafa.chafa_term_info_have_seq.argtypes = [
            ctypes.c_void_p, 
            ctypes.c_int
        ]
        
        self._chafa.chafa_term_info_have_seq.restype = ctypes.c_bool

        # Check for sequence
        return self._chafa.chafa_term_info_have_seq(self._term_info, seq)


    def detect_capabilities(self) -> TerminalCapabilities:
        """
            A function that tries to detect the capabilities of the
            terminal and return the appropriate canvas and pixel modes
        """
        # === Canvas mode ===

        color_direct = self.have_seq(TermSeq.CHAFA_TERM_SEQ_SET_COLOR_FGBG_DIRECT) \
            and        self.have_seq(TermSeq.CHAFA_TERM_SEQ_SET_COLOR_FG_DIRECT) \
            and        self.have_seq(TermSeq.CHAFA_TERM_SEQ_SET_COLOR_BG_DIRECT)

        color_256    = self.have_seq(TermSeq.CHAFA_TERM_SEQ_SET_COLOR_FGBG_256) \
            and        self.have_seq(TermSeq.CHAFA_TERM_SEQ_SET_COLOR_FG_256) \
            and        self.have_seq(TermSeq.CHAFA_TERM_SEQ_SET_COLOR_BG_256)

        color_16     = self.have_seq(TermSeq.CHAFA_TERM_SEQ_SET_COLOR_FGBG_16) \
            and        self.have_seq(TermSeq.CHAFA_TERM_SEQ_SET_COLOR_FG_16) \
            and        self.have_seq(TermSeq.CHAFA_TERM_SEQ_SET_COLOR_BG_16)

        color_2      = self.have_seq(TermSeq.CHAFA_TERM_SEQ_INVERT_COLORS) \
            and        self.have_seq(TermSeq.CHAFA_TERM_SEQ_RESET_ATTRIBUTES)

        if color_direct:
            canvas_mode = CanvasMode.CHAFA_CANVAS_MODE_TRUECOLOR

        elif color_256:
            canvas_mode = CanvasMode.CHAFA_CANVAS_MODE_INDEXED_240

        elif color_16:
            canvas_mode = CanvasMode.CHAFA_CANVAS_MODE_INDEXED_16

        elif color_2:
            canvas_mode = CanvasMode.CHAFA_CANVAS_MODE_FGBG_BGFG

        else:
            canvas_mode = CanvasMode.CHAFA_CANVAS_MODE_FGBG

        # === Pixel mode ===

        # Check for sixels
        sixel_capable = self.have_seq(TermSeq.CHAFA_TERM_SEQ_BEGIN_SIXELS) \
            and         self.have_seq(TermSeq.CHAFA_TERM_SEQ_END_SIXELS)

        # Check for kitty
        kitty_capable = self.have_seq(TermSeq.CHAFA_TERM_SEQ_BEGIN_KITTY_IMMEDIATE_IMAGE_V1)

        if kitty_capable:
            pixel_mode = PixelMode.CHAFA_PIXEL_MODE_KITTY

        elif sixel_capable:
            pixel_mode = PixelMode.CHAFA_PIXEL_MODE_SIXELS

        else:
            pixel_mode = PixelMode.CHAFA_PIXEL_MODE_SYMBOLS

        # Init capabilities
        terminal_capabilities = self.TerminalCapabilities(canvas_mode, pixel_mode)

        return terminal_capabilities

    
class Canvas:
    def __init__(self, config: CanvasConfig, term_info: TermInfo=None):
        # Init chafa
        self._chafa = ctypes.CDLL("libchafa.so")

        # Init config
        self._config = config

        # Check for term info
        if term_info is None:
            term_db = TermDb()
            self._term_info = term_db.detect()

        else:
            self._term_info = term_info 

        # Init canvas
        self._chafa.chafa_canvas_new.argtypes = [ctypes.c_void_p]
        self._chafa.chafa_canvas_new.restype  =  ctypes.c_void_p

        self._canvas = self._chafa.chafa_canvas_new(config._canvas_config)

    def _canvas_slice(self, y_slice=slice(None), x_slice=slice(None), axis=0, y=None, x=None):
        # Get slice of rows
        # Check slice component types

        # Define the hard stop
        hard_stop = (self._config.height, self._config.width)
        hard_stop = hard_stop[axis]

        which_slice = (y_slice, x_slice)[axis]
        
        # Evaluate defaults
        start = which_slice.start or 0
        stop  = which_slice.stop  or hard_stop
        step  = which_slice.step  or 1

        # Check 0 step
        if step == 0:
            raise ValueError("Slice step cannot be zero.")
        
        # Evaluate negative start and stop
        if start < 0:
            start = hard_stop + start
        
        if stop < 0:
            stop = hard_stop + stop

        # Evaluators for when to stop the while loop
        def positive_stop_evaluator(index):
            return index < min(hard_stop, stop)

        def negative_stop_evaluator(index):
            return index >= 0

        stop_evaluator = positive_stop_evaluator

        # Negative step means we reverse start and stop
        if step < 0:
            aux   = start
            start = stop - 1
            stop  = aux

            stop_evaluator = negative_stop_evaluator

        if any([not isinstance(val, int) for val in (start, stop, step)]):
            raise TypeError("Slice indices must be integers or None.")

        # We are slicing over y
        if axis == 0:
            y = start

            while stop_evaluator(y):
                yield self[y, x_slice] if x is None else self[y, x]
                y += step

            return

        # We are slicing over x
        if axis == 1:
            x = start

            while stop_evaluator(x):
                yield self[y, x]
                x += step

            return

    def __getitem__(self, pos):

        if isinstance(pos, int):
            return self[pos, :]

        
        if isinstance(pos, slice):
            return self._canvas_slice(y_slice=pos)

        if not isinstance(pos, tuple):
            raise TypeError(f"Indices of invalid type. Got {type(pos)}")

        # None of the above means tuple

        # Check for size
        if len(pos) > 2:
            raise IndexError(f"Too many indices for Canvas. Canvas is 2-dimensional, but got {len(pos)} indices.")
        
        # Empty tuple should return all rows
        if len(pos) == 0:
            return self[:]
        
        # Exact coordinates
        if isinstance(pos[0], int) and isinstance(pos[1], int):
            return CanvasInspector(self, *pos)
        
        # Slice of rows and columns
        if isinstance(pos[0], slice) and isinstance(pos[1], slice):
            return self._canvas_slice(y_slice=pos[0], x_slice=pos[1])
        
        # Slice of rows with exact x coordinate
        if isinstance(pos[0], slice):
            return self._canvas_slice(y_slice=pos[0], x=pos[1])
        
        # Slice of columns with exact y coordinate
        if isinstance(pos[1], slice):
            return self._canvas_slice(x_slice=pos[1], axis=1, y=pos[0])

        return


    def _get_char_at(self, x:int, y:int) -> str:
        """
        Wrapper for chafa_canvas_get_char_at
        """

        # Define types
        self._chafa.chafa_canvas_get_char_at.argtypes = [
            ctypes.c_void_p,
            ctypes.c_int,
            ctypes.c_int
        ]

        self._chafa.chafa_canvas_get_char_at.restype = ctypes.c_wchar

        # Get char
        char = self._chafa.chafa_canvas_get_char_at(
            self._canvas,
            x, y
        )

        return char


    def _set_char_at(self, x:int, y:int, char: str):
        """
        Wrapper for chafa_canvas_set_char_at
        """

        # Define types
        self._chafa.chafa_canvas_set_char_at.argtypes = [
            ctypes.c_void_p,
            ctypes.c_int,
            ctypes.c_int,
            ctypes.c_wchar
        ]

        # Set char
        self._chafa.chafa_canvas_set_char_at(
            self._canvas,
            x, y,
            char
        )


    def _get_colors_at(self, x: int, y:int) -> Tuple[int, int]:
        """
        Wrapper for chafa_canvas_get_colors_at
        """

        # Set types
        self._chafa.chafa_canvas_get_colors_at.argtypes = [
            ctypes.c_void_p,
            ctypes.c_int,
            ctypes.c_int,
            ctypes.POINTER(ctypes.c_int),
            ctypes.POINTER(ctypes.c_int)
        ]

        # Define storage
        bg_color = ctypes.pointer(ctypes.c_int(0))
        fg_color = ctypes.pointer(ctypes.c_int(0))

        # Get colors
        self._chafa.chafa_canvas_get_colors_at(
            self._canvas,
            x, y,
            fg_color,
            bg_color
        )

        return fg_color.contents.value, bg_color.contents.value


    def _set_colors_at(self, x:int, y: int, fg: int, bg: int):
        """
        Wrapper for chafa_canvas_set_colors_at
        """

        # Set types
        self._chafa.chafa_canvas_set_colors_at.argtypes = [
            ctypes.c_void_p,
            ctypes.c_int,
            ctypes.c_int,
            ctypes.c_int,
            ctypes.c_int
        ]

        # Set colors
        self._chafa.chafa_canvas_set_colors_at(
            self._canvas,
            x, y,
            fg,
            bg
        )

    def draw_all_pixels(self, src_pixel_type: PixelType, src_pixels: Sequence, src_width: int, src_height: int, src_rowstride: int):
        """
            Wrapper for chafa_canvas_draw_all_pixels
        """
        
        # Specify types
        self._chafa.chafa_canvas_draw_all_pixels.argtypes = [
            ctypes.c_void_p,
            ctypes.c_uint,
            ctypes.POINTER(ctypes.c_uint8),
            ctypes.c_uint,
            ctypes.c_uint,
            ctypes.c_uint
        ]

        # Init array
        # pixels = (ctypes.c_uint8 * len(src_pixels))()
        # pixels[:] = src_pixels

        # Draw pixels
        self._chafa.chafa_canvas_draw_all_pixels(
            self._canvas,
            src_pixel_type,
            src_pixels,
            src_width,
            src_height,
            src_rowstride,
        )


    def print(self):
        """
            Wrapper for chafa_canvas_print
        """

        class GString(ctypes.Structure):
            _fields_ = [('str',         ctypes.c_char_p),
                        ('len',           ctypes.c_uint),
                        ('allocated_len', ctypes.c_uint)]

        self._chafa.chafa_canvas_print.argtypes = [
            ctypes.c_void_p, 
            ctypes.c_void_p
        ]

        self._chafa.chafa_canvas_print.restype  = ctypes.c_void_p

        output = self._chafa.chafa_canvas_print(self._canvas, self._term_info._term_info)
        output = GString.from_address(output)

        return output.str



class CanvasInspector:
    def __init__(self, canvas: Canvas, y: int, x: int):
        # Get the configured height and width of the canvas
        width  = canvas._config.width
        height = canvas._config.height

        # Check if x and y are within bounds

        if x >= width or y >= height:
            raise ValueError(
                f"Coordinates ({x},{y}) are out of bounds for canvas with dimensions {width}x{height}."
            )
        
        self._canvas = canvas
        self._x = x
        self._y = y


    # === FG COLOR ===

    @property
    def fg_color(self) -> Union[Tuple[int, int, int], None]:
        # Get the color at pixel
        color = self._canvas._get_colors_at(self.x, self.y)[0]

        # Return None for transparency
        if color == -1:
            return None

        # Convert to bytes
        bit_length = 3 
        order      = "big"
        
        color = color.to_bytes(bit_length, order)

        return (color[0], color[1], color[2])
    
    @fg_color.setter
    def fg_color(self, color: Tuple[int, int, int]):

        # Remove foreground if we get none
        if color is None:
            self.remove_foreground()

        if len(color) != 3:
            raise ValueError("fg_color must have exactly 3 values")

        if any([255 < col or col < 0 for col in color]):
            raise ValueError("Each value of fg_color must in the range [0,255]")

        # Convert to int
        color = color[0] * 16**4 + color[1] * 16 ** 2 + color[2]

        bg_color = self.bg_color

        if bg_color is None:
            bg_color = -1

        else:
            bg_color = bg_color[0] * 16**4 + bg_color[1] * 16 ** 2 + bg_color[2]

        self._canvas._set_colors_at(self.x, self.y, color, bg_color)


    # === BG COLOR ===
    
    @property
    def bg_color(self) -> Union[Tuple[int, int, int], None]:
        # Get the color at pixel
        color = self._canvas._get_colors_at(self.x, self.y)[1]

        if color == -1:
            return None

        # Convert to bytes
        bit_length = 3 
        order      = "big"
        
        color = color.to_bytes(bit_length, order)

        return (color[0], color[1], color[2])
    
    @bg_color.setter
    def bg_color(self, color: Tuple[int, int, int]):

        # Remove background if we get none
        if color is None:
            self.remove_background()

        if len(color) != 3:
            raise ValueError("bg_color must have exactly 3 values")

        if any([255 < col or col < 0 for col in color]):
            raise ValueError("Each value of bg_color must in the range [0,255]")

        # Convert to int
        color = color[0] * 16**4 + color[1] * 16 ** 2 + color[2]

        fg_color = self.fg_color

        if fg_color is None:
            fg_color = -1

        else:
            fg_color = fg_color[0] * 16**4 + fg_color[1] * 16 ** 2 + fg_color[2]

        self._canvas._set_colors_at(self.x, self.y, fg_color, color)


    # === CHAR ===

    @property
    def char(self):
        return self._canvas._get_char_at(self.x, self.y)

    @char.setter
    def char(self, char: str):
        self._canvas._set_char_at(self.x, self.y, char)


    # === Coordinates ===

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value: int):
        width = self._canvas._config.width

        if value >= width:
            raise ValueError(
                f"x-coordinate {value} is out of bounds for canvas with width {width}."
            )
        
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value: int):
        height = self._canvas._config.height

        if value >= height:
            raise ValueError(
                f"y-coordinate {value} is out of bounds for canvas with width {height}."
            )
        
        self._y = value

    
    def remove_background(self):
        """
        A function that makes background of pixel transparent
        """

        fg_color = self.fg_color

        if fg_color is None:
            fg_color = -1

        else:
            fg_color = fg_color[0] * 16**4 + fg_color[1] * 16 ** 2 + fg_color[2]

        self._canvas._set_colors_at(self.x, self.y, fg_color, -1)

    def remove_foreground(self):
        """
        A function that makes foreground of pixel transparent
        """

        bg_color = self.bg_color

        if bg_color is None:
            bg_color = -1

        else:
            bg_color = bg_color[0] * 16**4 + bg_color[1] * 16 ** 2 + bg_color[2]

        self._canvas._set_colors_at(self.x, self.y, -1, bg_color)
