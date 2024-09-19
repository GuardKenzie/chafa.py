from __future__ import annotations
from typing import Union, Tuple
import array
import ctypes

from .libraries import _Chafa
from .enums import PixelType

class Frame:
    def __init__(
        self, 
        src_pixel_type: PixelType, 
        src_pixels:     Union[list, Tuple, array.array, ctypes.Array], 
        src_width:      int, 
        src_height:     int, 
        src_rowstride:  int
    ):
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
        
        _Chafa.chafa_frame_new.argtypes = [
            ctypes.POINTER(ctypes.c_uint8),
            ctypes.c_uint,
            ctypes.c_uint,
            ctypes.c_uint,
            ctypes.c_uint
        ]

        _Chafa.chafa_frame_new.restype = ctypes.c_void_p

        # Draw pixels
        self._frame = _Chafa.chafa_frame_new(
            src_pixels,
            src_pixel_type,
            src_width,
            src_height,
            src_rowstride,
        )