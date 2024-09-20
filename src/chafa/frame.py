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
        """
        This defines a frame of an image. This has to be added to an 
        :py:class:`Image`. The inputs are the same as in 
        :py:meth:`Canvas.draw_all_pixels`.

        .. note::
            Best performance is achieved by passing a :py:class:`ctypes.Array` 
            for src_pixels. A fast way to do this is to use 
            `Pillow <https://pillow.readthedocs.io/en/stable/>`_; specifically the 
            `Image.tobytes <https://pillow.readthedocs.io/en/stable/reference/Image.html#PIL.Image.Image.tobytes>`_ method.

        :param PixelType src_pixel_type: The pixel type of src_pixels.
            This will determine what order the color channels will be read 
            in and whether there is an alpha channel.
        :param list|tuple|array.array|ctypes.Array src_pixels: The source pixel
            data. This is a one dimensional array where every block of 3 (or 4 depending 
            on the :py:class:`PixelType`) values represents one pixel of the image. 
            The order of the channels is determined by src_pixel_type.
        :param int src_width:  The width of the source image.
        :param int src_height: The width of the source image.
        :param int src_rowstride: The number of values in src_image that 
            represents one line pixels in the source image. Typically this will be 
            the number of channels in the source image multiplied by src_width, 
            e.g. for an image with no alpha channel and a width of 300 pixels, this 
            will be ``3*300``.

        :raises ValueError: if src_width, src_height or src_rowstride are less 
            than or equal to 0.
        """
        
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