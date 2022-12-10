import ctypes
from dataclasses import dataclass
from typing import Tuple, Sequence
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
# === PIXEL TYPE
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


class SymbolMap():
    def __init__(self):
        # Init chafa
        self._chafa = ctypes.CDLL("libchafa.so")

        # Init map
        self._chafa.chafa_symbol_map_new.restype = ctypes.c_void_p
        self._symbol_map = self._chafa.chafa_symbol_map_new()


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
        _, height = self.get_geometry()

        return height

    @height.setter
    def height(self, value: int):
        self._set_geometry(self.width, value)


    @property
    def width(self) -> int:
        width, _ = self.get_geometry()

        return width

    @width.setter
    def width(self, value: int):
        self._set_geometry(value, self.height)


    # === pixel mode property ===

    @property
    def pixel_mode(self) -> PixelMode:
        return self._get_pixel_mode()

    @pixel_mode.setter
    def pixel_mode(self, mode: PixelMode):
        self._set_pixel_mode(mode)


    # === color extractor property ===

    @property
    def color_extractor(self) -> ColorExtractor:
        return self._get_color_extractor()

    @color_extractor.setter
    def color_extractor(self, extractor: ColorExtractor):
        self._set_color_extractor(extractor)


    # === color space property ===

    @property
    def color_space(self) -> ColorSpace:
        return self._get_color_space()

    @color_space.setter
    def color_space(self, space: ColorSpace):
        self._set_color_space(space)


    # === canvas mode property ===

    @property
    def canvas_mode(self) -> CanvasMode:
        return self._get_canvas_mode()

    @canvas_mode.setter
    def canvas_mode(self, mode: CanvasMode):
        self._set_canvas_mode(mode)


    # === dither grain width & height ===

    @property
    def dither_width(self) -> int:
        width, _, = self._get_dither_grain_size()
        return width
    
    @dither_width.setter
    def dither_width(self, width: int):
        self._set_dither_grain_size(width, self.dither_height)

    @property
    def dither_height(self) -> int:
        _, height, = self._get_dither_grain_size()
        return height 
    
    @dither_height.setter
    def dither_height(self, height: int):
        self._set_dither_grain_size(self.dither_width, height)



    # === cell width & height ===

    @property
    def cell_width(self) -> int:
        width, _ = self._get_cell_geometry()
        return width
    
    @cell_width.setter
    def cell_width(self, width: int):
        self._set_cell_geometry(width, self.cell_height)

    @property
    def cell_height(self) -> int:
        _, height = self._get_cell_geometry()
        return height 
    
    @cell_height.setter
    def cell_height(self, height: int):
        self._set_cell_geometry(self.cell_width, height)
        

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
            Get the canvas geometry.

            Returns: (width, height)
            
            Wrapper for chafa_canvas_config_get_geometry
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
    def set_symbol_map(self, symbol_map: SymbolMap):
        """
            Wrapper for chafa_canvas_config_set_symbol_map
        """

        # Specify types
        self._chafa.chafa_canvas_config_set_symbol_map.argtypes = [
            ctypes.c_void_p,
            ctypes.c_void_p
        ]

        self._chafa.chafa_canvas_config_set_symbol_map(self._canvas_config, symbol_map._symbol_map)


    def calc_canvas_geometry(self, src_width: int, src_height: int, font_ratio: float, zoom: bool=False, stretch: bool=False):
        """
            Automatically calculates the optimal geometry for a canvas
                - src_width:  width of source image (>0)
                - src_height: height of source image (>0)
                - font_ratio: font width / font height
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
        sixel_capable = self._have_seq(TermSeq.CHAFA_TERM_SEQ_BEGIN_SIXELS) \
            and         self._have_seq(TermSeq.CHAFA_TERM_SEQ_END_SIXELS)

        # Check for kitty
        kitty_capable = self._have_seq(TermSeq.CHAFA_TERM_SEQ_BEGIN_KITTY_IMMEDIATE_IMAGE_V1)

        if kitty_capable:
            pixel_mode = PixelMode.CHAFA_PIXEL_MODE_KITTY

        elif sixel_capable:
            pixel_mode = PixelMode.CHAFA_PIXEL_MODE_SIXELS

        else:
            pixel_mode = PixelMode.CHAFA_PIXEL_MODE_SYMBOLS

        # Init capabilities
        terminal_capabilities = self.TerminalCapabilities(canvas_mode, pixel_mode)

        return terminal_capabilities

    
class Canvas():
    def __init__(self, config: CanvasConfig, term_info: TermInfo=None):
        # Init chafa
        self._chafa = ctypes.CDLL("libchafa.so")

        # Init config
        self.config = config

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
        pixels = (ctypes.c_uint8 * len(src_pixels)).from_buffer(src_pixels)

        # Draw pixels
        self._chafa.chafa_canvas_draw_all_pixels(
            self._canvas,
            src_pixel_type,
            pixels,
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


