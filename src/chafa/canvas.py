from __future__ import annotations
import ctypes
from typing import Iterable
import array
from typing import Tuple, Union, Generator

from .libraries import _Chafa
from .canvas_config import ReadOnlyCanvasConfig, CanvasConfig
from .enums import *
from .term_info import TermInfo
from .term_db import TermDb
from .placement import Placement

class Canvas:
    def __init__(self, config: CanvasConfig):
        """
        :param CanvasConfig|None config: The config to initialise the 
        canvas with. If None is passed, the canvas will be initialised 
        with hard-coded defaults.

        :raises TypeError: If term_info is not None or :py:class:`TermInfo`
        :raises TypeError: If config is not None or :py:class:`CanvasConfig`
        """
        # Init config
        if config is None:
            _Chafa.chafa_canvas_new.argtypes = [ctypes.c_size_t]
            config = ctypes.c_size_t(0)

        elif not isinstance(config, CanvasConfig):
            raise TypeError(f"config must be of type CanvasConfig or None, not {type(config)}")

        else:
            _Chafa.chafa_canvas_new.argtypes = [ctypes.c_void_p]
            config = config._canvas_config

        # Init canvas
        _Chafa.chafa_canvas_new.restype  =  ctypes.c_void_p

        self._canvas = _Chafa.chafa_canvas_new(config)

        # Placement
        self._placement = None


    class GString(ctypes.Structure):
        _fields_ = [('str',         ctypes.c_char_p),
                    ('len',           ctypes.c_uint),
                    ('allocated_len', ctypes.c_uint)]


    @property
    def placement(self) -> Placement:
        """
        The :py:class:`Placement` of an :py:class:`Image`
        containing a :py:class:`Frame` on the canvas. Use 
        this as an alternative to :py:meth:`draw_all_pixels` 
        and for control over the image's alignment with :py:class:`Align` 
        and :py:class:`Tuck`.
        """

        return self._placement
    

    @placement.setter
    def placement(self, new_placement: Placement):
        self._set_placement(new_placement)


    def _set_placement(self, new_placement: Placement):
        """
        Bindings for chafa_canvas_set_placement
        """
        _Chafa.chafa_canvas_set_placement.argtypes = [
            ctypes.c_void_p,
            ctypes.c_void_p
        ]

        _Chafa.chafa_canvas_set_placement(self._canvas, new_placement._placement)
    

    def new_similar(self) -> Canvas:
        """
        Creates a new canvas configured similarly to this one.

        :rtype: Canvas
        """

        # types
        _Chafa.chafa_canvas_new_similar.argtypes = [
            ctypes.c_void_p
        ]

        _Chafa.chafa_canvas_new_similar.restype = ctypes.c_void_p

        # Get new pointer
        new_pointer = _Chafa.chafa_canvas_new_similar(self._canvas)

        # Init canvas
        new_canvas = Canvas(None)

        # Assign the new pointer to the newly created canvas
        new_canvas._canvas = new_pointer

        return new_canvas


    def peek_config(self) -> ReadOnlyCanvasConfig:
        """
        Returns a read only version of the :py:class:`CanvasConfig` 
        used to initialise the canvas.

        .. attention:: 
            This :py:class:`ReadOnlyCanvasConfig`'s properties can 
            be inspected but not changed.

        :rtype: ReadOnlyCanvasConfig
        """

        # Types
        _Chafa.chafa_canvas_peek_config.argtypes = [
            ctypes.c_void_p
        ]

        _Chafa.chafa_canvas_peek_config.restype = ctypes.c_void_p

        # Get the new pointer
        new_pointer = _Chafa.chafa_canvas_peek_config(self._canvas)

        # Init RO CanvasConfig
        config = ReadOnlyCanvasConfig()
        config._canvas_config = new_pointer

        return config


    def _canvas_slice(self, y_slice=slice(None), x_slice=slice(None), axis=0, y=None, x=None):
        # Get slice of rows
        # Check slice component types

        # Define the hard stop
        config = self.peek_config()
        hard_stop = (config.height, config.width)
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

    def __getitem__(self, pos) -> CanvasInspector:
        """
        You can inspect pixels in the canvas by indexing, 
        similar to if the canvas were a 2d array. When indexing, 
        the first coordinate represents the row (or y coordinate) 
        and the second represents the column (or x coordinate).

        When indexing using a single value, a `generator`_ of 
        relevant :py:class:`CanvasInspector` objects will be 
        returned, representing each pixel in the given row.

        When indexing using two values, a single :py:class:`CanvasInspector` 
        will be returned representing the given pixel.

        Slicing is also supported! You can slice either the row or 
        column coordinates and this will return generators as 
        expected. For example; if you index using ``[:,3]`` you will 
        get a generator for each pixel in the 3rd column of the 
        canvas (0 indexed). 
        
        Slicing using ``[3:6,:5]`` will return generators for rows 3 to 5 
        inclusive. Each of these rows will be represented by a generator 
        for :py:class:`CanvasInspector` objects representing pixels 0 to 
        4 inclusive.

        The take-away from this all is that indexing and slicing should work 
        (mostly) the same as you would expect a 2d array to work. Check out 
        the tutorial for more details.

        :param int|slice|tuple pos: The position to index

        :rtype: CanvasInspector
        """

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

        raise TypeError(f"Indices of invalid type. Got {type(pos)}")


    def _get_char_at(self, x:int, y:int) -> str:
        """
        Wrapper for chafa_canvas_get_char_at
        """

        # Define types
        _Chafa.chafa_canvas_get_char_at.argtypes = [
            ctypes.c_void_p,
            ctypes.c_int,
            ctypes.c_int
        ]

        _Chafa.chafa_canvas_get_char_at.restype = ctypes.c_wchar

        # Get char
        char = _Chafa.chafa_canvas_get_char_at(
            self._canvas,
            x, y
        )

        return char


    def _set_char_at(self, x:int, y:int, char: str):
        """
        Wrapper for chafa_canvas_set_char_at
        """

        # Define types
        _Chafa.chafa_canvas_set_char_at.argtypes = [
            ctypes.c_void_p,
            ctypes.c_int,
            ctypes.c_int,
            ctypes.c_wchar
        ]

        # Set char
        _Chafa.chafa_canvas_set_char_at(
            self._canvas,
            x, y,
            char
        )


    def _get_colors_at(self, x: int, y:int) -> Tuple[int, int]:
        """
        Wrapper for chafa_canvas_get_colors_at
        """

        # Set types
        _Chafa.chafa_canvas_get_colors_at.argtypes = [
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
        _Chafa.chafa_canvas_get_colors_at(
            self._canvas,
            x, y,
            fg_color,
            bg_color
        )

        return fg_color.contents.value, bg_color.contents.value


    def _get_raw_colors_at(self, x: int, y:int) -> Tuple[int, int]:
        """
        Wrapper for chafa_canvas_get_raw_colors_at
        """

        # Set types
        _Chafa.chafa_canvas_get_raw_colors_at.argtypes = [
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
        _Chafa.chafa_canvas_get_raw_colors_at(
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
        _Chafa.chafa_canvas_set_colors_at.argtypes = [
            ctypes.c_void_p,
            ctypes.c_int,
            ctypes.c_int,
            ctypes.c_int,
            ctypes.c_int
        ]

        # Set colors
        _Chafa.chafa_canvas_set_colors_at(
            self._canvas,
            x, y,
            fg,
            bg
        )


    def _set_raw_colors_at(self, x:int, y: int, fg: int, bg: int):
        """
        Wrapper for chafa_canvas_set_raw_colors_at
        """

        # Set types
        _Chafa.chafa_canvas_set_raw_colors_at.argtypes = [
            ctypes.c_void_p,
            ctypes.c_int,
            ctypes.c_int,
            ctypes.c_int,
            ctypes.c_int
        ]

        # Set colors
        _Chafa.chafa_canvas_set_raw_colors_at(
            self._canvas,
            x, y,
            fg,
            bg
        )


    def draw_all_pixels(
        self, 
        src_pixel_type: PixelType, 
        src_pixels:     Union[list, Tuple, array.array, ctypes.Array], 
        src_width:      int, 
        src_height:     int, 
        src_rowstride:  int
    ):
        """
        Draws the given src_pixels to the canvas. Depending on your 
        set :py:class:`PixelMode`, this will be symbols, kitty sequences 
        or sixel sequences. 

        To output the data after drawing, use the :py:meth:`print` method.

        .. note::
            Best performance is achieved by passing a :py:class:`ctypes.Array` 
            for src_pixels. The :py:class:`chafa.loader.Loader` 
            class provides convenient (and reasonably fast) 
            methods for this using the `MagickWand 
            <https://imagemagick.org/script/magick-wand.php>`_ 
            C-library.

        :param PixelType src_pixel_type: The pixel type of src_pixels. This 
            will determine what order the color channels will be read in 
            and whether there is an alpha channel.

        :param list|tuple|array.array|ctypes.Array src_pixels: The 
            source pixel data. This is a one dimensional array where 
            every block of 3 (or 4 depending on the :py:class:`PixelType`) 
            values represents one pixel of the image. The order of the 
            channels is determined by src_pixel_type.

        :param int src_width:  The width of the source image.
        :param int src_height: The width of the source image.

        :param int src_rowstride: The number of values in src_image that 
            represents one line pixels in the source image. Typically this 
            will be the number of channels in the source image multiplied 
            by src_width, e.g. for an image with no alpha channel and a 
            width of 300 pixels, this will be ``3*300``.

        :raises ValueError: if src_width, src_height or src_rowstride 
            are less than or equal to 0.
        """

        # Convert src_pixels to appropriate format
        if isinstance(src_pixels, ctypes.Array):
            src_pixels = src_pixels
        else:
            try:
                src_pixels = (ctypes.c_uint8 * len(src_pixels)).from_buffer(src_pixels)

            except TypeError:
                src_pixels = array.array("B", src_pixels)
                src_pixels = (ctypes.c_uint8 * len(src_pixels)).from_buffer(src_pixels)

        # Make sure types match
        src_pixel_type = PixelType(src_pixel_type)

        src_width     = int(src_width)
        src_height    = int(src_height)
        src_rowstride = int(src_rowstride)

        # Value errors
        if src_width <= 0:
            raise ValueError("src_width must be greater than 0")

        if src_height <= 0:
            raise ValueError("src_height must be greater than 0")

        if src_rowstride <= 0:
            raise ValueError("src_rowstride must be greater than 0")
        
        # Specify types
        _Chafa.chafa_canvas_draw_all_pixels.argtypes = [
            ctypes.c_void_p,
            ctypes.c_uint,
            ctypes.POINTER(ctypes.c_uint8),
            ctypes.c_uint,
            ctypes.c_uint,
            ctypes.c_uint
        ]

        # Draw pixels
        _Chafa.chafa_canvas_draw_all_pixels(
            self._canvas,
            src_pixel_type,
            src_pixels,
            src_width,
            src_height,
            src_rowstride,
        )


    def print(self, term_info: TermInfo=None, fallback=False) -> bytes:
        """
        Builds a UTF-8 string of terminal control sequences and symbols 
        representing the canvas' current contents. This can e.g. be 
        printed to a terminal. The exact choice of escape sequences and 
        symbols, dimensions, etc. is determined by the configuration 
        assigned to canvas on its creation.

        All output lines except for the last one will end in a newline.

        :param TermInfo term_info: The :py:class:`TermInfo` that will 
        provide the control sequences used when printing. If None is 
        specified, the term_info will be initialised with 
        :py:meth:`TermDb.detect`

        :param bool fallback: If True, the term_info (the one provided by
        :py:meth:`TermDb.detect` or the one provided by the user) will 
        be supplemented with fallback control sequences.
        """

        term_db = None

        # Check for term info
        if term_info is None:
            term_db = TermDb()
            term_info = term_db.detect()

        elif not isinstance(term_info, TermInfo):
            raise TypeError(f"term_info must be None or of type TermInfo or None, not {type(term_info)}")

        # Supplement with fallback sequences
        if fallback:
            if term_db is None:
                term_db = TermDb()

            fallback_info = term_db.get_fallback_info()
            term_info.supplement(fallback_info)



        _Chafa.chafa_canvas_print.argtypes = [
            ctypes.c_void_p, 
            ctypes.c_void_p
        ]

        _Chafa.chafa_canvas_print.restype  = ctypes.c_void_p

        output = _Chafa.chafa_canvas_print(self._canvas, term_info._term_info)
        output = self.GString.from_address(output)

        return output.str


    def print_rows(self, term_info: TermInfo=None, fallback=False) -> Generator[bytes]:
        term_db = None

        # Check for term info
        if term_info is None:
            term_db = TermDb()
            term_info = term_db.detect()

        elif not isinstance(term_info, TermInfo):
            raise TypeError(f"term_info must be None or of type TermInfo or None, not {type(term_info)}")

        # Supplement with fallback sequences
        if fallback:
            if term_db is None:
                term_db = TermDb()

            fallback_info = term_db.get_fallback_info()
            term_info.supplement(fallback_info)

        config = self.peek_config()

        max_length = config.height

        # Define storage for output with max_length to accomodate all the possible rows
        output_array = ctypes.POINTER(ctypes.POINTER(self.GString) * max_length)()
        output_rows = ctypes.c_int()

        _Chafa.chafa_canvas_print_rows.argtypes = [
            ctypes.c_void_p,
            ctypes.c_void_p,
            ctypes.POINTER(ctypes.POINTER(ctypes.POINTER(self.GString)*max_length)),
            ctypes.POINTER(ctypes.c_int)
        ]

        _Chafa.chafa_canvas_print_rows(self._canvas, term_info._term_info, output_array, output_rows)

        # Create a generator for the output
        current_row = 0
        while current_row < output_rows.value:
            yield output_array.contents[current_row].contents.str
            current_row += 1




class CanvasInspector:
    def __init__(self, canvas: Canvas, y: int, x: int):
        # Get the configured height and width of the canvas
        canvas_config = canvas.peek_config()
        width  = canvas_config.width
        height = canvas_config.height

        # Check if x and y are within bounds
        if (
            (x >= width or y >= height)
            or (x < 0 and width  < abs(x)) # If we have a negative we need to make sure it 
            or (y < 0 and height < abs(y)) # is not going past the start of the canvas
        ):
            raise ValueError(
                f"Coordinates ({x},{y}) are out of bounds for canvas with dimensions {width}x{height}."
            )
        
        self._canvas = canvas

        # Use modulo to cast negatives into positives
        self._x = x % width
        self._y = y % height


    # === FG COLOR ===

    @staticmethod
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

    @staticmethod
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
        

    @property
    def fg_color(self) -> Union[Tuple[int, int, int], None]:
        """
        :type: tuple[int, int, int] | None

        The foreground color at the inspector's pixel. The color 
        is represented as None if transparent or a tuple of 3 
        integers in range [0,255], representing the color in 
        (R, G, B) format.

        For double-width characters, both cells will be set to the 
        same color.

        :raises TypeError:  if fg_color is not an :py:class:`Iterable` 
            other than :py:class:`str`.
        :raises ValueError: if fg_color is not None and does not contain 
            exactly 3 values. 
        :raises ValueError: if fg_color contains a value greater than 255 
            or less than 0.
        """
        # Get the color at pixel
        color = self._canvas._get_colors_at(self.x, self.y)[0]

        # Return None for transparency
        if color == -1:
            return None

        # convert to tuple
        return self.packed_8bit_to_tuple(color)


    @fg_color.setter
    def fg_color(self, fg_color: Tuple[int, int, int]):
        # Remove foreground if we get none
        if fg_color is None:
            self.remove_foreground()
            return
    	
        # Check types
        if isinstance(fg_color, str):
            raise TypeError(f"fg_color must not be a string")

        if not isinstance(fg_color, Iterable):
            raise TypeError(f"fg_color must be iterable, not {type(fg_color)}")

        if len(fg_color) != 3:
            raise ValueError("fg_color must have exactly 3 values")

        color = self.tuple_to_packed_8bit(fg_color)

        bg_color = self.bg_color

        if bg_color is None:
            bg_color = -1

        else:
            bg_color = self.tuple_to_packed_8bit(bg_color)

        self._canvas._set_colors_at(self.x, self.y, color, bg_color)

    @property
    def raw_fg_color(self) -> int:
        """
        :type: int

        The raw foreground color at the inspector's pixel. The colors 
        are -1 for transparency, a packed 8-bit RGB value 
        (``0x00RRGGBB``) in truecolor mode, or the raw pen value (0-255) 
        in indexed modes.
        """
        # Get the color at pixel
        color = self._canvas._get_raw_colors_at(self.x, self.y)[0]

        return int(color)


    @raw_fg_color.setter
    def raw_fg_color(self, fg_color: int):

        if fg_color < -1 or fg_color > 0xFFFFFF:
            raise ValueError("color must be in range [-1, 0xFFFFFF]")

        self._canvas._set_raw_colors_at(self.x, self.y, fg_color, self.raw_bg_color)


    # === BG COLOR ===
    
    @property
    def bg_color(self) -> Union[Tuple[int, int, int], None]:
        """
        :type: tuple[int, int, int] | None

        The background color at the inspector's pixel. The color is 
        represented as None if transparent or a tuple of 3 integers 
        in range [0,255], representing the color in (R, G, B) format.

        For double-width characters, both cells will be set to the same color.

        :raises TypeError:  if bg_color is not an :py:class:`Iterable` 
            other than :py:class:`str`.
        :raises ValueError: if bg_color is not None and does not 
            contain exactly 3 values. 
        :raises ValueError: if bg_color contains a value greater than 255 
            or less than 0.
        """
        # Get the color at pixel
        color = self._canvas._get_colors_at(self.x, self.y)[1]

        if color == -1:
            return None

        # convert to tuple
        return self.packed_8bit_to_tuple(color)
    
    @bg_color.setter
    def bg_color(self, bg_color: Tuple[int, int, int]):

        # Remove background if we get none
        if bg_color is None:
            self.remove_background()
            return

        # Check types
        if isinstance(bg_color, str):
            raise TypeError(f"bg_color must not be a string")

        if not isinstance(bg_color, Iterable):
            raise TypeError(f"bg_color must be iterable, not {type(bg_color)}")

        if len(bg_color) != 3:
            raise ValueError("bg_color must have exactly 3 values")

        color  = self.tuple_to_packed_8bit(bg_color)

        fg_color = self.fg_color

        if fg_color is None:
            fg_color = -1

        else:
            fg_color = self.tuple_to_packed_8bit(fg_color)

        self._canvas._set_colors_at(self.x, self.y, fg_color, color)

    @property
    def raw_bg_color(self) -> int:
        """
        :type: int

        The raw background color at the inspector's pixel. The colors 
        are -1 for transparency, a packed 8-bit RGB value 
        (``0x00RRGGBB``) in truecolor mode, or the raw pen value (0-255) 
        in indexed modes.
        """
        # Get the color at pixel
        color = self._canvas._get_raw_colors_at(self.x, self.y)[1]

        return int(color)


    @raw_bg_color.setter
    def raw_bg_color(self, bg_color: int):

        if bg_color < -1 or bg_color > 0xFFFFFF:
            raise ValueError("color must be in range [-1, 0xFFFFFF]")

        self._canvas._set_raw_colors_at(self.x, self.y, self.raw_fg_color, bg_color)

    # === CHAR ===

    @property
    def char(self) -> str:
        """
        :type: str

        The character at the inspector's pixel. For double-width 
        characters, the leftmost cell must contain the character 
        and the cell to the right of it will automatically be set 
        to 0.

        :raises ValueError: if char is not of length 1.
        """
        return self._canvas._get_char_at(self.x, self.y)

    @char.setter
    def char(self, char: str):
        char = str(char)

        if len(char) != 1:
            raise ValueError(f"char must be of length 1")

        self._canvas._set_char_at(self.x, self.y, char)


    # === Coordinates ===

    @property
    def x(self) -> int:
        """
        :type: int

        The x coordinate of the inspector.

        :raises ValueError: if x is not less than the height of the canvas.
        """
        return self._x

    @x.setter
    def x(self, value: int):
        width = self._canvas.peek_config().width

        value = int(value)

        if value >= width:
            raise ValueError(
                f"x-coordinate {value} is out of bounds for canvas with width {width}."
            )
        
        self._x = value

    @property
    def y(self) -> int:
        """
        :type: int

        The y coordinate of the inspector.

        :raises ValueError: if y is not less than the height of the canvas.
        """
        return self._y

    @y.setter
    def y(self, value: int):
        height = self._canvas.peek_config().height

        value = int(value)

        if value >= height:
            raise ValueError(
                f"y-coordinate {value} is out of bounds for canvas with width {height}."
            )
        
        self._y = value

    
    def remove_background(self):
        """
        A function that sets the background color at the 
        inspectors pixel to be transparent.
        """

        fg_color = self.fg_color

        if fg_color is None:
            fg_color = -1

        else:
            fg_color = self.tuple_to_packed_8bit(fg_color)

        self._canvas._set_colors_at(self.x, self.y, fg_color, -1)

    def remove_foreground(self):
        """
        A function that sets the foreground color at the 
        inspectors pixel to be transparent.
        """

        bg_color = self.bg_color

        if bg_color is None:
            bg_color = -1

        else:
            bg_color = self.tuple_to_packed_8bit(bg_color)

        self._canvas._set_colors_at(self.x, self.y, -1, bg_color)
