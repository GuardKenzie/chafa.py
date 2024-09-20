from __future__ import annotations
import ctypes
from typing import Tuple, Iterable

from .libraries import _Chafa
from .symbol_map import ReadOnlySymbolMap, SymbolMap
from .enums import *

def packed_8bit_to_tuple(color: int) -> Tuple[int, int, int]:
    """
    A static method that takes an integer representing a packed
    8bit RGB value and converts it into a tuple (R,G,B)

    :rtype: tuple[int, int, int]
    """

    # Convert to bytes
    bit_length = 3
    order      = "big"
    
    color = color.to_bytes(bit_length, order)

    return (color[0], color[1], color[2])

def tuple_to_packed_8bit(color_tuple: Tuple[int, int, int]) -> int:
    """
    A static method that takes a tuple (R,G,B) representing a color
    and converts it into a packed 8bit RGB value represented by an
    integer.

    :rtype: tuple[int, int, int]
    """

    offset = 1
    color  = 0

    # Convert color to packed bytes
    for col in color_tuple[::-1]:
        col = int(col)

        if 255 < col or col < 0:
            raise ValueError("Each value of color must be in the range [0,255]")
        
        color  += offset * col
        offset *= 16**2

    return color


class ReadOnlyCanvasConfig:
    def __init__(self):
        # Init config
        _Chafa.chafa_canvas_config_new.restype = ctypes.c_void_p
        self._canvas_config = _Chafa.chafa_canvas_config_new()


    # === Width & Height property ===

    @property
    def height(self) -> int:
        """
        :type: int

        Sets the config's height in character cells.
        """

        _, height = self.get_geometry()

        return height

    @property
    def width(self) -> int:
        """
        :type: int

        Sets the config's width in character cells.
        """
        width, _ = self.get_geometry()

        return width


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


    # === color extractor property ===

    @property
    def color_extractor(self) -> ColorExtractor:
        """
        :type: ColorExtractor

        The config's stored :py:class:`ColorExtractor`. 
        This determines how colours are approximated in 
        character symbol output. e.g. 
        :py:attr:`PixelMode.CHAFA_PIXEL_MODE_SYMBOLS`.
        """
        return self._get_color_extractor()

    
    # === color space property ===

    @property
    def color_space(self) -> ColorSpace:
        """
        :type: ColorSpace

        The config's stored :py:class:`ColorSpace`.
        """
        return self._get_color_space()


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

    
    # === dither mode property ===

    @property
    def dither_mode(self) -> DitherMode:
        """
        :type: DitherMode

        The config's stored :py:class:`DitherMode`.
        """
        return self._get_dither_mode()


    # === dither intensity ===

    @property
    def dither_intensity(self) -> float:
        """
        :type: float

        Returns the relative intensity of the dithering 
        pattern applied during image conversion. 1.0 
        is the default, corresponding to a moderate intensity.
        """
        return self._get_dither_intensity()


    # === optimizations ===

    @property
    def optimizations(self) -> Tuple[Optimizations, ...]:
        """
        :type: Tuple[Optimizations, ...] 

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


    # === cell width & height ===

    @property
    def cell_width(self) -> int:
        """
        :type: int

        Sets config's cell width in pixels.
        """

        width, _ = self._get_cell_geometry()
        return width


    @property
    def cell_height(self) -> int:
        """
        :type: int

        Sets config's cell height in pixels.
        """
        _, height = self._get_cell_geometry()
        return height 


    # === Transparency threshold ===

    @property
    def transparency_threshold(self) -> float:
        """
        :type: float

        The threshold above which full transparency will be used.
        """
        return self._get_transparency_threshold()


    # === Work factor ===

    @property
    def work_factor(self) -> float:
        """
        :type: float

        Gets the work/quality tradeoff factor. A higher 
        value means more time and memory will be spent 
        towards a higher quality output.
        """
        return self._get_work_factor()

    
    # === fg only ===

    @property
    def fg_only(self) -> bool:
        """
        :type: bool

        Queries whether to use foreground colors only, 
        leaving the background unmodified in the canvas 
        output.

        When this is set, the canvas will emit escape codes 
        to set the foreground color only.
        
        .. note::

            This is relevant only when the :py:attr:`pixel_mode` 
            is set to :py:attr:`PixelMode.CHAFA_PIXEL_MODE_SYMBOLS`.
        """
        return self._get_fg_only_enabled()


    # === fg and bg colors ===

    @property
    def fg_color(self) -> Tuple[int, int, int]:
        """
        :type: Tuple[int, int, int]

        The assumed foreground color of the output device. This 
        is used to determine how to apply the foreground pen in 
        FGBG modes like :py:attr:`CanvasMode.CHAFA_CANVAS_MODE_FGBG`.

        The color is a tuple containing 3 integers in range [0,255] 
        corresponding to red, green and blue respectively.
        """
        # Get the color
        color = self._get_fg_color()

        # convert to tuple
        return packed_8bit_to_tuple(color)

    
    @property
    def bg_color(self) -> Tuple[int, int, int]:
        """
        :type: Tuple[int, int, int]

        The assumed foreground color of the output device. This 
        is used to determine how to apply the foreground pen in 
        FGBG modes like :py:attr:`CanvasMode.CHAFA_CANVAS_MODE_FGBG`.

        The color is a tuple containing 3 integers in range [0,255] 
        corresponding to red, green and blue respectively.
        """
        # Get the color
        color = self._get_bg_color()

        # convert to tuple
        return packed_8bit_to_tuple(color)


    @property
    def passthrough(self) -> Passthrough:
        # Get passthrough
        through = self._get_passthrough()

        # Convert to enum
        return Passthrough(through)


    def get_geometry(self) -> Tuple[int, int]:
        """
        Get the config's canvas geometry in character cells. 
        This is the same as inspecting :py:attr:`width` 
        and :py:attr:`height`

        :rtype: typing.Tuple[int, int] of width and height.
        """

        # Init pointers
        width  = ctypes.pointer(ctypes.c_int(-1))
        height = ctypes.pointer(ctypes.c_int(-1))

        # get geometry
        _Chafa.chafa_canvas_config_get_geometry.argtypes = [
            ctypes.c_void_p,
            ctypes.POINTER(ctypes.c_int),
            ctypes.POINTER(ctypes.c_int)
        ]

        _Chafa.chafa_canvas_config_get_geometry(
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
        _Chafa.chafa_canvas_config_get_fg_only_enabled.argtypes = [
            ctypes.c_void_p
        ]

        _Chafa.chafa_canvas_config_get_fg_only_enabled.restype = ctypes.c_bool

        # Get fg_only 
        fg_only = _Chafa.chafa_canvas_config_get_fg_only_enabled(self._canvas_config)

        return fg_only


    def _get_fg_color(self) -> int:
        """
        Wrapper for chafa_canvas_config_get_fg_color
        """

        # Set types
        _Chafa.chafa_canvas_config_get_fg_color.argtypes = [
            ctypes.c_void_p
        ]

        _Chafa.chafa_canvas_config_get_fg_color.restype = ctypes.c_uint32

        # Get fg_color
        color = _Chafa.chafa_canvas_config_get_fg_color(
            self._canvas_config 
        )

        return color

    
    def _get_bg_color(self) -> int:
        """
        Wrapper for chafa_canvas_config_get_bg_color
        """

        # Set types
        _Chafa.chafa_canvas_config_get_bg_color.argtypes = [
            ctypes.c_void_p
        ]

        _Chafa.chafa_canvas_config_get_bg_color.restype = ctypes.c_uint32

        # Get bg_color
        color = _Chafa.chafa_canvas_config_get_bg_color(
            self._canvas_config 
        )

        return color

    
    def _get_transparency_threshold(self) -> float:
        """
        Wrapper for chafa_canvas_config_get_transparency_threshold
        """

        # Set types
        _Chafa.chafa_canvas_config_get_transparency_threshold.argtypes = [
            ctypes.c_void_p
        ]

        _Chafa.chafa_canvas_config_get_transparency_threshold.restype = ctypes.c_float

        # Get threshold
        threshold = _Chafa.chafa_canvas_config_get_transparency_threshold(self._canvas_config)

        return threshold


    def _get_work_factor(self) -> float:
        """
        Wrapper for chafa_canvas_config_get_work_factor
        """

        # Set types
        _Chafa.chafa_canvas_config_get_work_factor.argtypes = [
            ctypes.c_void_p
        ]

        _Chafa.chafa_canvas_config_get_work_factor.restype = ctypes.c_float

        # Get factor
        factor = _Chafa.chafa_canvas_config_get_work_factor(self._canvas_config)

        return factor


    def _get_pixel_mode(self) -> PixelMode:
        """
        Wrapper for chafa_canvas_config_get_pixel_mode
        """

        # Set types
        _Chafa.chafa_canvas_config_get_pixel_mode.argtypes = [ctypes.c_void_p]
        _Chafa.chafa_canvas_config_get_pixel_mode.restype  = ctypes.c_uint

        # Get mode
        pixel_mode = _Chafa.chafa_canvas_config_get_pixel_mode(self._canvas_config)

        return PixelMode(pixel_mode)

    
    def _get_dither_grain_size(self) -> Tuple[int, int]:
        """
        Wrapper for chafa_canvas_config_get_dither_grain_size
        """

        # Specify types
        _Chafa.chafa_canvas_config_get_dither_grain_size.argtypes = [
            ctypes.c_void_p,
            ctypes.POINTER(ctypes.c_int),
            ctypes.POINTER(ctypes.c_int)
        ]

        width_out  = ctypes.pointer(ctypes.c_int(0))
        height_out = ctypes.pointer(ctypes.c_int(0))

        # Set grain size
        _Chafa.chafa_canvas_config_get_dither_grain_size(self._canvas_config, width_out, height_out)

        return (width_out.contents.value, height_out.contents.value)

    
    def _get_cell_geometry(self) -> Tuple[int, int]:
        """
        Wrapper for chafa_canvas_config_get_dither_grain_size
        """

        # Specify types
        _Chafa.chafa_canvas_config_get_cell_geometry.argtypes = [
            ctypes.c_void_p,
            ctypes.POINTER(ctypes.c_int),
            ctypes.POINTER(ctypes.c_int)
        ]

        width_out  = ctypes.pointer(ctypes.c_int(0))
        height_out = ctypes.pointer(ctypes.c_int(0))

        # Set grain size
        _Chafa.chafa_canvas_config_get_cell_geometry(self._canvas_config, width_out, height_out)

        return (width_out.contents.value, height_out.contents.value)

    
    def _get_dither_mode(self) -> DitherMode:
        """
        Wrapper for chafa_canvas_config_get_cnavas_mode
        """

        # Specify types
        _Chafa.chafa_canvas_config_get_dither_mode.argtypes = [ctypes.c_void_p]
        _Chafa.chafa_canvas_config_get_dither_mode.restype  = ctypes.c_uint

        # Get mode
        mode = _Chafa.chafa_canvas_config_get_dither_mode(self._canvas_config)

        return DitherMode(mode)


    def _get_dither_intensity(self) -> float:
        """
        Wrapper for chafa_canvas_config_get_dither_intensity
        """

        # Specify types
        _Chafa.chafa_canvas_config_get_dither_intensity.argtypes = [
            ctypes.c_void_p
        ]

        _Chafa.chafa_canvas_config_get_dither_intensity.restype = ctypes.c_float

        # Get intensity
        intensity = _Chafa.chafa_canvas_config_get_dither_intensity(self._canvas_config)

        return intensity

    
    def _get_canvas_mode(self) -> CanvasMode:
        """
        Wrapper for chafa_canvas_config_get_cnavas_mode
        """

        # Specify types
        _Chafa.chafa_canvas_config_get_canvas_mode.argtypes = [ctypes.c_void_p]
        _Chafa.chafa_canvas_config_get_canvas_mode.restype  = ctypes.c_uint

        # Get mode
        mode = _Chafa.chafa_canvas_config_get_canvas_mode(self._canvas_config)

        return CanvasMode(mode)

    
    def _get_color_extractor(self) -> ColorExtractor:
        """
        Wrapper for chafa_canvas_config_get_color_extractor
        """

        # Set types
        _Chafa.chafa_canvas_config_get_color_extractor.argtypes = [ctypes.c_void_p]
        _Chafa.chafa_canvas_config_get_color_extractor.restype  = ctypes.c_uint

        # Get extractor
        extractor = _Chafa.chafa_canvas_config_get_color_extractor(self._canvas_config)

        return ColorExtractor(extractor)

    
    def _get_color_space(self) -> ColorSpace:
        """
        Wrapper for chafa_canvas_config_get_color_space
        """

        # Set types
        _Chafa.chafa_canvas_config_get_color_space.argtypes = [ctypes.c_void_p]
        _Chafa.chafa_canvas_config_get_color_space.restype  = ctypes.c_uint

        # Get space
        space = _Chafa.chafa_canvas_config_get_color_space(self._canvas_config)

        return ColorSpace(space)


    def _get_preprocessing_enabled(self) -> bool:
        """
        Wrapper for chafa_canvas_config_get_preprocessing_enabled
        """

        # Set types
        _Chafa.chafa_canvas_config_get_preprocessing_enabled.argtypes = [ctypes.c_void_p]
        _Chafa.chafa_canvas_config_get_preprocessing_enabled.restype  = ctypes.c_bool

        # Get preprocessing value 
        preprocessing = _Chafa.chafa_canvas_config_get_preprocessing_enabled(self._canvas_config)

        return preprocessing


    def _get_optimizations(self) -> int:
        """
        Wrapper for chafa_canvas_config_get_optimizations
        """

        # Specify types
        _Chafa.chafa_canvas_config_get_optimizations.argtypes = [
            ctypes.c_void_p
        ]

        _Chafa.chafa_canvas_config_get_optimizations.restype = ctypes.c_uint

        return _Chafa.chafa_canvas_config_get_optimizations(self._canvas_config)

    
    def _get_passthrough(self) -> int:
        """
        Wrapper for chafa_canvas_config_get_passthrough
        """

        # Specify types
        _Chafa.chafa_canvas_config_get_passthrough.argtypes = [
            ctypes.c_void_p
        ]

        _Chafa.chafa_canvas_config_get_passthrough.restype = ctypes.c_uint

        return _Chafa.chafa_canvas_config_get_passthrough(self._canvas_config)


    def peek_symbol_map(self) -> ReadOnlySymbolMap:
        """
        Wrapper for chafa_canvas_config_peek_symbol_map
        """

        # define types
        _Chafa.chafa_canvas_config_peek_symbol_map.argtypes = [
            ctypes.c_void_p
        ]

        _Chafa.chafa_canvas_config_peek_symbol_map.restype = ctypes.c_void_p

        # Get new pointer
        new_pointer = _Chafa.chafa_canvas_config_peek_symbol_map(self._canvas_config)

        # Init RO SymbolMap
        symbol_map = ReadOnlySymbolMap()
        symbol_map._symbol_map = new_pointer

        return symbol_map



class CanvasConfig(ReadOnlyCanvasConfig):
    # === Width & Height property ===
    @ReadOnlyCanvasConfig.height.setter
    def height(self, value: int):
        value = int(value)

        self._set_geometry(self.width, value)

    @ReadOnlyCanvasConfig.width.setter
    def width(self, value: int):
        value = int(value)

        self._set_geometry(value, self.height)


    # === pixel mode property ===
    @ReadOnlyCanvasConfig.pixel_mode.setter
    def pixel_mode(self, mode: PixelMode):
        mode = PixelMode(mode)

        self._set_pixel_mode(mode)

    
    # === color extractor property ===

    @ReadOnlyCanvasConfig.color_extractor.setter
    def color_extractor(self, extractor: ColorExtractor):
        extractor = ColorExtractor(extractor)

        self._set_color_extractor(extractor)


    # === color space property ===

    @ReadOnlyCanvasConfig.color_space.setter
    def color_space(self, space: ColorSpace):
        space = ColorSpace(space)

        self._set_color_space(space)


    # === canvas mode property ===

    @ReadOnlyCanvasConfig.canvas_mode.setter
    def canvas_mode(self, mode: CanvasMode):
        mode = CanvasMode(mode)

        self._set_canvas_mode(mode)


    # === preprocessing property ===

    @ReadOnlyCanvasConfig.preprocessing.setter
    def preprocessing(self, preproc: bool):
        if preproc is None:
            raise TypeError("preprocessing must not be None")

        preproc = bool(preproc)

        self._set_preprocessing_enabled(preproc)
    
    
    # === dither grain width & height ===
    
    @ReadOnlyCanvasConfig.dither_width.setter
    def dither_width(self, width: int):
        width = int(width)

        self._set_dither_grain_size(width, self.dither_height)

    
    @ReadOnlyCanvasConfig.dither_height.setter
    def dither_height(self, height: int):
        height = int(height)

        self._set_dither_grain_size(self.dither_width, height)


    # === dither mode property ===
    
    @ReadOnlyCanvasConfig.dither_mode.setter
    def dither_mode(self, mode: DitherMode):
        mode = DitherMode(mode)

        self._set_dither_mode(mode)

    
    # === dither intensity ===

    @ReadOnlyCanvasConfig.dither_intensity.setter
    def dither_intensity(self, intensity: float):
        intensity = float(intensity)

        if intensity < 0:
            raise ValueError("Dither intensity must be positive.")

        self._set_dither_intensity(intensity)
    

    # === optimizations ===

    @ReadOnlyCanvasConfig.optimizations.setter
    def optimizations(self, optimizations: Tuple):
        # Convert optimizations to proper type to
        # raise appropriate errors
        if not isinstance(optimizations, Iterable):
            raise TypeError(f"optimizations must be iterable, not {type(optimizations)}")

        # Or all optimizations together
        compounded = 0
        for flag in optimizations:
            # Convert flag to Optimizations to get error if invalid
            flag = Optimizations(flag)

            compounded |= flag

        self._set_optimizations(compounded)


    # === cell width & height ===
    
    @ReadOnlyCanvasConfig.cell_width.setter
    def cell_width(self, width: int):
        width = int(width)

        self._set_cell_geometry(width, self.cell_height)

    
    @ReadOnlyCanvasConfig.cell_height.setter
    def cell_height(self, height: int):
        height = int(height)

        self._set_cell_geometry(self.cell_width, height)


    # === Transparency threshold ===
    
    @ReadOnlyCanvasConfig.transparency_threshold.setter
    def transparency_threshold(self, threshold: float):
        threshold = float(threshold)

        if 1 < threshold or threshold < 0:
            raise ValueError("Transparency threshold must be in range [0,1]")

        self._set_transparency_threshold(threshold)


    # === Work factor ===

    @ReadOnlyCanvasConfig.work_factor.setter
    def work_factor(self, factor: float):
        factor = float(factor)

        if 1 < factor or factor < 0:
            raise ValueError("Work factor must be in range [0,1]")

        self._set_work_factor(factor)
        

    # === fg only ===

    @ReadOnlyCanvasConfig.fg_only.setter
    def fg_only(self, fg_only: bool):
        if fg_only is None:
            raise TypeError("fg_only must not be None")

        fg_only = bool(fg_only)

        self._set_fg_only_enabled(fg_only)
        

    # === fg and bg colors ===

    @ReadOnlyCanvasConfig.fg_color.setter
    def fg_color(self, fg_color: Tuple[int, int, int]):

        if isinstance(fg_color, str):
            raise TypeError(f"fg_color must not be a string")

        if not isinstance(fg_color, Iterable):
            raise TypeError(f"fg_color must be iterable, not {type(fg_color)}")

        if len(fg_color) != 3:
            raise ValueError("fg_color must have exactly 3 values")

        color  = tuple_to_packed_8bit(fg_color)

        self._set_fg_color(color)


    @ReadOnlyCanvasConfig.bg_color.setter
    def bg_color(self, bg_color: Tuple[int, int, int]):

        if isinstance(bg_color, str):
            raise TypeError(f"bg_color must not be a string")

        if not isinstance(bg_color, Iterable):
            raise TypeError(f"bg_color must be iterable, not {type(bg_color)}")

        if len(bg_color) != 3:
            raise ValueError("bg_color must have exactly 3 values")

        color = tuple_to_packed_8bit(bg_color)

        self._set_bg_color(color)

    
    @ReadOnlyCanvasConfig.passthrough.setter
    def passthrough(self, through: Passthrough):
        through = Passthrough(through)

        self._set_passthrough(through)



    def copy(self) -> CanvasConfig:
        """
        Creates a new :py:class:`CanvasConfig` that is a copy of this config.

        :rtype: CanvasConfig
        """

        # define types
        _Chafa.chafa_canvas_config_copy.argtypes = [
            ctypes.c_void_p
        ]

        _Chafa.chafa_canvas_config_copy.restype = ctypes.c_void_p

        # Init new config
        new_config = CanvasConfig()

        # Get new pointer
        config_copy = _Chafa.chafa_canvas_config_copy(self._canvas_config)

        new_config._canvas_config = config_copy

        return new_config


    def _set_geometry(self, width: int, height: int):
        """
        Wrapper for chafa_canvas_config_set_geometry
        """

        _Chafa.chafa_canvas_config_set_geometry.argtypes = [
            ctypes.c_void_p, 
            ctypes.c_uint, 
            ctypes.c_uint
        ]

        _Chafa.chafa_canvas_config_set_geometry(
            self._canvas_config, 
            width, 
            height
        )


    def _set_fg_only_enabled(self, fg_only: bool):
        """
        Wrapper for chafa_canvas_config_set_fg_only_enabled
        """

        # Set types
        _Chafa.chafa_canvas_config_set_fg_only_enabled.argtypes = [
            ctypes.c_void_p,
            ctypes.c_bool
        ]

        # Set threshold
        _Chafa.chafa_canvas_config_set_fg_only_enabled(
            self._canvas_config,
            fg_only
        )


    def _set_fg_color(self, fg_color: int):
        """
        Wrapper for chafa_canvas_config_set_fg_color
        """

        # Set types
        _Chafa.chafa_canvas_config_set_fg_color.argtypes = [
            ctypes.c_void_p,
            ctypes.c_uint32
        ]

        # Set fg_color
        color = _Chafa.chafa_canvas_config_set_fg_color(
            self._canvas_config,
            fg_color
        )


    def _set_bg_color(self, bg_color: int):
        """
        Wrapper for chafa_canvas_config_set_bg_color
        """

        # Set types
        _Chafa.chafa_canvas_config_set_bg_color.argtypes = [
            ctypes.c_void_p,
            ctypes.c_uint32
        ]

        # Set bg_color
        color = _Chafa.chafa_canvas_config_set_bg_color(
            self._canvas_config,
            bg_color
        )


    def _set_transparency_threshold(self, threshold: float):
        """
        Wrapper for chafa_canvas_config_set_transparency_threshold
        """

        # Set types
        _Chafa.chafa_canvas_config_set_transparency_threshold.argtypes = [
            ctypes.c_void_p,
            ctypes.c_float
        ]

        # Set threshold
        _Chafa.chafa_canvas_config_set_transparency_threshold(
            self._canvas_config,
            threshold
        )


    def _set_work_factor(self, factor: float):
        """
        Wrapper for chafa_canvas_config_set_work_factor
        """

        # Set types
        _Chafa.chafa_canvas_config_set_work_factor.argtypes = [
            ctypes.c_void_p,
            ctypes.c_float
        ]

        # Set factor
        _Chafa.chafa_canvas_config_set_work_factor(
            self._canvas_config,
            factor
        )

    
    def _set_pixel_mode(self, mode: PixelMode):
        """
        Wrapper for chafa_canvas_config_set_pixel_mode
        """

        # Specify types
        _Chafa.chafa_canvas_config_set_pixel_mode.argtypes = [
            ctypes.c_void_p,
            ctypes.c_uint
        ]

        _Chafa.chafa_canvas_config_set_pixel_mode(self._canvas_config, mode)


    def _set_dither_grain_size(self, width: int, height: int):
        """
        Wrapper for chafa_canvas_config_set_dither_grain_size
        """

        # Specify types
        _Chafa.chafa_canvas_config_set_dither_grain_size.argtypes = [
            ctypes.c_void_p,
            ctypes.c_int,
            ctypes.c_int
        ]

        # Set grain size
        _Chafa.chafa_canvas_config_set_dither_grain_size(self._canvas_config, width, height)


    def _set_cell_geometry(self, width: int, height: int):
        """
        Wrapper for chafa_canvas_config_set_cell_geometry
        """

        # Specify types
        _Chafa.chafa_canvas_config_set_cell_geometry.argtypes = [
            ctypes.c_void_p,
            ctypes.c_int,
            ctypes.c_int
        ]

        # Set grain size
        _Chafa.chafa_canvas_config_set_cell_geometry(self._canvas_config, width, height)

    
    def _set_dither_mode(self, mode: DitherMode):
        """
            wrapper for chafa_canvas_config_set_dither_mode
        """

        # Specify types
        _Chafa.chafa_canvas_config_set_dither_mode.argtypes = [
            ctypes.c_void_p,
            ctypes.c_uint
        ]

        _Chafa.chafa_canvas_config_set_dither_mode(self._canvas_config, mode)


    def _set_dither_intensity(self, intensity: float):
        """
        Wrapper for chafa_canvas_config_set_dither_intensity
        """

        # Specify types
        _Chafa.chafa_canvas_config_set_dither_intensity.argtypes = [
            ctypes.c_void_p,
            ctypes.c_float
        ]

        # Set intensity
        _Chafa.chafa_canvas_config_set_dither_intensity(
            self._canvas_config,
            intensity
        )

    
    def _set_canvas_mode(self, mode: CanvasMode):
        """
            wrapper for chafa_canvas_config_set_canvas_mode
        """

        # Specify types
        _Chafa.chafa_canvas_config_set_canvas_mode.argtypes = [
            ctypes.c_void_p,
            ctypes.c_uint
        ]

        _Chafa.chafa_canvas_config_set_canvas_mode(self._canvas_config, mode)

    
    def _set_color_extractor(self, extractor: ColorExtractor):
        """
        Wrapper for chafa_canvas_config_set_color_extractor
        """

        # Specify types
        _Chafa.chafa_canvas_config_set_color_extractor.argtypes = [
            ctypes.c_void_p,
            ctypes.c_uint
        ]

        _Chafa.chafa_canvas_config_set_color_extractor(self._canvas_config, extractor)

    
    def _set_color_space(self, space: ColorSpace):
        """
        Wrapper for chafa_canvas_config_set_color_space
        """

        # Specify types
        _Chafa.chafa_canvas_config_set_color_space.argtypes = [
            ctypes.c_void_p,
            ctypes.c_uint
        ]

        _Chafa.chafa_canvas_config_set_color_space(self._canvas_config, space)

    
    def _set_preprocessing_enabled(self, preproc: bool):
        """
        Wrapper for chafa_canvas_config_set_preprocessing_enabled
        """

        # Specify types
        _Chafa.chafa_canvas_config_set_preprocessing_enabled.argtypes = [
            ctypes.c_void_p,
            ctypes.c_bool
        ]

        _Chafa.chafa_canvas_config_set_preprocessing_enabled(self._canvas_config, preproc)


    def _set_optimizations(self, optimizations: int):
        """
        Wrapper for chafa_canvas_config_set_optimizations
        """

        # Specify types
        _Chafa.chafa_canvas_config_set_optimizations.argtypes = [
            ctypes.c_void_p,
            ctypes.c_uint
        ]

        # Set optimizations
        _Chafa.chafa_canvas_config_set_optimizations(
            self._canvas_config,
            optimizations
        )


    def _set_passthrough(self, through: Passthrough):
        """
        Wrapper for chafa_canvas_config_set_passthrough
        """

        # Specify types
        _Chafa.chafa_canvas_config_set_passthrough.argtypes = [
            ctypes.c_void_p,
            ctypes.c_uint
        ]

        # Set passthrough
        _Chafa.chafa_canvas_config_set_passthrough(
            self._canvas_config,
            through
        )


    def set_symbol_map(self, symbol_map: SymbolMap):
        """
        Assigns a copy of symbol_map to config.

        :param SymbolMap symbol_map: The symbol_map.
        """
        
        if not isinstance(symbol_map, SymbolMap):
            raise TypeError(f"symbol_map must be a SymbolMap, not {type(symbol_map)}")

        # Specify types
        _Chafa.chafa_canvas_config_set_symbol_map.argtypes = [
            ctypes.c_void_p,
            ctypes.c_void_p
        ]

        _Chafa.chafa_canvas_config_set_symbol_map(self._canvas_config, symbol_map._symbol_map)


    def set_fill_symbol_map(self, fill_symbol_map: SymbolMap):
        """
        Assigns a copy of fill_symbol_map to config.

        Fill symbols are assigned according to their overall 
        foreground to background coverage, disregarding shape. ???

        :param SymbolMap fill_symbol_map: The fill symbol map.
        """

        if not isinstance(fill_symbol_map, SymbolMap):
            raise TypeError(f"fill_symbol_map must be a SymbolMap, not {type(fill_symbol_map)}")

        # Specify types
        _Chafa.chafa_canvas_config_set_fill_symbol_map.argtypes = [
            ctypes.c_void_p,
            ctypes.c_void_p
        ]

        _Chafa.chafa_canvas_config_set_fill_symbol_map(self._canvas_config, fill_symbol_map._symbol_map)

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

        src_width  = int(src_width)
        src_height = int(src_height)

        font_ratio = float(font_ratio)

        if zoom is None:
            raise TypeError("zoom must not be None")

        if stretch is None:
            raise TypeError("stretch must not be None")

        zoom       = bool(zoom)
        stretch    = bool(stretch)


        if src_width <= 0:
            raise ValueError("src_width must be greater than 0")

        if src_height <= 0:
            raise ValueError("src_height must be greater than 0")

        if font_ratio <= 0:
            raise ValueError("font_ratio must be greater than 0")

        _Chafa.chafa_calc_canvas_geometry.argtypes = [
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
        
        _Chafa.chafa_calc_canvas_geometry(
            src_width, src_height,
            new_width, new_height,
            font_ratio,
            zoom,
            stretch
        )

        self.width  = new_width. contents.value
        self.height = new_height.contents.value

