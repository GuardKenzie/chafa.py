from __future__ import annotations
import ctypes

from .libraries import _Chafa
from .frame import Frame

class Image:
    def __init__(self):
        """
        A container for a :py:class:`Frame`. To be placed on a 
        :py:class:`Placement`.
        """
        
        _Chafa.chafa_image_new.restype = ctypes.c_void_p

        self._image = _Chafa.chafa_image_new()
        self._frame = None


    # === Frame property ===

    @property
    def frame(self) -> Frame:
        """
        :type: Frame

        The :py:class:`Frame` for the image
        """
        
        return self._frame
    

    @frame.setter
    def frame(self, new_frame: Frame):
        self._set_frame(new_frame)
    

    def _set_frame(self, new_frame: Frame):
        """
        Bindings for chafa_image_set_frame
        """

        _Chafa.chafa_image_set_frame.argtypes = [
            ctypes.c_void_p,
            ctypes.c_void_p    
        ]

        _Chafa.chafa_image_set_frame(self._image, new_frame._frame)

        self._frame = new_frame