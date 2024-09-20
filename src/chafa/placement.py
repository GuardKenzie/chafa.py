from __future__ import annotations
import ctypes

from .libraries import _Chafa
from .enums import Tuck, Align
from .image import Image


class Placement:
    def __init__(self, image: Image, id: int = 0):
        """
        This class defines the placement of an :py:class:`Image` on a 
        :py:class:`Canvas`. 

        .. note::
            None of placement's properties have any effect if the 
            :py:class:`Canvas`'s pixel mode is set to 
            :py:attr:`PixelMode.CHAFA_PIXEL_MODE_SYMBOLS`.

        :param image: The :py:class:`Image` to be placed.
        :param id: An id to assign to the image. Leave as ``0`` to assign 
            one automatically.
        """
        
        _Chafa.chafa_placement_new.argtypes = [
            ctypes.c_void_p,
            ctypes.c_int
        ]

        _Chafa.chafa_placement_new.restype = ctypes.c_void_p

        self._placement = _Chafa.chafa_placement_new(image._image, id)
        self._image = image


    # === Tuck property ===
    
    @property
    def tuck(self) -> Tuck:
        """
        :type: Tuck

        This describes how the :py:class:`Image` is resized to fit on the 
        :py:class:`Canvas`, and defaults to :py:attr:`Tuck.CHAFA_TUCK_STRETCH`.
        """
        
        return self._get_tuck()


    @tuck.setter
    def tuck(self, new_tuck: Tuck):
        new_tuck = Tuck(new_tuck)

        self._set_tuck(new_tuck)


    # === Halign property === 

    @property
    def halign(self) -> Align:
        """
        :type: Align

        Describes the horizontal alignment of the :py:class:`Image` on the 
        :py:class:`Canvas`.
        """
        
        return self._get_halign()


    @halign.setter
    def halign(self, new_halign: Align):
        new_halign = Align(new_halign)

        self._set_halign(new_halign)


    # === Valign property ===

    @property
    def valign(self) -> Align:
        """
        :type: Align

        Describes the horizontal alignment of the :py:class:`Image` on the 
        :py:class:`Canvas`.
        """
        
        return self._get_valign()


    @valign.setter
    def valign(self, new_valign: Align):
        new_valign = Align(new_valign)

        self._set_valign(new_valign)
    

    def _get_tuck(self) -> Tuck:
        """
        Bindings for chafa_placement_get_tuck
        """
        _Chafa.chafa_placement_get_tuck.argtypes = [ctypes.c_void_p]

        _Chafa.chafa_placement_get_tuck.restype  = ctypes.c_uint

        tuck =_Chafa.chafa_placement_get_tuck(self._placement)
        return Tuck(tuck)
    

    def _set_tuck(self, new_tuck: Tuck):
        """
        Bindings for chafa_placement_set_tuck
        """
        _Chafa.chafa_placement_set_tuck.argtypes = [
            ctypes.c_void_p,
            ctypes.c_uint
        ]

        _Chafa.chafa_placement_set_tuck(self._placement, new_tuck)


    def _get_halign(self) -> Align:
        """
        Bindings for chafa_placement_get_halign
        """
        _Chafa.chafa_placement_get_halign.argtypes = [ctypes.c_void_p]

        _Chafa.chafa_placement_get_halign.restype  = ctypes.c_uint

        halign =_Chafa.chafa_placement_get_halign()
        return Align(halign)
    

    def _set_halign(self, new_halign: Align):
        """
        Bindings for chafa_placement_set_halign
        """
        _Chafa.chafa_placement_set_halign.argtypes = [
            ctypes.c_void_p,
            ctypes.c_uint
        ]

        _Chafa.chafa_placement_set_halign(self._placement, new_halign)


    def _get_valign(self) -> Align:
        """
        Bindings for chafa_placement_get_valign
        """
        _Chafa.chafa_placement_get_valign.argtypes = [ctypes.c_void_p]

        _Chafa.chafa_placement_get_valign.restype  = ctypes.c_uint

        valign =_Chafa.chafa_placement_get_valign()
        return Align(valign)
    

    def _set_valign(self, new_valign: Align):
        """
        Bindings for chafa_placement_set_valign
        """
        _Chafa.chafa_placement_set_valign.argtypes = [
            ctypes.c_void_p,
            ctypes.c_uint
        ]

        _Chafa.chafa_placement_set_valign(self._placement, new_valign)